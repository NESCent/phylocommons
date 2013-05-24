'''create_profiles.py

Ordinarily, user profiles will be automatically created when user accounts
are created. In some instances, however (such as automatically creating 
superusers through syncdb) this may not work correctly.

This script will create user profiles for all users that don't have one.

run this script with:

    python manage.py shell
    import create_profiles
'''


from django.contrib.auth.models import User
from phylocommons.models import UserProfile
 
users = User.objects.all()
for u in users:
     try:
          p = u.get_profile()
     except:
          UserProfile(user = u).save()