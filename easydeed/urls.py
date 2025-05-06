from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('', include('base.urls')),
    path('', include('dataprep.urls')),
    path('admin/', admin.site.urls),
]
