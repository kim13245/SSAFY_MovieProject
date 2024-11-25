from django.db import models
from django.conf import settings

class Person(models.Model):
    id = models.IntegerField(primary_key=True) # TMDB 인물 ID
    name = models.TextField(max_length=100)  # 이름
    profile_path = models.TextField(max_length=200, null=True, blank=True)  # 프로필 이미지 경로


class Crew(models.Model):
    department = models.CharField(max_length=100)  # 부서 이름
    person = models.ForeignKey('Person', on_delete=models.CASCADE)  # 인물 ID (외래키)


class Cast(models.Model):
    name = models.CharField(max_length=100)  # 배우 이름
    character = models.TextField()  # 배역 이름
    person = models.ForeignKey('Person', on_delete=models.CASCADE)  # 인물 ID (외래키)


class Genre(models.Model):
    id = models.IntegerField(primary_key=True) # TMDB 장르 ID
    name = models.CharField(max_length=100)  # 장르 이름


class Emotion(models.Model):
    name = models.CharField(max_length=100)  # 감정 이름
    genres = models.ManyToManyField('Genre', related_name='emotions')  # 감정과 장르 간의 다대다 관계


class Movie(models.Model):
    id = models.IntegerField(primary_key=True)  # TMDB의 영화 ID를 기본 키로 사용
    title = models.CharField(max_length=100)  # 제목
    belong_to_collection = models.CharField(max_length=100, null=True, blank=True) # 시리즈
    original_title = models.CharField(max_length=100, null=True, blank=True)  # 원제목
    release_date = models.DateField(null=True, blank=True)  # 개봉일
    overview = models.TextField(null=True, blank=True)  # 줄거리
    runtime = models.IntegerField(null=True, blank=True)  # 영화 런타임
    popularity = models.FloatField(null=True, blank=True)  # 인기 점수
    vote_average = models.FloatField(null=True, blank=True)  # 평균 평점
    vote_count = models.IntegerField(default=0)  # 평점 투표 수
    poster_path = models.CharField(max_length=200, null=True, blank=True)  # 포스터 이미지 경로
    backdrop_path = models.CharField(max_length=200, null=True, blank=True)  # 배경 이미지 경로
    budget = models.BigIntegerField(null=True, blank=True)  # 제작비
    revenue = models.BigIntegerField(null=True, blank=True)  # 매출
    adult = models.BooleanField(default=False)  # 성인 영화 여부
    status = models.CharField(max_length=50, null=True, blank=True) # 개봉 상태
    homepage = models.URLField(null=True, blank=True)
    imdb_id = models.CharField(max_length=15, null=True, blank=True) # imdb 아이디
    tagline = models.CharField(max_length=255, null=True, blank=True) # 태그라인
    origin_country = models.CharField(max_length=100, null=True, blank=True) # 제작 국가
    spoken_languages = models.CharField(max_length=100, null=True, blank=True) # 영화 언어
    user_rating = models.FloatField(default=0.0)
    genres = models.ManyToManyField('Genre', related_name='genres')  # 장르 ID
    cast = models.ManyToManyField('Cast', related_name='movies')  # 출연진
    crew = models.ManyToManyField('Crew', related_name='movies')  # 제작진
    trailer = models.CharField(max_length=100, null=True, blank=True) #영화 트레일러

class Community(models.Model):
    title = models.CharField(max_length=255)  # 제목
    content = models.TextField()  # 내용
    movie = models.ForeignKey('movies.Movie', on_delete=models.CASCADE)  # 영화 ID (외래키)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # 사용자 ID (외래키)


class Comment(models.Model):
    community = models.ForeignKey('Community', on_delete=models.CASCADE)  # 커뮤니티 ID (외래키)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # 사용자 ID (외래키)
    content = models.TextField()  # 댓글 내용


class Review(models.Model):
    content = models.TextField()  # 리뷰 내용
    rating = models.FloatField(default=0.0)  # 평점
    create_review = models.DateTimeField(auto_now_add=True)  # 리뷰 작성일
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # 사용자 ID (외래키)
    movie = models.ForeignKey('movies.Movie', on_delete=models.CASCADE)  # 영화 ID (외래키)
    emotion = models.ForeignKey('movies.Emotion', on_delete=models.CASCADE)  # 감정 ID (외래키)
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name = 'liked_reviews',
        blank=True
    )
    @property
    def likes_count(self):
        return self.likes.count()


class ReviewComment(models.Model):
    review = models.ForeignKey('Review', on_delete=models.CASCADE)  # 리뷰 ID (외래키)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # 사용자 ID (외래키)
    content = models.TextField()  # 댓글 내용
    created_at = models.DateTimeField(auto_now_add=True)


class Collection(models.Model):
    # user, movie, title, poster_path, vote_average
    title = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="collections")  # 사용자
    vote_average = models.FloatField(default = 0.0) # 사용자가 담은 플레이리스트들의 평균 평점
    movies = models.ManyToManyField('movies.Movie', related_name="collections")  # 여러 영화를 플레이리스트에 추가 가능
