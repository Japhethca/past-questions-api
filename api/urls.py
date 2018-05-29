from rest_framework.routers import SimpleRouter
from django.urls import path

from .views import index


router = SimpleRouter()

urlpatterns = [
    path('', index, name='index')
]

urlpatterns += router.urls
