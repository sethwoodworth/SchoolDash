from django.db import models
from django.contrib.auth.models import User

from userena.models import UserenaBaseProfile

class UserProfile(UserenaBaseProfile):
    # Associate a user with a homeroom in userload.demographics.homeroom
    # TODO: This should be a foreign key from here and demographics to a 'class' table
    user = models.OneToOneField(User, primary_key=True)
    homeroom  = models.TextField(blank=True)
