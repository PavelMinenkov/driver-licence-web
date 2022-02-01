import asyncio
import logging
from time import sleep

import sirius_sdk
from ilock import ILock
from django.conf import settings
from django.core.management.base import BaseCommand

from main.ssi.custom import run


class Command(BaseCommand):

    help = 'Run gov SSI logic'

    def handle(self, *args, **options):
        with ILock('GovLock'):
            print('********************************************')
            print(self.help)
            print('********************************************')
            sirius_sdk.init(**settings.GOV['SDK'])
            while True:
                try:
                    asyncio.get_event_loop().run_until_complete(
                        run(
                            me=sirius_sdk.Pairwise.Me(
                                did=settings.GOV['DID'],
                                verkey=settings.GOV['VERKEY']
                            )
                        )
                    )
                except Exception as e:
                    logging.error(str(e))
                print('Gov: reconnect to cloud agent...')
                sleep(3)
