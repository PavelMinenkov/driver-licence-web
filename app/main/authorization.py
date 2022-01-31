from dataclasses import dataclass
from typing import Optional

import sirius_sdk
from django.conf import settings

from main.memcached import Memcached


@dataclass
class User:
    did: str
    verkey: str
    label: str
    driver_license: dict = None


AUTH_NAMESPACE = 'auth-driver-licence'


async def login(connection_key: str, p2p: sirius_sdk.Pairwise) -> User:
    kwargs = {
        'did': p2p.their.did,
        'verkey': p2p.their.verkey,
        'label': p2p.their.label
    }
    await Memcached.set(
        key=connection_key,
        value=kwargs,
        exp_time=settings.AUTH_LIVE_SECS,
        namespace=AUTH_NAMESPACE
    )
    return User(**kwargs)


async def auth(connection_key: str) -> Optional[User]:
    kwargs = await Memcached.get(
        key=connection_key,
        namespace=AUTH_NAMESPACE
    )
    if kwargs:
        # Update expiration
        await Memcached.touch(
            key=connection_key,
            exp_time=settings.AUTH_LIVE_SECS,
            namespace=AUTH_NAMESPACE
        )
        return User(**kwargs)
    else:
        return None


async def save_driver_license(connection_key: str, driver_license: dict):
    kwargs = await Memcached.get(
        key=connection_key,
        namespace=AUTH_NAMESPACE
    )
    if kwargs:
        kwargs["driver_license"] = driver_license
        await Memcached.set(
            key=connection_key,
            value=kwargs,
            exp_time=settings.AUTH_LIVE_SECS,
            namespace=AUTH_NAMESPACE
        )


async def logout(connection_key: str):
    await Memcached.delete(
        key=connection_key,
        namespace=AUTH_NAMESPACE
    )
