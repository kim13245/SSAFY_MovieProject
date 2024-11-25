

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from .models import Movie, Cast, Crew, Emotion, Genre, Person, Review, Comment, ReviewComment, Collection
from .serilalizers import MovieDetailSerializer, MovieListSerializer, ReviewSerializer, ReviewCommentSerializer, CollectionSerializer
from .get_data import get_movie_details, get_cast_crew, serch_movie, get_movie_trailer
from django.shortcuts import get_object_or_404

# 영화 리스트 가져오기
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


class MovieListView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="영화 목록 가져오기",
        description="데이터베이스에 저장된 모든 영화의 목록",
        responses={
            200: OpenApiResponse(
                response=MovieListSerializer(many=True),
                description="모든 영화의 목록"
            ),
        },
    )
    def get(self, request):
        movies = Movie.objects.all()
        serializer = MovieListSerializer(movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# 영화 세부 정보 가져오기


class MovieDetailView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="영화 상세 데이터",
        parameters=[
            OpenApiParameter("movie_id", int, description="영화 ID"),
        ],
        responses={
            200: OpenApiResponse(
                response=MovieDetailSerializer,
                description="영화 정보와 해당 영화의 리뷰 데이터"
            ),
        },
    )
    @method_decorator(csrf_exempt)
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
        # 디버깅을 위해 반환값 출력 추가
        trailer_data = get_movie_trailer(movie.title)
        print("Trailer Data:", trailer_data)  # 실제로 어떤 데이터가 오는지 확인

        # 데이터 형태에 따른 안전한 처리
        if isinstance(trailer_data, dict) and 'videoId' in trailer_data:
            trailer_id = trailer_data['videoId']
            movie.trailer = trailer_id
            movie.save()
        else:
            print(f"'{movie.title}' 영화의 트레일러를 찾을 수 없습니다.")
            # 트레일러를 찾지 못한 경우 None으로 설정하거나 건너뛰기
            movie.trailer = None
            movie.save()
        reviews = Review.objects.filter(movie=movie_id).select_related('user')
        movie_serializer = MovieDetailSerializer(
            movie, context={'request': request})
        review_serializer = ReviewSerializer(reviews, many=True, context={'request': request})
        response_data = {
            "movie": movie_serializer.data,
            "reviews": review_serializer.data,
            "credits": credits_data
        }
        # print(response_data)
        return Response(response_data, status=status.HTTP_200_OK)


# 영화 검색 기능

class MovieSearchView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="영화 검색",
        description="사용자가 제공한 영화 제목(query)을 바탕으로 TMDB 또는 내부 데이터베이스에서 영화 검색",
        parameters=[
            OpenApiParameter(
                name="title",
                type=str,
                description="검색할 영화의 제목",
                required=True
            )
        ],
        responses={
            200: OpenApiResponse(
                response=MovieListSerializer(many=True),
                description="검색된 영화 목록"
            ),
        },
    )
    def get(self, request):
        query = request.query_params.get('title')
        movie_data = serch_movie(query)
        return Response(movie_data, status=status.HTTP_200_OK)

# 감정 별로 영화 리스트 가져오기


