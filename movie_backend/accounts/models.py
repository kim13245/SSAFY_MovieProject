from django.db import models


class User(models.Model):
    user_email = models.CharField(max_length=100, unique=True)  # 이메일
    user_password = models.CharField(max_length=100)  # 비밀번호
    user_profile = models.CharField(max_length=200, null=True, blank=True)  # 프로필 이미지 경로
    user_intro = models.CharField(max_length=100, null=True, blank=True)  # 사용자 소개
    # 찜한 영화
    kept_movies = models.ManyToManyField('movies.Movie', related_name='kept_by_users')

class Community(models.Model):
    title = models.CharField(max_length=255)  # 제목
    content = models.TextField()  # 내용
    movie = models.ForeignKey('movies.Movie', on_delete=models.CASCADE)  # 영화 ID (외래키)
    user = models.ForeignKey('User', on_delete=models.CASCADE)  # 사용자 ID (외래키)


class Comment(models.Model):
    community = models.ForeignKey('Community', on_delete=models.CASCADE)  # 커뮤니티 ID (외래키)
    user = models.ForeignKey('User', on_delete=models.CASCADE)  # 사용자 ID (외래키)
    content = models.TextField()  # 댓글 내용


class Review(models.Model):
    content = models.TextField()  # 리뷰 내용
    rating = models.FloatField()  # 평점
    create_review = models.DateTimeField(auto_now_add=True)  # 리뷰 작성일
    user = models.ForeignKey('User', on_delete=models.CASCADE)  # 사용자 ID (외래키)
    movie = models.ForeignKey('movies.Movie', on_delete=models.CASCADE)  # 영화 ID (외래키)
    emotion = models.ForeignKey('movies.Emotion', on_delete=models.CASCADE)  # 감정 ID (외래키)
    likes = models.ManyToManyField(
        'User',
        related_name = 'liked_reviews',
        blank=True
    )
    @property
    def likes_count(self):
        return self.likes.count()