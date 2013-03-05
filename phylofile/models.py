from django.db import models
from django.contrib.auth.models import User
from phylofile.signals import create_profile
from django.utils.html import escape


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    profile_text = models.TextField(max_length=5000)
    
    #def profile_text_html(self):
        #return escape(self.profile_text).replace('\n', '<br/>')
    
    
models.signals.post_save.connect(create_profile, sender=User)
