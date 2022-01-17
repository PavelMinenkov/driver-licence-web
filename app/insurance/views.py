from django.http import HttpResponse
from django.template import loader


async def index(request):
    template = loader.get_template('index.insurance.html')
    context = {
        'title': 'Insurance'
    }
    return HttpResponse(template.render(context, request))
