from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.

class Material(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=255)

    body = models.TextField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_matherials')

    publish = models.DateTimeField(default=timezone.now)

    MATERIAL_TYPE = [
        ('theory', 'Theoretical Material'),
        ('practice', 'Practical Task'),
    ]
    material_type = models.CharField(max_length=25,
                                      choices=MATERIAL_TYPE,
                                      default='theory')

    # def __str__(self):
    #     return self.title
