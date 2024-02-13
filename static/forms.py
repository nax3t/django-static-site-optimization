from django import forms

classes = 'block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6'

class UploadForm(forms.Form):
    zip_file = forms.FileField(widget=forms.FileInput(attrs={'required': True, 'class':'block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400'}))
    cloud_name = forms.CharField(widget=forms.TextInput(attrs={'required': True, 'required': True, 'class':classes}))
    api_key = forms.CharField(widget=forms.TextInput(attrs={'required': True, 'class':classes}))
    api_secret = forms.CharField(widget=forms.PasswordInput(attrs={'required': True, 'class':classes}))