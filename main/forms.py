from django import forms

class UploadForm(forms.Form):
    zip_file = forms.FileField(widget=forms.FileInput(attrs={'required': True, 'class': 'display-none', 'accept': '.zip', 'id': 'zip-file'}))
    cloud_name = forms.CharField(widget=forms.TextInput(attrs={'required': True, 'required': True}))
    api_key = forms.CharField(widget=forms.TextInput(attrs={'required': True}))
    api_secret = forms.CharField(widget=forms.PasswordInput(attrs={'required': True}))