import sirius_sdk

DKMS_NAME = 'test_network'

GOV = {
    'SDK': {
        'server_uri': 'https://demo.socialsirius.com',
        'credentials': 'BXXwMmUlw7MTtVWhcVvbSVWbC1GopGXDuo+oY3jHkP/4jN3eTlPDwSwJATJbzwuPAAaULe6HFEP5V57H6HWNqYL4YtzWCkW2w+H7fLgrfTLaBtnD7/P6c5TDbBvGucOV'.encode(),
        'p2p': sirius_sdk.P2PConnection(
            my_keys=('EzJKT2Q6Cw8pwy34xPa9m2qPCSvrMmCutaq1pPGBQNCn', '273BEpAM8chzfMBDSZXKhRMPPoaPRWRDtdMmNoKLmJUU6jvm8Nu8caa7dEdcsvKpCTHmipieSsatR4aMb1E8hQAa'),
            their_verkey='342Bm3Eq9ruYfvHVtLxiBLLFj54Tq6p8Msggt7HiWxBt'
        )
    },
    'DID': 'X1YdguoHBaY1udFQMbbKKG',
    'VERKEY': 'HMf57wiWK1FhtzLbm76o37tEMJvaCbWfGsaUzCZVZwnT'
}

RENT_A_CAR = {
    'SDK': {
        'server_uri': 'https://demo.socialsirius.com',
        'credentials': b'hMPfx0D1ptQa2fK8UPw7p9/Zf/UUEY9Ppk9oU92VO8IUHnc6oP5ov7f9PQ1NLIO5EHcqghOJvRoV7taA/vCd27dfNDKGk1lHqBCjpgHwwotACFHXe3JwIxBUoVBFOMW0',
        'p2p': sirius_sdk.P2PConnection(
                my_keys=('4MnPFkkZ3NWZ2vRq5U3mQhZPkGw6y1DQCzynd4kyYtUw', '24gsMTc77ZHoGFCbQrTEEgTGFSZkK6WhUZKJySC19QswJ1mPZKSZnH9ohzn686UYBD9fj5TCAzxUiwzYhamk64Hu'),
                their_verkey='31qXP2rhZPMXvZTm1PrdvBNrmSdxxTNxVNgmKMAuPKJ3'
            )
    },
    'DID': 'Jj9FsbrRkcrPrB4PFZFRg7',
    'VERKEY': 'AfNcBeyuPZ5WKbiNQKw9vogzkYQggU8BsaTyAaMDfkQv'
}
