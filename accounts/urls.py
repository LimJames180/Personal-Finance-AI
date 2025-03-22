from django.urls import path
from .views import register, user_login, user_logout, home, logged_out,login_redirect

urlpatterns = [
    path('', home, name='home'),
    path('', login_redirect, name='login_redirect'),

    path('', login_redirect, name='login_redirect'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('logged-out/', logged_out, name='logged_out'),
]
