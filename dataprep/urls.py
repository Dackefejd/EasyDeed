from django.urls import path
from . import views

urlpatterns = [
    path('presets/<slug:slug>/run/', views.run_preset, name="run_preset")
]
