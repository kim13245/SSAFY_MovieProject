from rest_framework import serializers
from .models import Movie, Cast, Crew, Emotion, Genre, Person, Review, ReviewComment 

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

    class Meta:
        model = Review
        fields = ('id', 'content', 'rationg', 'likes_count', 'is_liked','create_review', 'user', 'movie', 'emotion')
        read_only_fields = ('id', 'create_review', 'user', 'is_liked')
    
    def get_is_liked(self, obj):
        user = self.context.get('request').user
        return user in obj.likes.all() if user.is_authenticated else False

class ReviewCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewComment
        fields = ('id', 'review', 'user', 'content', 'created_at')
        read_only_fields = ('id', 'user', 'created_at')
        