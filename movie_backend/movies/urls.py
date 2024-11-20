from django.urls import path
from . import views

urlpatterns = [
    path('movie_list/', views.MovieListView.as_view(), name='movie_list'),
    path('movie_detail/<int:movie_id>/', views.MovieDetailView.as_view(), name='movie_detail'),
    path('movie_search/', views.MovieSearchView.as_view(), name='movie_search'),
    path('emotion/<str:emotion>', views.SelectedEmotionView.as_view(), name='emotion'),
]
