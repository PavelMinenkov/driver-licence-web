import asyncio
import logging
from time import sleep

import sirius_sdk
from ilock import ILock
from django.conf import settings
from django.core.management.base import BaseCommand

from main.ssi.custom import run


class Command(BaseCommand):

    help = 'Run Driving School SSI logic'

    def handle(self, *args, **options):
        with ILock('DrivingSchoolLock'):
            print('********************************************')
            print(self.help)
            print('********************************************')
            sirius_sdk.init(**settings.DRIVING_SCHOOL['SDK'])
            while True:
                try:
                    asyncio.get_event_loop().run_until_complete(
                        run(
                            me=sirius_sdk.Pairwise.Me(
                                did=settings.DRIVING_SCHOOL['DID'],
                                verkey=settings.DRIVING_SCHOOL['VERKEY']
                            )
                        )
                    )
                except Exception as e:
                    logging.error(str(e))
                print('Driving School: reconnect to cloud agent...')
                sleep(3)
