from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader
from django.conf import settings

import sirius_sdk
import base64

from main.helpers import BrowserSession, build_websocket_url
from main.authorization import auth
from police.forms import IssueDriverLicenseForm
from police.ssi import issue_driver_license


async def index(request):

    async with sirius_sdk.context(**settings.POLICE['SDK']):
        browser_session = BrowserSession(request, cookie_path=reverse('police-index'))
        connection_key = await browser_session.get_connection_key()
        if not connection_key:
            connection_key = await browser_session.create_connection_key()
        qr_url = await browser_session.get_qr_code_url("Police")

        if request.method == 'POST':
            form = IssueDriverLicenseForm(request.POST, request.FILES)
            if form.is_valid():
                values = {
                    "last_name": form.cleaned_data['last_name'],
                    "first_name": form.cleaned_data['first_name'],
                    "birthday": form.cleaned_data['birthday'],
                    "place_of_birth": form.cleaned_data['place_of_birth'],
                    "issue_date": form.cleaned_data['issue_date'],
                    "photo": base64.b64encode(form.cleaned_data['photo'].read()).decode("UTF-8"),
                    "place_of_residence": form.cleaned_data['place_of_residence'],
                    "categories": form.cleaned_data['categories']
                }
                conn_key = await browser_session.get_connection_key()
                user = await auth(conn_key)
                pw = await sirius_sdk.PairwiseList.load_for_verkey(user.verkey)
                await issue_driver_license(conn_key, pw, values, form.cleaned_data['photo'].content_type)

        template = loader.get_template('index.police.html')
        context = {
            'title': 'Police',
            'qr_url': qr_url,
            'ws_url': build_websocket_url(request, path=f'/qr/{connection_key}'),
            'auth': await browser_session.auth()
        }
        response = HttpResponse(template.render(context, request))
        await browser_session.set_connection_key(response)
        return response


async def logout(request):
    async with sirius_sdk.context(**settings.POLICE['SDK']):
        browser_session = BrowserSession(request, cookie_path=reverse('police-index'))
        response = HttpResponseRedirect(redirect_to=reverse('police-index'))
        await browser_session.logout(response)
        return response