class SelectedEmotionView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="감정으로 영화 목록 조회",
        description="특정 감정과 연결된 장르를 기반으로 해당 장르의 영화를 조회",
        parameters=[
            OpenApiParameter(
                name="emotion",
                type=str,
                description="조회할 감정의 이름",
                required=True
            )
        ],
        responses={
            200: OpenApiResponse(
                response=MovieListSerializer(many=True),
                description="지정된 감정에 해당하는 영화 목록"
            ),
        },
    )
    def get(self, request, emotion):
        genres = Genre.objects.filter(emotions__name=emotion)
        movies = Movie.objects.filter(genres__in=genres)

        serializer = MovieListSerializer(movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# 영화 리뷰 기능


class ReviewView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="리뷰 조회",
        description="특정 리뷰 ID를 사용하여 리뷰를 조회하거나, 모든 리뷰를 가져옴",
        parameters=[
            OpenApiParameter(
                name="review_id",
                type=int,
                description="조회할 리뷰의 ID (선택 사항)",
                required=False
            )
        ],
        responses={
            200: OpenApiResponse(
                response=ReviewSerializer(many=True),
                description="리뷰 목록 또는 단일 리뷰"
            ),
            404: OpenApiResponse(description="리뷰를 찾을 수 없습니다."),
        },
    )
    def get(self, request, review_id=None):

        if review_id:
            review = get_object_or_404(
                Review.objects.prefetch_related(
                    'likes', 'reviewcomment_set', 'movie', 'user'),
                id=review_id)
            serializer = ReviewSerializer(review, context={'request': request})
            return Response({"review": serializer.data}, status=status.HTTP_200_OK)

        reviews = Review.objects.all().prefetch_related(
            'likes', 'reviewcomment_set', 'movie', 'user')
        serializer = ReviewSerializer(
            reviews, many=True, context={'request': request})
        return Response(data={"review": serializer.data}, status=status.HTTP_200_OK)

    @extend_schema(
        summary="리뷰 작성",
        description="새로운 리뷰를 작성 동일한 영화에 대한 중복 리뷰는 허용되지 않음",
        request=ReviewSerializer,
        responses={
            201: OpenApiResponse(
                response=ReviewSerializer,
                description="작성된 리뷰"
            ),
            400: OpenApiResponse(description="잘못된 요청 또는 중복된 리뷰"),
        },
    )
    def post(self, request):
        movie_id = request.data.get('movie')
        if Review.objects.filter(user=request.user, movie_id=movie_id).exists():
            return Response({'message': '작성한 리뷰가 이미 있습니다.'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = ReviewSerializer(data=request.data, context={
                                      'request': request})  # context 전달
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="리뷰 좋아요 상태 변경",
        description="리뷰의 좋아요 상태를 토글. 이미 좋아요를 누른 경우 취소하고, 좋아요를 누르지 않은 경우 추가",
        request=None,
        responses={
            200: OpenApiResponse(
                description="좋아요 상태 변경 성공",
                examples={
                    "liked": True,
                    "likes_count": 10
                },
            ),
            400: OpenApiResponse(description="리뷰 ID가 제공되지 않았습니다."),
            404: OpenApiResponse(description="리뷰를 찾을 수 없습니다."),
        },
    )
    # 좋아요 기능
    def patch(self, request, review_id):
        print(f"현재 사용자: {request.user}, 인증 여부: {request.user.is_authenticated}")
        if not review_id:
            return Response({'error': '리뷰 아이디가 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)
        review = get_object_or_404(Review, id=review_id)
        is_liked = review.likes.filter(id=request.user.id).exists()
        if is_liked:
            review.likes.remove(request.user)
        else:
            review.likes.add(request.user)
        return Response({
            'message': '좋아요 상태 변경 성공',
            'is_liked': review.likes.filter(id=request.user.id).exists(),
            'likes_count': review.likes.count(),
        }, status=status.HTTP_200_OK)

    @extend_schema(
        summary="리뷰 수정",
        description="리뷰 내용을 수정. 리뷰 작성자만 수정할 수 있음",
        request=ReviewSerializer,
        responses={
            200: OpenApiResponse(
                response=ReviewSerializer,
                description="수정된 리뷰"
            ),
            403: OpenApiResponse(description="수정 권한이 없습니다."),
            404: OpenApiResponse(description="리뷰를 찾을 수 없습니다."),
        },
    )
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

    @extend_schema(
        summary="리뷰 삭제",
        description="리뷰를 삭제. 리뷰 작성자만 삭제할 수 있음",
        parameters=[
            OpenApiParameter(
                name="review_id",
                type=int,
                description="삭제할 리뷰의 ID",
                required=True
            )
        ],
        responses={
            204: OpenApiResponse(description="리뷰 삭제 성공"),
            403: OpenApiResponse(description="삭제 권한이 없습니다."),
            404: OpenApiResponse(description="리뷰를 찾을 수 없습니다."),
        },
    )
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
    permission_classes = [AllowAny]

    @extend_schema(
        summary="리뷰 댓글 작성",
        description="특정 리뷰에 댓글을 작성",
        parameters=[
            OpenApiParameter(
                name="review_id",
                type=int,
                description="댓글을 작성할 리뷰의 ID",
                required=True
            )
        ],
        request=ReviewCommentSerializer,
        responses={
            201: OpenApiResponse(
                response=ReviewCommentSerializer,
                description="작성된 댓글"
            ),
            400: OpenApiResponse(description="잘못된 요청 데이터"),
            404: OpenApiResponse(description="리뷰를 찾을 수 없습니다."),
        },
    )
    def post(self, request, review_id):
        review = get_object_or_404(Review, id=review_id)

        serializer = ReviewCommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, review=review)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="리뷰 댓글 조회",
        description="특정 리뷰에 작성된 모든 댓글을 조회",
        parameters=[
            OpenApiParameter(
                name="review_id",
                type=int,
                description="댓글을 조회할 리뷰의 ID",
                required=True
            )
        ],
        responses={
            200: OpenApiResponse(
                response=ReviewCommentSerializer(many=True),
                description="리뷰에 작성된 댓글 목록"
            ),
            404: OpenApiResponse(description="리뷰를 찾을 수 없습니다."),
        },
    )
    def get(self, request, review_id):
        review = get_object_or_404(Review, id=review_id)
        comments = ReviewComment.objects.filter(review=review)
        serializer = ReviewCommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="리뷰 댓글 수정",
        description="작성된 리뷰 댓글을 수정. 댓글 작성자만 수정할 수 있음",
        parameters=[
            OpenApiParameter(
                name="comment_id",
                type=int,
                description="수정할 댓글의 ID",
                required=True
            )
        ],
        request=ReviewCommentSerializer,
        responses={
            200: OpenApiResponse(
                response=ReviewCommentSerializer,
                description="수정된 댓글"
            ),
            403: OpenApiResponse(description="수정 권한이 없습니다."),
            404: OpenApiResponse(description="댓글을 찾을 수 없습니다."),
        },
    )
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

    @extend_schema(
        summary="리뷰 댓글 삭제",
        description="리뷰 댓글을 삭제. 댓글 작성자만 삭제할 수 있음",
        parameters=[
            OpenApiParameter(
                name="comment_id",
                type=int,
                description="삭제할 댓글의 ID",
                required=True
            )
        ],
        responses={
            204: OpenApiResponse(description="댓글 삭제 성공"),
            403: OpenApiResponse(description="삭제 권한이 없습니다."),
            404: OpenApiResponse(description="댓글을 찾을 수 없습니다."),
        },
    )
    def delete(self, request, comment_id):
        comment = get_object_or_404(ReviewComment, id=comment_id)
        if comment.user != request.user:
            return Response({'error': '삭제 권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)

        comment.delete()
        return Response({'message': '댓글 삭제 성공'}, status=status.HTTP_204_NO_CONTENT)

# 플레이리스트 기능


class PlaylistView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="플레이리스트 생성",
        description="새로운 플레이리스트를 생성 영화는 생성 시 추가하지 않음. 나중에 /update 주소를 통해 추가할 수 있음",
        request=CollectionSerializer,
        responses={
            201: OpenApiResponse(
                response=CollectionSerializer,
                description="생성된 플레이리스트"
            ),
            400: OpenApiResponse(description="잘못된 요청 데이터"),
        },
    )
    def post(self, request):
        serializer = CollectionSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            collection = serializer.save(user=request.user)  # Collection 생성
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="플레이리스트 조회",
        description="사용자의 모든 플레이리스트를 조회하거나 특정 플레이리스트의 상세 정보를 가져옴",
        parameters=[
            OpenApiParameter(
                name="user_id",
                type=int,
                description="플레이리스트를 조회할 사용자 ID",
                required=True
            ),
            OpenApiParameter(
                name="playlist_id",
                type=int,
                description="조회할 특정 플레이리스트 ID (선택 사항)",
                required=False
            ),
        ],
        responses={
            200: OpenApiResponse(
                response=CollectionSerializer(many=True),
                description="플레이리스트 목록 또는 특정 플레이리스트 상세 정보"
            ),
            404: OpenApiResponse(description="플레이리스트를 찾을 수 없습니다."),
        },
    )
    def get(self, request, user_id, playlist_id=None):
        if playlist_id:
            playlist = get_object_or_404(Collection, id=playlist_id)
            serializer = CollectionSerializer(playlist)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            playlists = Collection.objects.filter(user=user_id)
            serializer = CollectionSerializer(playlists, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="플레이리스트 삭제",
        description="특정 플레이리스트를 삭제. 플레이리스트 소유자만 삭제할 수 있음",
        parameters=[
            OpenApiParameter(
                name="playlist_id",
                type=int,
                description="삭제할 플레이리스트 ID",
                required=True
            ),
        ],
        responses={
            204: OpenApiResponse(description="플레이리스트 삭제 성공"),
            403: OpenApiResponse(description="삭제 권한이 없습니다."),
            404: OpenApiResponse(description="플레이리스트를 찾을 수 없습니다."),
        },
    )
    def delete(self, request, playlist_id):
        playlist = get_object_or_404(
            Collection, id=playlist_id, user=request.user)
        playlist.delete()
        return Response({'message': '플레이리스트가 삭제되었습니다.'}, status=status.HTTP_204_NO_CONTENT)

