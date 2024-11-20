from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from .models import Movie, Cast, Crew, Emotion, Genre, Person
from .serilalizers import MovieDetailSerializer, MovieListSerializer

from django.shortcuts import get_list_or_404, get_object_or_404

# Create your views here.

@api_view(['GET'])
def movie_list(request):
    movies = get_list_or_404(Movie)
    serializer = MovieListSerializer(movies, many=True)
    return Response(serializer.data)

class MovieListView(APIView):
    def get(self, request):
        movies = get_list_or_404(Movie)
        serializer = MovieListSerializer(movies, many=True)
        return Response(serializer.data)

class MovieDetailView(APIView):
    def get(self, request, movie_id):
        movie = get_object_or_404(Movie, id=movie_id)
        serializer = MovieDetailSerializer(movie)
        return Response(serializer.data)