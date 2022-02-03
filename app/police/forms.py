from django import forms


class IssueDriverLicenseForm(forms.Form):
    last_name = forms.CharField()
    first_name = forms.CharField()
    birthday = forms.DateField()
    place_of_birth = forms.CharField()
    issue_date = forms.DateField()
    photo = forms.FileField()
    expiry_date = forms.DateField()
    place_of_residence = forms.CharField()
    categories = forms.CharField()


class VerifyFaceForm(forms.Form):
    source_image = forms.FileField()
    target_image = forms.FileField()
