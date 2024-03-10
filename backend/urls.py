from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from drf_yasg import openapi
from drf_yasg.views import get_schema_view


schema_view = get_schema_view(
    openapi.Info(
        title="ParkVision API",
        default_version="v1",
        description="ParkVision API Documentation",
        terms_of_service="",
        contact=openapi.Contact(email="atharvabhide2020.comp@mmcoe.edu.in"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    authentication_classes=[],
)


class HomeView(APIView):
    def get(self, request):
        return Response({
            'message': 'Welcome to Parkomate Backend Server',
            'endpoints': [
                '/admin/',
                '/api/analytics/',
                '/api/users/',
                '/api/organization/',
                '/api/parking/',
                '/api/vehicle/',
                '/api/analytics/'
            ]
        })


urlpatterns = [
    path("api/", HomeView.as_view()),
    path("admin/", admin.site.urls),
    path("api/", include("users.urls")),
    path("api/", include("organization.urls")),
    path("api/", include("vehicle.urls")),
    path("api/", include("parking.urls")),
    path("api/", include("analytics.urls")),
]

urlpatterns += [
    # Swagger UI
    re_path(
        r'^swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0),
        name='schema-json'
    ),
    path('swagger/', schema_view.with_ui('swagger',
         cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc',
         cache_timeout=0), name='schema-redoc'),
]
