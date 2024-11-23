from rest_framework import serializers
from .models import Movie, Cast, Crew, Emotion, Genre, Person, Review, ReviewComment, Collection

class MovieListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('id', 'title', 'poster_path',)


class MovieDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    likes_count = serializers.ReadOnlyField()   # @property 처리
    is_liked = serializers.SerializerMethodField()
    nickname = serializers.CharField(source='user.nickname', read_only=True)  # user의 nickname 추가
    movie_title = serializers.CharField(source='movie.title', read_only=True)
    poster_path = serializers.CharField(source='movie.poster_path', read_only=True)# 연관된 영화의 포스터 경로

    class Meta:
        model = Review
        fields = ('id', 'content', 'rating', 'likes_count', 'is_liked','create_review','nickname', 'user', 'movie', 'emotion', 'poster_path', 'movie_title')
        read_only_fields = ('id', 'create_review', 'user', 'is_liked')
    
    def get_is_liked(self, obj):
        request = self.context.get('request', None)
        print(self.context)
        if request and hasattr(request, 'user'):
            user = request.user
            return obj.likes.filter(id=user.id).exists()
        return False

class ReviewCommentSerializer(serializers.ModelSerializer):
    nickname = serializers.CharField(source='user.nickname', read_only=True)  # user의 nickname 추가
    movie_title = serializers.CharField(source='review.movie.title', read_only=True)
    poster_path = serializers.CharField(source='review.movie.poster_path', read_only=True)# 연관된 영화의 포스터 경로
    class Meta:
        model = ReviewComment
        fields = ('id', 'review', 'user', 'content', 'created_at', 'nickname', 'movie_title', 'poster_path')
        read_only_fields = ('id', 'user', 'created_at', 'review',)
    
    def validate_content(self, value):
        if not value.strip():
            raise serializers.ValidationError("댓글 내용은 비어 있을 수 없습니다.")
        return value

class CollectionSerializer(serializers.ModelSerializer):
    movies = MovieListSerializer(many=True, read_only=True) 
    class Meta:
        model = Collection
        fields = ('id', 'title', 'vote_average', 'movies')