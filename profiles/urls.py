from django.urls import path
from .views import *
from django.contrib.auth.views import LoginView, LogoutView
app_name = 'profiles'

urlpatterns = [
    # path('', IndexView.as_view(), name='index'),
    path('register/',anonymous_required(UserRegistration.as_view()),name="register"),
    path('login/', anonymous_required(LoginView.as_view(template_name='profiles/login.html')), name='login'),
    path('logout/', login_required(LogoutView.as_view()), name='logout'),
    path('profile/edit/',EditProfile.as_view(),name='profile_edit'),
    path('profile/<str:username>', ProfileDetailView.as_view(), name='profile_main'),
    path('search/', search,name="search"),
    path('ajax/accept_connection_request/', accept_connection_request ,name="accept_connection_request"),
    path('ajax/reject_connection_request/', reject_connection_request ,name="reject_connection_request"),
    path('ajax/send_connection_request/', send_connection_request ,name="send_connection_request"),
]
 