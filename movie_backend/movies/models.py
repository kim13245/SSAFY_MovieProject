from django.db import models
from accounts.models import User


class Person(models.Model):
    id = models.IntegerField(primary_key=True) # TMDB 인물 ID
    name = models.TextField(max_length=100)  # 이름
    # biography = models.TextField(null=True, blank=True)  # 인물 소개
    # birthday = models.DateField(null=True, blank=True)  # 출생일
    # deathday = models.DateField(null=True, blank=True)  # 사망일(옵션)
    profile_path = models.TextField(max_length=200, null=True, blank=True)  # 프로필 이미지 경로


class Crew(models.Model):
    department = models.CharField(max_length=100)  # 부서 이름
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE, related_name='crews')  # 영화 ID (외래키)
    person = models.ForeignKey('Person', on_delete=models.CASCADE)  # 인물 ID (외래키)


class Cast(models.Model):
    name = models.CharField(max_length=100)  # 배우 이름
    character = models.TextField()  # 배역 이름
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE, related_name='casts')  # 영화 ID (외래키)
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
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)  # 장르 ID
    cast = models.ManyToManyField('Cast', related_name='movies')  # 출연진
    crew = models.ManyToManyField('Crew', related_name='movies')  # 제작진
