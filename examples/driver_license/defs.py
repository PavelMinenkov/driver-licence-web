import sirius_sdk

DKMS_NAME = 'test_network'

GOV = {
    'SDK': {
        'server_uri': 'https://demo.socialsirius.com',
        'credentials': b'hMPfx0D1ptQa2fK8UPw7p9/Zf/UUEY9Ppk9oU92VO8IUHnc6oP5ov7f9PQ1NLIO5EHcqghOJvRoV7taA/vCd29jfRMZ9/VdiFHKHxS3FdtMT19uY7Os7ERst14ASRcf5',
        'p2p': sirius_sdk.P2PConnection(
            my_keys=('3r8TRFsAZZNjmxFb8Hb5XVuJm7rdttyVcqbhLb6z1ay9', '2z4ED7MskwBrrSgzdcHSzusrqhDajUidrrGXXHrNvzfGoxvDDbM6pXUzKXVB6TSdoaVQUN8sgBn7UbrnfA15dKVD'),
            their_verkey='3x82GoLgC3WZ2nnjYZaqwFnbtaq9kxXEMRf2QHq1bF5G'
        )
    },
    'DID': 'UZ6ULjvZj4Pog7SDrKxXGx',
    'VERKEY': 'G21uvChANhXCxXVe7F9VQeAc6eyt7fZ1hYHHRR3YVNry'
}

RENT_A_CAR = {
    'SDK': {
        'server_uri': 'https://demo.socialsirius.com',
        'credentials': b'hMPfx0D1ptQa2fK8UPw7p9/Zf/UUEY9Ppk9oU92VO8IUHnc6oP5ov7f9PQ1NLIO5EHcqghOJvRoV7taA/vCd28f9cZJym6VMb+wus3RwPeyV1ze+MeCZhLZ+KRJzmdZR',
        'p2p': sirius_sdk.P2PConnection(
            my_keys=('5rzyEdyTkLyeJmMC9VUvEPx4hozkHkB47cXHwmS4T3Cu', '29Yj3tp2ewETQknzt1eZFkt1vn9riA8Abos1VA7E3KAgx1UbsBVknTVvSKrioQsnoJEUV5heqLNuqghHnYcjQuUM'),
            their_verkey='5MwrFLPP91phaEe5QjDAUhj4kmqQHkZszbNksFxqXWSM'
        )
    },
    'DID': '9UVPoNm8fqhWUsnm6mcuGd',
    'VERKEY': '5csxHQdoAyhi5VUeLsv97dtGnueeRRpHpE6XRuF8xGVP'
}
