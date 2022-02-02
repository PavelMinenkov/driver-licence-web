from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader
from django.conf import settings

import sirius_sdk
import asyncio

from main.helpers import BrowserSession, build_websocket_url
from main.authorization import auth, save_passport
from drivingschool.forms import DrivingSchoolDiplomaForm
from drivingschool.ssi import ask_passport, issue_driving_school_diploma


async def index(request):

    async with sirius_sdk.context(**settings.DRIVING_SCHOOL['SDK']):
        browser_session = BrowserSession(request, cookie_path=reverse('drivingschool-index'))
        connection_key = await browser_session.get_connection_key()
        if not connection_key:
            connection_key = await browser_session.create_connection_key()
        qr_url = await browser_session.get_qr_code_url("Driving school")

        user = await auth(connection_key)
        passport = user.passport if user else None

        if request.method == 'POST':
            form = DrivingSchoolDiplomaForm(request.POST)
            if form.is_valid():
                values = {
                    "issue_date": form.cleaned_data['issue_date'],
                    "categories": form.cleaned_data['categories']
                }
                if passport:
                    values["first_name"] = passport["first_name"]
                    values["last_name"] = passport["last_name"]

                pw = await sirius_sdk.PairwiseList.load_for_verkey(user.verkey)
                await issue_driving_school_diploma(pw, values)

        template = loader.get_template('index.drivingschool.html')
        context = {
            'title': 'Driving school',
            'qr_url': qr_url,
            'is_authorized': False,
            'ws_url': build_websocket_url(request, path=f'/qr/{connection_key}'),
            'auth': await browser_session.auth()
        }
        if passport:
            context["first_name"] = passport["first_name"]
            context["last_name"] = passport["last_name"]
        response = HttpResponse(template.render(context, request))
        await browser_session.set_connection_key(response)
        return response


async def logout(request):
    async with sirius_sdk.context(**settings.DRIVING_SCHOOL['SDK']):
        browser_session = BrowserSession(request, cookie_path=reverse('drivingschool-index'))
        response = HttpResponseRedirect(redirect_to=reverse('drivingschool-index'))
        await browser_session.logout(response)
        return response


async def request_passport(request):
    async with sirius_sdk.context(**settings.DRIVING_SCHOOL['SDK']):
        browser_session = BrowserSession(request, cookie_path=reverse('drivingschool-index'))
        conn_key = await browser_session.get_connection_key()
        user = await auth(conn_key)
        pw = await sirius_sdk.PairwiseList.load_for_verkey(user.verkey)
        ok, drive_lic_attrs = await ask_passport(conn_key, pw)
        if ok:
            await save_passport(await browser_session.get_connection_key(), drive_lic_attrs)

    response = HttpResponseRedirect(redirect_to=reverse('drivingschool-index'))
    return response
