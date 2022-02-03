from django import forms


class IssueDriverLicenseForm(forms.Form):
    issue_date = forms.DateField()
    photo = forms.FileField()
    expiry_date = forms.DateField()
    place_of_residence = forms.CharField()
