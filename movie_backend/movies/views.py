
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status


from .models import Movie, Cast, Crew, Emotion, Genre, Person, Review, Comment, ReviewComment, Collection
from .serilalizers import MovieDetailSerializer, MovieListSerializer, ReviewSerializer, ReviewCommentSerializer, CollectionSerializer
from .get_data import get_movie_details, get_cast_crew, serch_movie
from django.shortcuts import get_object_or_404

# Create your views here.

# 영화 리스트 가져오기


class MovieListView(APIView):
    def get(self, request):
        movies = Movie.objects.all()
        serializer = MovieListSerializer(movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# 영화 세부 정보 가져오기


class MovieDetailView(APIView):
    def get(self, request, movie_id):
        movie = Movie.objects.filter(id=movie_id).first()
        credits_data = get_cast_crew(movie_id)
        if not movie:
            print('현재 선택한 영화가 DB에 없음')
            new_movie = get_movie_details(movie_id)
            genre_ids = [genre['id'] for genre in new_movie.get('genres', [])]
            movie = Movie.objects.create(
                id=movie_id,
                title=new_movie['title'],
                original_title=new_movie.get('original_title'),
                release_date=new_movie.get('release_date'),
                overview=new_movie.get('overview'),
                runtime=new_movie.get('runtime'),
                popularity=new_movie.get('popularity'),
                vote_average=new_movie.get('vote_average'),
                vote_count=new_movie.get('vote_count'),
                poster_path=new_movie.get('poster_path'),
                backdrop_path=new_movie.get('backdrop_path'),
                budget=new_movie.get('budget', 0),
                revenue=new_movie.get('revenue', 0),
                adult=new_movie.get('adult', False),
                status=new_movie.get('status'),
                homepage=new_movie.get('homepage'),
                imdb_id=new_movie.get('imdb_id'),
                tagline=new_movie.get('tagline'),
                origin_country=new_movie.get('production_countries', [{}])[
                    0].get('iso_3166_1')
                if new_movie.get('production_countries') else None,
                spoken_languages=new_movie.get('spoken_languages', [{}])[
                    0].get('english_name')
                if new_movie.get('spoken_languages') else None,
            )
            for genre_id in genre_ids:
                genre = Genre.objects.get(id=genre_id)
                movie.genres.add(genre)

            for cast_data in credits_data.get('cast', []):
                # 배우 정보 DB 저장
                person, created = Person.objects.update_or_create(
                    id=cast_data['id'],
                    defaults={
                        'id': cast_data['id'],
                        'name': cast_data['name'],
                        'profile_path': cast_data.get('profile_path'),
                    },
                )

                # 출연한 배우 목록 DB 저장
                cast, created = Cast.objects.update_or_create(
                    name=cast_data['name'],
                    defaults={
                        'character': cast_data.get('character'),
                        'person': person,
                    }
                )

                # 해당 영화에 배우 추가
                movie.cast.add(cast)

            for crew_data in credits_data.get('crew', []):

                person, created = Person.objects.update_or_create(
                    id=crew_data['id'],
                    defaults={
                        'id': crew_data['id'],
                        'name': crew_data['name'],
                        'profile_path': crew_data.get('profile_path'),
                    },
                )
                # 제작진들 DB 저장
                crew, created = Crew.objects.update_or_create(
                    department=crew_data['department'],
                    defaults={
                        'person': person,
                    }
                )
                # 해당 영화에 제작진 추가
                movie.crew.add(crew)
        reviews = Review.objects.filter(movie=movie_id).select_related('user')
        movie_serializer = MovieDetailSerializer(movie)
        review_serializer = ReviewSerializer(reviews, many=True)
        response_data = {
            "movie": movie_serializer.data,
            "reviews": review_serializer.data,
            "credits": credits_data
        }
        print(response_data)
        return Response(response_data, status=status.HTTP_200_OK)

# 영화 검색 기능


class MovieSearchView(APIView):
    def get(self, request):
        query = request.query_params.get('title')
        movie_data = serch_movie(query)
        return Response(movie_data, status=status.HTTP_200_OK)

# 감정 별로 영화 리스트 가져오기


class SelectedEmotionView(APIView):
    def get(self, request, emotion):
        genres = Genre.objects.filter(emotions__name=emotion)
        movies = Movie.objects.filter(genres__in=genres)

        serializer = MovieListSerializer(movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# 영화 리뷰 기능


class ReviewView(APIView):

    def get(self, request, review_id=None):

        if review_id:
            review = get_object_or_404(Review, id=review_id)
            comments = ReviewComment.objects.filter(review=review)
            review_serializer = ReviewSerializer(review)
            comment_serializer = ReviewCommentSerializer(comments, many=True)
            return Response(
                data={
                    'review': review_serializer.data,
                    'comments': comment_serializer.data,
                }, status=status.HTTP_200_OK)

        reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ReviewSerializer(data=request.data, context={
                                      'request': request})  # context 전달
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 좋아요 기능
    def patch(self, request):
        review_id = request.data.get('id', None)
        if not review_id:
            return Response({'error': '리뷰 아이디가 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)
        review = get_object_or_404(Review, id=review_id)
        is_liked = review.likes.filter(id=request.user.id).exists()
        if is_liked:
            review.likes.remove(request.user)
            liked = False
        else:
            review.likes.add(request.user)
            liked = True
        return Response({
            'message': '좋아요 상태 변경 성공',
            'liked': liked,
            'likes_count': review.likes.count(),
        }, status=status.HTTP_200_OK)

    def put(self, request):
        review_id = request.data.get('id', None)
        if not review_id:
            return Response({'error': '리뷰 ID가 필요합니다.'}, status=status.HTTP_403_FORBIDDEN)

        review = get_object_or_404(Review, id=review_id)
        if review.user != request.user:
            return Response({'error': '수정 권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = ReviewSerializer(
            instance=review, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, review_id):
        # review_id = request.data.get('id', None)
        # if  not review_id:
        #     return Response({'error':'리뷰 ID가 필요합니다.'}, status=status.HTTP_400_BAD_REQUEST)

        review = get_object_or_404(Review, id=review_id)
        print(request.user)
        if review.user_id != request.user.id:
            return Response({'error': '삭제 권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)

        review.delete()
        return Response({'message': '리뷰가 삭제되었습니다.'}, status=status.HTTP_204_NO_CONTENT)

# 리뷰의 댓글 기능


class ReviewCommentView(APIView):
    def post(self, request, review_id):
        review = get_object_or_404(Review, id=review_id)
        serializer = ReviewCommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, review=review)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, review_id):
        review = get_object_or_404(Review, id=review_id)
        comments = ReviewComment.objects.filter(review=review)
        serializer = ReviewCommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, comment_id):
        comment = get_object_or_404(ReviewComment, id=comment_id)
        if comment.user != request.user:
            return Response({'error': '수정 권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = ReviewCommentSerializer(
            comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, comment_id):
        comment = get_object_or_404(ReviewComment, id=comment_id)
        if comment.user != request.user:
            return Response({'error': '삭제 권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)

        comment.delete()
        return Response({'message': '댓글 삭제 성공'}, status=status.HTTP_204_NO_CONTENT)

# 플레이리스트 기능


class PlaylistView(APIView):
    # 플레이리스트 추가
    def post(self, request):
        serializer = CollectionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 플레이리스트 가져오기
    def get(self, request, user_id, playlist_id=None):
        if playlist_id:
            playlist = get_object_or_404(Collection, id=playlist_id)
            serializer = CollectionSerializer(playlist)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            playlists = Collection.objects.filter(user=user_id)
            serializer = CollectionSerializer(playlists, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)

    # 플레이리스트 삭제
    def delete(self, request, playlist_id):
        playlist = get_object_or_404(
            Collection, id=playlist_id, user=request.user)
        playlist.delete()
        return Response({'message': '플레이리스트가 삭제되었습니다.'}, status=status.HTTP_204_NO_CONTENT)

    # 플레이리스트 수정
    def put(self, request, playlist_id):
        playlist = get_object_or_404(
            Collection, id=playlist_id, user=request.user)
        data = request.data

        # 제목 수정
        if 'title' in data:
            serializer = CollectionSerializer(
                playlist, data={'title': data['title']}, partial=True)
            if serializer.is_valid():
                serializer.save()

        # 영화 추가
        if 'movies_add' in data:
            for movie_data in data['movies_add']:
                movie = get_object_or_404(Movie, id=movie_data.get('id'))
                playlist.movies.add(movie)

        # 영화 삭제
        if 'movies_remove' in data:
            for movie_data in data['movies_remove']:
                movie = get_object_or_404(Movie, id=movie_data.get('id'))
                playlist.movies.remove(movie)

        new_serializer = CollectionSerializer(playlist)
        return Response(new_serializer.data, status=status.HTTP_200_OK)
