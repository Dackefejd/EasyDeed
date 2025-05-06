from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.db.models import SET

# Create your models here.


# Returns the default user 'Eddy' which is used as a fallback if the original user (e.g. the creator of a DataPreset) has been deleted. Eddy represents the EasyDeed system user.
def get_eddy_user():
    return get_user_model().objects.get(username='Eddy')

class DataPreset(models.Model):
    user = models.ForeignKey(User, on_delete=SET(get_eddy_user), null=True, blank=True)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    
    def __str__(self):
        return f'{self.name} Owner: {self.user} | Created: {self.created.strftime("%Y-%m-%d")} | Updated: {self.updated.strftime("%Y-%m-%d")}'
    


class TransformationStep(models.Model):
    preset = models.ForeignKey(DataPreset, related_name='steps', on_delete=models.CASCADE)
    step_type = models.CharField(max_length=100)
    config = models.JSONField()
    order = models.IntegerField()

    def __str__(self):
        return self.step_type