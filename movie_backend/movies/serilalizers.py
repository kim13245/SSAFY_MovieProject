from rest_framework import serializers
from .models import Movie, Cast, Crew, Emotion, Genre, Person, Review, ReviewComment, Collection
from django.contrib.auth import get_user_model

User = get_user_model()

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
    is_kept = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = ('id', 'title', 'belong_to_collection', 'original_title', 'release_date', 'overview', 'runtime',
                  'popularity', 'vote_average', 'poster_path', 'backdrop_path', 'budget', 'revenue', 'adult', 'status',
                  'homepage', 'imdb_id', 'tagline', 'origin_country', 'spoken_languages', 'user_rating', 'genres', 'cast', 'crew', 'is_kept')

    def get_is_kept(self, obj):
        request = self.context.get('request', None)
        print(request.user)
        if request and request.user.is_authenticated:
            user = User.objects.get(id=request.user.id)
            print('사용자가 찜한 영화들\n', user.kept_movies.all())
            print(f"Checking if user {user.id} has kept the movie {obj.id}")
            return user.kept_movies.filter(id=obj.id).exists()
        return False


class EmotionSerializer(serializers.ModelSerializer):
    genres = serializers.StringRelatedField(many=True)

    class Meta:
        model = Emotion
        fields = ('id', 'name', 'genres')


class ReviewCommentSerializer(serializers.ModelSerializer):
    nickname = serializers.CharField(
        source='user.nickname', read_only=True)  # user의 nickname 추가
    movie = MovieListSerializer(source='review.movie', read_only=True)

    class Meta:
        model = ReviewComment
        fields = ('id', 'review', 'user', 'content',
                  'created_at', 'nickname', 'movie')
        read_only_fields = ('id', 'user', 'created_at', 'review',)

    def validate_content(self, value):
        if not value.strip():
            raise serializers.ValidationError("댓글 내용은 비어 있을 수 없습니다.")
        return value


class ReviewSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()   # @property 처리
    is_liked = serializers.SerializerMethodField()
    nickname = serializers.CharField(
        source='user.nickname', read_only=True)  # user의 nickname 추가
    movie_title = serializers.CharField(source='movie.title', read_only=True)
    poster_path = serializers.CharField(source='movie.poster_path', read_only=True)
    comments = ReviewCommentSerializer(
        many=True, read_only=True, source='comments_set')

    class Meta:
        model = Review
        fields = ('id', 'content', 'rating', 'likes_count', 'is_liked',
                  'create_review', 'nickname', 'user', 'movie', 'movie', 'movie_title',
                  'poster_path', 'emotion', 'comments')
        read_only_fields = ('id', 'create_review', 'user', 'is_liked')

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_is_liked(self, obj):
        print('get_is_liked 호출됨')
        request = self.context.get('request', None)
        print(request.user.is_authenticated)

        if request and hasattr(request, 'user') :
            
            user = request.user
            print(f"User: {user}, Likes: {list(obj.likes.values_list('id', flat=True))}")
            return obj.likes.filter(id=user.id).exists()
        return False


class CollectionSerializer(serializers.ModelSerializer):
    movies = MovieListSerializer(many=True, read_only=True)

    class Meta:
        model = Collection
        fields = ('id', 'title', 'vote_average', 'movies')
        read_only_fields = ('id', 'vote_average',)
