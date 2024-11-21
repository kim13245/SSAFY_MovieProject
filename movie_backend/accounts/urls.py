from django.urls import path
from . import views
urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),  
    path('signout/', views.SignoutView.as_view(), name='signout'),
    path('profile/<int:user_id>', views.ProfileUserView.as_view(), name='profile'), 
]
