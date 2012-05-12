
from django.db import models


class Profile(models.Model):
    user = models.ForeignKey("auth.User")
    bio = models.TextField()
