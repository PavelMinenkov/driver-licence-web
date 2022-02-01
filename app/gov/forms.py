from django import forms


class PassportForm(forms.Form):
    last_name = forms.CharField()
    first_name = forms.CharField()
    birthday = forms.DateField()
    place_of_birth = forms.CharField()
    issue_date = forms.DateField()
    expiry_date = forms.DateField()
    photo = forms.FileField(required=False)