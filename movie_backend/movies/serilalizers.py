from rest_framework import serializers
from .models import Movie, Cast, Crew, Emotion, Genre, Person, Review 

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

    class Meta:
        model = Review
        fields = ('id', 'content', 'rationg', 'create_review', 'user', 'movie', 'emotion')
        read_only_fields = ('id', 'create_review', 'user')
    