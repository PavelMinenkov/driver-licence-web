from django.http import HttpResponse
from django.template import loader


async def index(request):
    template = loader.get_template('index.police.html')
    context = {
        'title': 'Police'
    }
    return HttpResponse(template.render(context, request))
