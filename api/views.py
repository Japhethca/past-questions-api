from rest_framework.response import Response
from rest_framework import viewsets, views, generics
from django.http import JsonResponse


def index(request):
    return JsonResponse(
        {
            'message': 'Welcome to past questions API'
        }
    )


