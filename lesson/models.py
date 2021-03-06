from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
from django.urls import reverse



# Create your models here.

class Material(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=255, unique_for_date='publish')

    body = models.TextField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_materials')

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

    def get_absolute_url(self):
        return reverse('lesson:detailed_material',
                       args=[
                           self.publish.year,
                           self.publish.month,
                           self.publish.day,
                           self.slug])

class Comment(models.Model):
    material = models.ForeignKey(Material,
                                 on_delete=models.CASCADE,
                                 related_name='comments')
    name = models.CharField(max_length=250)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    birth = models.DateField(null=True, blank=True)
    photo = models.ImageField(upload_to="User/%Y/%m/%d", blank=True)




