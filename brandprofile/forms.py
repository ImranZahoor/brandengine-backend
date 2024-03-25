from django import forms


class FileUploadForm(forms.Form):
    """
    Form class for uploading files.
    """

    file = forms.FileField()
