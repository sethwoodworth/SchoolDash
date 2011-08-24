from django.db import models
from userena.models import UserenaBaseProfile

class UserProfile(UserenaBaseProfile):
    # Associate a user with a homeroom in userload.demographics.homeroom
    # TODO: This should be a foreign key from here and demographics to a 'class' table
    homeroom = models.TextField(blank=True)
