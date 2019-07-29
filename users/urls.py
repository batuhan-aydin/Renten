from django.urls import path, include
from .views import RegistrationView,Login,PasswordResetView,Logout,ProfileDetailView,ProfileUpdateView
app_name = 'users'
urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register' ),
    path('login/', Login.as_view(), name='login' ),
    path('logout/', Logout.as_view(), name='logout'),
    path('reset_password/', PasswordResetView.as_view(), name='reset_password' ),
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='user_profile' ),
    path('profile/me/', ProfileDetailView.as_view(is_me=True), name='me' ),
    path('profile/edit/', ProfileUpdateView.as_view(), name='profile_update' ),
]