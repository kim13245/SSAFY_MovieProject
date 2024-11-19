from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Movie, Cast, Crew, Emotion, Genre, Person
from .serilalizers import MovieDetailSerializer, MovieListSerializer

from django.shortcuts import get_list_or_404, get_object_or_404

# Create your views here.

@api_view(['GET'])
def movie_list(request):
    movies = Movie.objects.all()
    serializer = MovieListSerializer(movies, many=True)
    return Response(serializer.data)