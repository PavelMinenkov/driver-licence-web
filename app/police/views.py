from django.http import HttpResponse
from django.template import loader
from django.conf import settings

import sirius_sdk

from main.helpers import BrowserSession, build_websocket_url
from police.forms import IssueDriverLicenseForm
from police.ssi import reg_driver_license, issue_driver_license


async def index(request):

    async with sirius_sdk.context(**settings.GOV['SDK']):
        browser_session = BrowserSession(request, cookie_path=request.path)
        connection_key = await browser_session.get_connection_key()
        if not connection_key:
            await browser_session.create_connection_key()
        qr_url = await browser_session.get_qr_code_url()

        if request.method == 'POST':
            form = IssueDriverLicenseForm(request.POST)
            if form.is_valid():
                values = {
                    "last_name": form.cleaned_data['last_name'],
                    "first_name": form.cleaned_data['first_name'],
                    "birthday": form.cleaned_data['birthday'],
                    "place_of_birth": form.cleaned_data['place_of_birth'],
                    "issue_date": form.cleaned_data['issue_date'],
                    # "photo": form.cleaned_data['photo'],
                    "place_of_residence": form.cleaned_data['place_of_residence'],
                    "categories": form.cleaned_data['categories']
                }
                async with sirius_sdk.context(**settings.GOV['SDK']):
                    driver_lic_cred_def, driver_lic_schema = await reg_driver_license()
                    # TODO await issue_driver_license(driver_lic_cred_def, driver_lic_schema, values)

        else:
            pass
        template = loader.get_template('index.police.html')
        context = {
            'title': 'Police',
            'qr_url': qr_url,
            'is_authorized': False,
            'ws_url': build_websocket_url(request, path=f'/qr/{connection_key}')
        }
        response = HttpResponse(template.render(context, request))
        await browser_session.set_connection_key(response)
        return response
