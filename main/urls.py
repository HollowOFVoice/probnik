from django.urls import path

from main.views import login_user, register, home, create_request

urlpatterns = [
    path('', login_user, name='login'),
    path('register/', register, name='register'),
    path('home/',home,name='home'),
    path('request/', create_request, name='request')
]
