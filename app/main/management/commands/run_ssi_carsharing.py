import asyncio

import sirius_sdk
from django.conf import settings
from django.core.management.base import BaseCommand

from main.ssi.custom import run


class Command(BaseCommand):

    help = 'Run CarSharing SSI logic'

    def handle(self, *args, **options):
        print(self.help)
        sirius_sdk.init(**settings.RENT_A_CAR['SDK'])
        asyncio.get_event_loop().run_until_complete(
            run(
                me=sirius_sdk.Pairwise.Me(
                    did=settings.RENT_A_CAR['DID'],
                    verkey=settings.RENT_A_CAR['VERKEY']
                )
            )
        )
