from django.urls import path
from rest_framework.views import APIView
from rest_framework.response import Response

class HomeView(APIView):
    def get(self, request):
        return Response({
            'message': 'Welcome to Parkomate Main API',
            'endpoints': [
                '/organizations/',
            ]
        })

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
]