from rest_framework import serializers
from .models import Movie, Cast, Crew, Emotion, Genre, Person 

class MovieListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('id', 'title', 'poster_path',)

class CastSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cast
        fields = ('name', 'character')

class MovieDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

