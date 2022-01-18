from datetime import datetime

from django.http import HttpResponse
from django.template import loader


async def index(request):
    template = loader.get_template('index.html')
    context = {}
    return HttpResponse(template.render(context, request))


async def check_health(request):
    now = datetime.utcnow()
    msg = 'utc: ' + str(now)
    return HttpResponse(msg.encode())
