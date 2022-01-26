from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader
from django.conf import settings

import sirius_sdk

from main.helpers import BrowserSession, build_websocket_url
from main.authorization import auth
from carsharing.forms import CarRentalForm
from carsharing.ssi import check_driver_license, issue_confirmation


async def index(request):

    async with sirius_sdk.context(**settings.RENT_A_CAR['SDK']):
        browser_session = BrowserSession(request, cookie_path=reverse('carsharing-index'))
        connection_key = await browser_session.get_connection_key()
        if not connection_key:
            connection_key = await browser_session.create_connection_key()
        qr_url = await browser_session.get_qr_code_url()

        if request.method == 'POST':
            form = CarRentalForm(request.POST)
            if form.is_valid():
                values = {
                    "car_name": form.cleaned_data['car_name'],
                    "pick_up_date": form.cleaned_data['pick_up_date'],
                    "drop_off_date": form.cleaned_data['drop_off_date']
                }
                async with sirius_sdk.context(**settings.RENT_A_CAR['SDK']):
                    conn_key = await browser_session.get_connection_key()
                    user = await auth(conn_key)
                    pw = await sirius_sdk.PairwiseList.load_for_verkey(user.verkey)
                    ok, drive_lic_attrs = await check_driver_license(pw)
                    if ok:
                        values["last_name"] = drive_lic_attrs["last_name"]
                        values["first_name"] = drive_lic_attrs["first_name"]
                        await issue_confirmation(pw, values)

        template = loader.get_template('index.carsharing.html')
        context = {
            'title': 'CarSharing',
            'qr_url': qr_url,
            'is_authorized': False,
            'ws_url': build_websocket_url(request, path=f'/qr/{connection_key}'),
            'auth': await browser_session.auth()
        }
        response = HttpResponse(template.render(context, request))
        await browser_session.set_connection_key(response)
        return response


async def logout(request):
    async with sirius_sdk.context(**settings.RENT_A_CAR['SDK']):
        browser_session = BrowserSession(request, cookie_path=reverse('carsharing-index'))
        response = HttpResponseRedirect(redirect_to=reverse('carsharing-index'))
        await browser_session.logout(response)
        return response
