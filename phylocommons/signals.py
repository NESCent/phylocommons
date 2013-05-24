def create_profile(sender, instance, signal, created, **kwargs):
    """When user is created also create a matching profile."""
 
    from phylocommons.models import UserProfile
 
    if created:
        UserProfile(user = instance).save()
