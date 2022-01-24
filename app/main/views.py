from datetime import datetime

from django.conf import settings
from django.http import HttpResponse
from django.template import loader

from .helpers import extract_host, extract_scheme


async def index(request):
    template = loader.get_template('index.html')
    # Websocket URL builder
    host = extract_host(request)
    scheme = extract_scheme(request)
    context = {
        'ws_url': f'{scheme}://{host}/qr/AfNcBeyuPZ5WKbiNQKw9vogzkYQggU8BsaTyAaMDfkQv'
    }
    return HttpResponse(template.render(context, request))


async def check_health(request):
    now = datetime.utcnow()
    msg = 'utc: ' + str(now)
    return HttpResponse(msg.encode())