# 플레이리스트 업데이트


class UpdatePlaylistView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="플레이리스트 제목 수정",
        description="플레이리스트의 제목을 수정",
        parameters=[
            OpenApiParameter(name="playlist_id", type=int,
                             description="수정할 플레이리스트 ID"),
        ],
        responses={
            200: OpenApiResponse(description="수정된 플레이리스트 제목"),
            404: OpenApiResponse(description="플레이리스트를 찾을 수 없습니다."),
        },
    )
    def put(self, request, playlist_id):
        playlist = get_object_or_404(
            Collection, id=playlist_id, user=request.user)
        playlist.title = request.data.get('title', playlist.title)
        playlist.save()
        return Response({'message': '제목 수정 완료'}, status=status.HTTP_200_OK)

    @extend_schema(
        summary="플레이리스트에 영화 추가",
        description="플레이리스트에 영화를 추가",
        parameters=[
            OpenApiParameter(name="playlist_id", type=int,
                             description="플레이리스트 ID"),
        ],
        responses={
            200: OpenApiResponse(description="추가된 영화 목록"),
            404: OpenApiResponse(description="플레이리스트를 찾을 수 없습니다."),
        },
    )
    def post(self, request, playlist_id):
        playlist = get_object_or_404(
            Collection, id=playlist_id, user=request.user)
        movie_ids = request.data.get('movies', [])
        movies_to_add = Movie.objects.filter(id__in=movie_ids)
        playlist.movies.add(*movies_to_add)
        return Response({'message': '영화 추가 완료'}, status=status.HTTP_200_OK)

    @extend_schema(
        summary="플레이리스트에서 영화 제거",
        description="플레이리스트에서 영화를 제거",
        parameters=[
            OpenApiParameter(name="playlist_id", type=int,
                             description="플레이리스트 ID"),
        ],
        responses={
            200: OpenApiResponse(description="제거된 영화 목록"),
            404: OpenApiResponse(description="플레이리스트를 찾을 수 없습니다."),
        },
    )
    def delete(self, request, playlist_id):
        playlist = get_object_or_404(
            Collection, id=playlist_id, user=request.user)
        movie_ids = request.data.get('movies', [])
        movies_to_remove = Movie.objects.filter(id__in=movie_ids)
        playlist.movies.remove(*movies_to_remove)
        return Response({'message': '영화 제거 완료'}, status=status.HTTP_200_OK)

class AllReviewView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="모든 리뷰 조회",
        description="등록된 모든 리뷰를 조회합니다.",
        responses={
            200: OpenApiResponse(
                description="리뷰 목록 반환",
                examples={
                    "application/json": [
                        {
                            "id": 1,
                            "content": "영화가 정말 재밌었어요!",
                            "rating": 4.5,
                            "create_review": "2024-11-24T12:34:56",
                            "nickname": "사용자1",
                            "movie": {
                                "id": 101,
                                "title": "영화 제목",
                                "poster_path": "/path_to_poster.jpg"
                            },
                            "is_liked": True,
                            "likes_count": 10
                        },
                        {
                            "id": 2,
                            "content": "별로였어요.",
                            "rating": 2.0,
                            "create_review": "2024-11-23T10:00:00",
                            "nickname": "사용자2",
                            "movie": {
                                "id": 102,
                                "title": "다른 영화 제목",
                                "poster_path": "/path_to_poster2.jpg"
                            },
                            "is_liked": False,
                            "likes_count": 3
                        }
                    ]
                }
            )
        }
    )
    def get(self, request):
        reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    