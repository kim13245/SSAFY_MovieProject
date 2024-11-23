from django.urls import path
from . import views
from movies.views import PlaylistView
urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),  
    path('signout/', views.SignoutView.as_view(), name='signout'),
    path('profile/me/', views.MyProfileView.as_view(), name='my_profile'),
    path('profile/<int:user_id>/', views.UserProfileView.as_view(), name='user_profile'),
    path('profile/<int:user_id>/reviews/', views.UserReviewView.as_view(), name='user_reviews'),
    path('profile/<int:user_id>/reviews/<int:review_id>', views.UserReviewView.as_view(), name='review_delete'),
    path('profile/<int:user_id>/rcomments/', views.UserReviewCommentView.as_view(), name='user_rcomments'),
    path('profile/<int:user_id>/movies/', views.UserMovieView.as_view(), name='user_moviess'),
    path('users/<int:user_id>/follow', views.UserFollowView.as_view(), name='follow'),
    path('profile/<int:user_id>/playlists/', PlaylistView.as_view(), name='user_playlists'),
    path('profile/<int:user_id>/playlists/<int:playlist_id>/', PlaylistView.as_view(), name='playlist_detail'),

]
