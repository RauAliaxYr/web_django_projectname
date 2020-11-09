from django.db import models

from django.db import models
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)


class Event(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.TextField(max_length=100)
    text = models.TextField(max_length=400)
    image = models.ImageField()
    date = models.DateField()
    location = models.TextField()
