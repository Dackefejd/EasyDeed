from django.contrib import admin
from .models import *
# Register your models here.

apps = [DataPreset, TransformationStep]


admin.site.register(apps)