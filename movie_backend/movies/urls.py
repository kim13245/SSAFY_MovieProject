from django.urls import path
from . import views
from accounts.views import UserKeepMovieView
urlpatterns = [
    path('movie_list/', views.MovieListView.as_view(), name='movie_list'),
    path('movie_detail/<int:movie_id>/', views.MovieDetailView.as_view(), name='movie_detail'),
    path('movie_search/', views.MovieSearchView.as_view(), name='movie_search'),
    path('emotion/<str:emotion>', views.SelectedEmotionView.as_view(), name='emotion'),
    path('reviews/', views.ReviewView.as_view(), name='reviews'),
    path('reviews/<int:review_id>/', views.ReviewView.as_view(), name='review_detail'),
    path('reviews/<int:review_id>/comments/', views.ReviewCommentView.as_view(), name='review_comment'),
    path('comments/<int:comment_id>/', views.ReviewCommentView.as_view(), name='comment_detail'),
    path('playlists/<int:playlist_id>/update/', views.UpdatePlaylistView.as_view(), name='playlist_update'),
    path('keep/<int:movie_id>/', UserKeepMovieView.as_view(), name='keep_movie'),

]
