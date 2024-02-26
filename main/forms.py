from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

ALLOWED_FILE_SIZE_MB = 128
def validate_file_size(value):
    limit = ALLOWED_FILE_SIZE_MB * 1000 * 1000
    if value.size > limit:
        raise ValidationError(f"File too large. Size should not exceed {ALLOWED_FILE_SIZE_MB}MB.")

class UploadForm(forms.Form):
    zip_file = forms.FileField(
        widget=forms.FileInput(attrs={'required': True, 'class': 'zip_file', 'accept': '.zip', 'id': 'zip-file'}),
        validators=[
            validate_file_size
        ]
    )
    cloud_name = forms.CharField(widget=forms.TextInput(attrs={'required': True}))
    api_key = forms.CharField(widget=forms.TextInput(attrs={'required': True}))
    api_secret = forms.CharField(widget=forms.PasswordInput(attrs={'required': True}))
