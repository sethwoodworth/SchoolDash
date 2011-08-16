from django.db import models
from userena.models import UserenaBaseProfile

class UserProfile(UserenaBaseProfile):
    fav_color = models.TextField(blank=True)
