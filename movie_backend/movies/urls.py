from django.urls import path
from . import views

urlpatterns = [
    path('movie_list/', views.MovieListView.as_view(), name='movie_list'),
    path('movie_detail/<int:movie_id>/', views.MovieDetailView.as_view(), name='movie_detail'),
    path('movie_search/', views.MovieSearchView.as_view(), name='movie_search'),
    path('emotion/<str:emotion>', views.SelectedEmotionView.as_view(), name='emotion'),\
    path('reviews/', views.ReviewView.as_view(), name='reviews'),
    path('reviews/likes/', views.ReviewView.as_view(), name='review_like'),
    path('reviews/<int:review_id>/', views.ReviewView.as_view()),
    path('reviews/<int:review_id>/comments/', views.ReviewCommentView.as_view(), name='review_comment'),
    path('comments/<int:comment_id>/', views.ReviewCommentView.as_view(), name='comment_detail'),
    path('playlists/', views.PlaylistView.as_view(), name='playlists'),
    path('playlists/<int:playlist_id>/', views.PlaylistView.as_view(), name='playlist_detail'),
]
