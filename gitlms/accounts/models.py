from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    contact = models.CharField(max_length=15, blank=True, null=True)
    profilepicture = models.ImageField(upload_to='images/profilepictures', blank=True, null=True,default='images/profilepictures/rafid1.jpg')
    role=models.TextField(default='user')
    institute=models.IntegerField(default=-1)
    course=models.IntegerField(default=-1)
    department=models.IntegerField(default=-1)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions_set',
        blank=True
    )

    def __str__(self):
        return self.username  # Adjusted to remove raw password display