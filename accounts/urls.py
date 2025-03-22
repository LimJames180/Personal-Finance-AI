from django.urls import path
from .views import register, user_login, user_logout, home, logged_out,login_redirect, change_password, change_username

urlpatterns = [
    path('', home, name='home'),
    path('', login_redirect, name='login_redirect'),

    path('', login_redirect, name='login_redirect'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('logged-out/', logged_out, name='logged_out'),
    # Other URLs
    path('change-username/', change_username, name='change_username'),
    path('change-password/', change_password, name='change_password'),

]
