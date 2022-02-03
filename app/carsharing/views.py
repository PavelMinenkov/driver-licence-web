from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader
from django.conf import settings

import sirius_sdk

from main.helpers import BrowserSession, build_websocket_url
from main.authorization import auth, save_driver_license
from carsharing.forms import CarRentalForm
from carsharing.ssi import check_driver_license, issue_confirmation


async def index(request):

    async with sirius_sdk.context(**settings.RENT_A_CAR['SDK']):
        browser_session = BrowserSession(request, cookie_path=reverse('carsharing-index'))
        connection_key = await browser_session.get_connection_key()
        if not connection_key:
            connection_key = await browser_session.create_connection_key()
        qr_url = await browser_session.get_qr_code_url("Rent a car")

        user = await auth(connection_key)
        driver_license = user.driver_license if user else None

        if request.method == 'POST':
            form = CarRentalForm(request.POST)
            if form.is_valid():
                values = {
                    "pick_up_date": form.cleaned_data['pick_up_date'],
                    "drop_off_date": form.cleaned_data['drop_off_date']
                }
                if driver_license:
                    values["last_name"] = driver_license["last_name"]
                    values["first_name"] = driver_license["first_name"]
                pw = await sirius_sdk.PairwiseList.load_for_verkey(user.verkey)
                await issue_confirmation(connection_key, pw, values)

        template = loader.get_template('index.carsharing.html')
        context = {
            'title': 'CarSharing',
            'qr_url': qr_url,
            'is_authorized': False,
            'ws_url': build_websocket_url(request, path=f'/qr/{connection_key}'),
            'auth': await browser_session.auth(),
        }
        if driver_license:
            context["last_name"] = driver_license["last_name"]
            context["first_name"] = driver_license["first_name"]
        response = HttpResponse(template.render(context, request))
        await browser_session.set_connection_key(response)
        return response


async def logout(request):
    async with sirius_sdk.context(**settings.RENT_A_CAR['SDK']):
        browser_session = BrowserSession(request, cookie_path=reverse('carsharing-index'))
        response = HttpResponseRedirect(redirect_to=reverse('carsharing-index'))
        await browser_session.logout(response)
        return response


async def request_driver_license(request):
    async with sirius_sdk.context(**settings.RENT_A_CAR['SDK']):
        browser_session = BrowserSession(request, cookie_path=reverse('carsharing-index'))
        conn_key = await browser_session.get_connection_key()
        user = await auth(conn_key)
        pw = await sirius_sdk.PairwiseList.load_for_verkey(user.verkey)
        ok, drive_lic_attrs = await check_driver_license(conn_key, pw)
        if ok:
            await save_driver_license(await browser_session.get_connection_key(), drive_lic_attrs)
        response = HttpResponseRedirect(redirect_to=reverse('carsharing-index'))
        return response
