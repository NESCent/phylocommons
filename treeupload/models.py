from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.template.defaultfilters import filesizeformat
import Bio.Phylo as bp
from phylocommons import settings
import os


# Create your models here.

class TreeSubmission(models.Model):
    tree_file = models.FileField(
        upload_to=os.path.join(settings.MEDIA_ROOT),
    )
    
    tree_id = models.CharField(max_length=100)
    
    format_choices = sorted(bp._io.supported_formats.keys())
    format_choices = [(x,x) for x in format_choices]
    format = models.CharField(choices=format_choices, default='newick',
                              max_length=20)
    
    uploaded_by = models.ForeignKey(User, related_name='uploaded_by')
    upload_time = models.DateTimeField(auto_now_add=True)

    doi = models.CharField(max_length=100)
    
    def tree_file_name(self):
        return os.path.split(self.tree_file.name)[1]
        
    def tree_file_size(self):
        return filesizeformat(self.tree_file.size)
    
    
class TreeSubmissionJob(models.Model):
    user = models.ForeignKey(User, related_name='user')
    start_time = models.DateTimeField(auto_now_add=True)
    submission = models.ForeignKey(TreeSubmission, related_name='submission')
    status = models.TextField(default='Pending')
