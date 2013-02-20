from django.db import models
from django import forms
from django.contrib.auth.models import User
import Bio.Phylo as bp
from phylofile import settings
import os


# Create your models here.

class TreeSubmission(models.Model):
    tree_file = models.FileField(
        upload_to=os.path.join(settings.BASE_DIR, 'uploaded_trees/'),
        verbose_name='Select a file',
        help_text='File should be a properly formatted species list CSV. Max size 50mb.',
    )
    
    tree_id = models.CharField(max_length=100)
    
    format_choices = sorted(bp._io.supported_formats.keys())
    format_choices = [(x,x) for x in format_choices]
    format = models.CharField(choices=format_choices, default='newick',
                              max_length=20)
    
    uploaded_by = models.ForeignKey(User, related_name='uploaded_by')
    upload_time = models.DateTimeField(auto_now_add=True)
    
    
class TreeSubmissionJob(models.Model):
    user = models.ForeignKey(User, related_name='user')
    start_time = models.DateTimeField(auto_now_add=True)
    submission = models.ForeignKey(TreeSubmission, related_name='submission')
    status = models.TextField(default='Pending')
