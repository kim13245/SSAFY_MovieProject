from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    nickname = models.CharField(max_length=100, default='크와와와왕', null=True) #유저 닉네임
    user_profile = models.CharField(max_length=200, null=True, blank=True)  # 프로필 이미지 경로
    user_intro = models.CharField(max_length=100, null=True, blank=True)  # 사용자 소개
    # 찜한 영화
    kept_movies = models.ManyToManyField('movies.Movie', related_name='kept_by_users')
    followings = models.ManyToManyField('self', symmetrical=False, related_name='followers')  # 팔로우 관계
    