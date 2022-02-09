from django import forms


class IssueDriverLicenseForm(forms.Form):
    issue_date = forms.DateField()
    expiry_date = forms.DateField()
    place_of_residence = forms.CharField()


class VerifyFaceForm(forms.Form):
    source_image = forms.FileField()
    target_image = forms.FileField()

