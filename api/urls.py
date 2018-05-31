from rest_framework.routers import SimpleRouter
from django.urls import path

from .views import UserSignup, user_auth


router = SimpleRouter()

urlpatterns = [
    path('users/signup', UserSignup.as_view(), name='signup'),
    path('users/login', user_auth, name='login')
]

urlpatterns += router.urls
