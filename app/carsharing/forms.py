from django import forms


class CarRentalForm(forms.Form):
    pick_up_date = forms.DateField()
    drop_off_date = forms.DateField()
