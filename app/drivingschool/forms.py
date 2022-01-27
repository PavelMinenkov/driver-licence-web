from django import forms


class DrivingSchoolDiplomaForm(forms.Form):
    issue_date = forms.DateField()
    categories = forms.CharField()
