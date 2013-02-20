from django import forms
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from treeupload.models import TreeSubmission, TreeSubmissionJob


MAX_UPLOAD_SIZE_MB = 100
MAX_UPLOAD_SIZE = MAX_UPLOAD_SIZE_MB * 1024**2

class TreeSubmissionForm(forms.ModelForm):
    max_upload_size = MAX_UPLOAD_SIZE

    tree_id = forms.RegexField(
        r'^[a-zA-Z][a-zA-Z0-9\_\-]*$', 
        min_length=10, required=True,
        error_message='Tree ID must be at least 10 characters, start with a letter, and contain only letters, numbers, dashes and underscores.'
    )
    
    class Meta:
        model = TreeSubmission
        exclude = ['uploaded_by', 'upload_time']
        
    def clean(self, *args, **kwargs):
        data = super(TreeSubmissionForm, self).clean(*args, **kwargs)
        
        try:
            file = self.cleaned_data['tree_file']
        except:
            raise forms.ValidationError(_('No file selected.'))
        
        if file.size > self.max_upload_size:
            raise forms.ValidationError(_('Please keep filesize under %s. Current filesize %s') % (filesizeformat(self.max_upload_size), filesizeformat(file._size)))
            
        return data
