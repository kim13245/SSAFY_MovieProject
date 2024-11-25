import time
from django.core.management.base import BaseCommand
from movies.models import Genre, Movie, Cast, Crew, Person
from movies.get_data import get_genres, get_movie_trailer, get_movies_by_genre, get_movie_details, get_cast_crew

# 다 하고 dumbdata
# python manage.py dumpdata movies --indent 4 > movies_data.json

class Command(BaseCommand):
    # Command(BaseCommand): **커스텀 관리 명령어(Management Command)**를 작성할 때 사용하는 기본 클래스
    # python manage.py 명령어에 새로운 하위 명령어를 추가할 수 있음 ((ex) python manage.py fetch_movies)
    #  Django 프로젝트에서 반복적인 작업, 데이터 관리, 또는 배치 작업을 자동화하려는 경우에 주로 사용됨
    # **주의!!** 파일 구조 Django 프로젝트의 앱 디렉토리 안에 management/commands 디렉토리를 만들어야 커스텀 관리 명령어가 작동됨!!

    # 명령어 설명으로, python manage.py help <command> 실행 시 표시됨
    help = "TMDB에서 장르별로 20개의 영화를 가져와 Movie 테이블을 채움"

    # BaseCommand를 상속받아 커스텀 명령어를 생성하고, handle 메서드를 구현하면 명령어 실행 시 호출됨

    def handle(self, *args, **kwargs):

        # self.stdout.write, self.stderr.write 메서드를 통해 표준 출력/에러 출력을 관리
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
            time.sleep(0.25)
            movies_data = get_movies_by_genre(genre_id=genre.id, page=1)

            for movie_data in movies_data:
                movie_id = movie_data['id']

                # 저장된 영화인지 확인
                if Movie.objects.filter(id=movie_id).exists():
                    self.stdout.write(
                        f"{movie_data['title']}({movie_id})는 이미 저장되어 있습니다.")
                    
                    continue

                # 3-1. 영화 상세 정보 가져오기 (디테일 요청)
                time.sleep(0.25)
                movie_details = get_movie_details(movie_id)

                # 3-2. Movie 테이블에 저장
                movie, created = Movie.objects.update_or_create(
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
                        'status': movie_details.get('status'),
                        'homepage': movie_details.get('homepage'),
                        'imdb_id': movie_details.get('imdb_id'),
                        'tagline': movie_details.get('tagline'),
                        'origin_country': movie_details.get('production_countries', [{}])[0].get('iso_3166_1') 
                                            if movie_details.get('production_countries') else None,
                        'spoken_languages': movie_details.get('spoken_languages', [{}])[0].get('english_name')
                                            if movie_details.get('spoken_languages') else None, 
                    }
                )

                genre_ids = [g['id'] for g in movie_details.get('genres', [])]  # TMDB 장르 ID 가져오기
                for genre_id in genre_ids:
                    try:
                        genre = Genre.objects.get(id=genre_id)
                        movie.genres.add(genre)  # ManyToMany 관계 추가
                    except Genre.DoesNotExist:
                        self.stderr.write(f"장르 ID {genre_id}가 DB에 없습니다.")

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
                # 4. 출연진 목록 가져와서 DB 저장
                time.sleep(0.25)
                credits_data = get_cast_crew(movie_id)

                for cast_data in credits_data.get('cast', []):
                    try:
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
                    except Exception as e:
                        self.stderr.write(f"출연진 데이터 저장 중 오류 발생: {e}")

                for crew_data in credits_data.get('crew', []):
                    try:
                        # 제작진 목록 DB 저장
                        # 위에서 배우들은 DB에 이미 저장되어 있음 -> 감독, 작가 등 DB에 추가
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
                    except Exception as e:
                        self.stderr.write(f"제작진 데이터 저장 중 오류 발생: {e}")

        self.stdout.write("모든 영화 데이터를 성공적으로 저장했습니다!")
