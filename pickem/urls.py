from django.contrib import admin
from django.urls import path, include
from django.conf import settings


urlpatterns = [
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/', include('base.urls')),
    path('admin/', admin.site.urls),
]
