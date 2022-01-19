from django.http import HttpResponse
from django.template import loader
from django import forms


class IssueDriverLicenseForm(forms.Form):
    last_name = forms.CharField()
    first_name = forms.CharField()
    birthday = forms.DateField()


async def index(request):
    if request.method == 'POST':
        form = IssueDriverLicenseForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data['first_name'])
    else:
        template = loader.get_template('index.police.html')
        context = {
            'title': 'Police'
        }
        return HttpResponse(template.render(context, request))
