from datetime import datetime

from django.http import HttpResponse
from django.template import loader


async def index(request):
    template = loader.get_template('index.html')
    # Websocket URL builder
    host = request.headers.get('host', 'localhost')
    scheme = 'ws' if request.scheme == 'http' else 'wss'
    context = {
        'ws_url': f'{scheme}://{host}/qr-notification'
    }
    return HttpResponse(template.render(context, request))


async def check_health(request):
    now = datetime.utcnow()
    msg = 'utc: ' + str(now)
    return HttpResponse(msg.encode())
