from rest_framework.routers import SimpleRouter
from django.urls import path

from .views import UserSignup, user_auth, api_index


router = SimpleRouter()

urlpatterns = [
    path('users/signup', UserSignup.as_view(), name='signup'),
    path('users/login', user_auth, name='login'),
    path('', api_index, name='api_index')
]

urlpatterns += router.urls
