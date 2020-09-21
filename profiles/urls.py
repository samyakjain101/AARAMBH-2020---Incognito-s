from django.urls import path
from .views import *
from django.contrib.auth.views import LoginView, LogoutView
app_name = 'profiles'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('register/',anonymous_required(UserRegistration.as_view()),name="register"),
    path('login/', anonymous_required(LoginView.as_view(template_name='profiles/login.html')), name='login'),
    path('logout/', login_required(LogoutView.as_view()), name='logout'),
    path('profile/', login_required(ProfileView.as_view()),name='profile_detail'),
    path('profile/edit/', login_required(EditProfile.as_view()),name='profile_edit'),
    path('profile/<str:username>', ProfileDetailView.as_view(), name='profile_global'),
    path('search/', search,name="search"),
]
