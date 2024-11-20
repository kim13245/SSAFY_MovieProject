from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Movie, Cast, Crew, Emotion, Genre, Person
from .serilalizers import MovieDetailSerializer, MovieListSerializer
from .get_data import get_movie_details, get_cast_crew, serch_movie
from django.shortcuts import get_list_or_404, get_object_or_404, redirect

# Create your views here.


class MovieListView(APIView):
    def get(self, request):
        movies = get_list_or_404(Movie)
        serializer = MovieListSerializer(movies, many=True)
        return Response(serializer.data)

class MovieDetailView(APIView):
    def get(self, request, movie_id):
        movie = Movie.objects.filter(id=movie_id).first()
        if movie:
            serializer = MovieDetailSerializer(movie)
            return Response(serializer.data)
        else:
            new_movie = get_movie_details(movie_id)
            genre_id = new_movie.get('genres')[0].get('id') if new_movie.get('genres') else None
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
            origin_country=new_movie.get('production_countries', [{}])[0].get('iso_3166_1')
                            if new_movie.get('production_countries') else None,
            spoken_languages=new_movie.get('spoken_languages', [{}])[0].get('english_name')
                            if new_movie.get('spoken_languages') else None,
            genre = Genre.objects.get_or_create(id=genre_id)[0] if genre_id else None
            )
        
            credits_data = get_cast_crew(movie_id)
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
                        'movie': movie,
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
                        'movie': movie,
                    }
                )
                # 해당 영화에 제작진 추가
                movie.crew.add(crew)
                
            serializer = MovieDetailSerializer(movie)
            return Response(serializer.data)
        
# class MovieSearchView(APIView):
#     def get(self, request):
#         request.data.title