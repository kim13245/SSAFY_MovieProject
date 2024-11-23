from rest_framework import serializers
from .models import Movie, Cast, Crew, Emotion, Genre, Person, Review, ReviewComment, Collection

class MovieListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Movie
        fields = ('id', 'title', 'poster_path',)

class CastSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cast
        fields = ('id', 'name', 'character')

class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = ('id', 'department', 'person')

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('id', 'name')

class MovieDetailSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True)
    cast = CastSerializer(many=True)
    crew = CrewSerializer(many=True)
    is_kept = serializers.SerializerMethodField()
    
    class Meta:
        model = Movie
        fields = ('id', 'title', 'overview', 'release_date', 'runtime',
                  'poster_path', 'vote_average', 'genres', 'cast', 'crew', 'is_kept')
        
    def get_is_kept(self, obj):
        request = self.context.get('request', None)
        if request and request.user.is_authenticated:
            return obj.kept_by_users.filter(id=request.user.id).exists()
        return False

class EmotionSerializer(serializers.ModelSerializer):
    genres = serializers.StringRelatedField(many=True)
    
    class Meta:
        model = Emotion
        fields = ('id', 'name', 'genres')

class ReviewCommentSerializer(serializers.ModelSerializer):
    nickname = serializers.CharField(source='user.nickname', read_only=True)  # user의 nickname 추가
    movie = MovieListSerializer(source='review.movie', read_only=True)
    class Meta:
        model = ReviewComment
        fields = ('id', 'review', 'user', 'content', 'created_at', 'nickname', 'movie')
        read_only_fields = ('id', 'user', 'created_at', 'review',)
    
    def validate_content(self, value):
        if not value.strip():
            raise serializers.ValidationError("댓글 내용은 비어 있을 수 없습니다.")
        return value

class ReviewSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()   # @property 처리
    is_liked = serializers.SerializerMethodField()
    nickname = serializers.CharField(source='user.nickname', read_only=True)  # user의 nickname 추가
    movie = MovieListSerializer(read_only=True)
    comments = ReviewCommentSerializer(many=True, read_only=True, source='comments_set')
    
    class Meta:
        model = Review
        fields = ('id', 'content', 'rating', 'likes_count', 'is_liked',
                  'create_review','nickname', 'user', 'movie', 'emotion', 'comments')
        read_only_fields = ('id', 'create_review', 'user', 'is_liked')
    
    def get_likes_count(self, obj):
        return obj.likes.count()
    
    def get_is_liked(self, obj):
        request = self.context.get('request', None)
        print(self.context)
        if request and hasattr(request, 'user'):
            user = request.user
            return obj.likes.filter(id=user.id).exists()
        return False

class CollectionSerializer(serializers.ModelSerializer):
    movies = MovieListSerializer(many=True, read_only=True) 
    class Meta:
        model = Collection
        fields = ('id', 'title', 'vote_average', 'movies')
        read_only_fields = ('id', 'vote_average',)