from django.db import models
from django.utils.translation import gettext_lazy as _

class roles_choice(models.IntegerChoices):
        ADMIN = 0 , 'Admin'
        GUEST = 1, "Guest"
        AUTHOR = 2, "Author"
        EDITOR = 3, "Editor"
        
