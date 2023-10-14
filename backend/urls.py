from django.contrib import admin
from django.urls import path, include
from rest_framework.views import APIView
from rest_framework.response import Response

class HomeView(APIView):
    def get(self, request):
        return Response({
            'message': 'Welcome to Parkomate Backend Server',
            'endpoints': [
                '/admin/',
                '/users/',
                '/api/',
                '/parking/'
            ]
        })

urlpatterns = [
    path("", HomeView.as_view()),
    path("admin/", admin.site.urls),
    path("users/", include("users.urls")),
    path("api/", include("api.urls")),
    path("parking/", include("parking.urls")),
]
