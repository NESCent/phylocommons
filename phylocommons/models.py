from django.db import models
from django.contrib.auth.models import User
from phylocommons.signals import create_profile
from django.utils.html import escape
from markdown import markdown


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    profile_text = models.TextField(max_length=5000)
    
    def profile_text_html(self):
        return markdown(self.profile_text, safe_mode=True, enable_attributes=False)
    
    
models.signals.post_save.connect(create_profile, sender=User)
