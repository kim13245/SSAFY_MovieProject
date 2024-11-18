import time
from django.core.management.base import BaseCommand
from movies.models import Genre, Movie
from movies.get_data import get_genres, get_movies_by_genre, get_movie_details


class Command(BaseCommand):
    help = "TMDB에서 장르별로 10개의 영화를 가져와 Movie 테이블을 채움"

    def handle(self, *args, **kwargs):
        self.stdout.write("TMDB에서 장르 데이터를 가져오는 중...")
        
        # 1. 장르 데이터를 가져와 DB에 저장
        genres = get_genres()
        for genre in genres:
            Genre.objects.get_or_create(
                id=genre['id'], 
                defaults={'name': genre['name']}
            )
        
        # 2. 장르별 영화 데이터 가져오기
        self.stdout.write("장르별로 영화를 가져오는 중...")
        for genre in Genre.objects.all():
            self.stdout.write(f"장르: {genre.name} ({genre.id})")

            # 장르별로 최대 20개의 영화 가져오기
            movies_data = get_movies_by_genre(genre_id=genre.id, page=1)
            movies_to_fetch = movies_data

            for movie_data in movies_to_fetch:
                movie_id = movie_data['id']

                # 3. 영화 상세 정보 가져오기 (디테일 요청)
                time.sleep(1.5)  # 요청 간 대기 시간을 설정해 TMDB 요청 제한을 피함
                movie_details = get_movie_details(movie_id)

                # 4. Movie 테이블에 저장
                Movie.objects.update_or_create(
                    id=movie_id,  # TMDB의 영화 ID를 사용
                    defaults={
                        'title': movie_details['title'],
                        'original_title': movie_details.get('original_title'),
                        'release_date': movie_details.get('release_date'),
                        'overview': movie_details.get('overview'),
                        'runtime': movie_details.get('runtime'),
                        'popularity': movie_details.get('popularity'),
                        'vote_average': movie_details.get('vote_average'),
                        'vote_count': movie_details.get('vote_count'),
                        'poster_path': movie_details.get('poster_path'),
                        'backdrop_path': movie_details.get('backdrop_path'),
                        'budget': movie_details.get('budget', 0),
                        'revenue': movie_details.get('revenue', 0),
                        'adult': movie_details.get('adult', False),
                        'genre': genre,  # 연결된 장르
                    }
                )

        self.stdout.write("모든 영화 데이터를 성공적으로 저장했습니다!")
