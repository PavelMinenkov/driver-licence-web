from django import forms


class CarRentalForm(forms.Form):
    car_name = forms.CharField()
    pick_up_date = forms.DateField()
    drop_off_date = forms.DateField()
