import sirius_sdk
from django.conf import settings
from main.ssi.custom import RedisLogger, fetch_schema


async def ask_passport(connection_key: str, pairwise: sirius_sdk.Pairwise) -> (bool, dict):
    proof_request = {
        "nonce": await sirius_sdk.AnonCreds.generate_nonce(),
        "name": "Verify passport",
        "version": "1.0",
        "requested_attributes": {
            "attr1_referent": {
                "name": "last_name",
                # "restrictions": {
                #     "issuer_did": settings.GOV["DID"]
                # }
            },
            "attr2_referent": {
                "name": "first_name",
                # "restrictions": {
                #     "issuer_did": settings.GOV["DID"]
                # }
            }
        }
    }

    ledger = await sirius_sdk.ledger(settings.DKMS_NAME)
    logger = RedisLogger(connection_key)
    verifier = sirius_sdk.aries_rfc.Verifier(pairwise, ledger, logger=logger)
    ok = await verifier.verify(proof_request=proof_request, comment="Verify passport")
    if ok:
        return ok, verifier.revealed_attrs
    else:
        return ok, None


async def issue_driving_school_diploma(connection_key: str, pairwise: sirius_sdk.Pairwise, values: dict):
    cred_def, schema = await fetch_schema(
        name="Vehicle licence",
        version="1.0",
        attrs=[
            "last_name",
            "first_name",
            "issue_date",
            "categories"
        ],
        did=settings.DRIVING_SCHOOL["DID"]
    )
    logger = RedisLogger(connection_key)
    issuer = sirius_sdk.aries_rfc.Issuer(pairwise, logger=logger)
    preview = [sirius_sdk.aries_rfc.ProposedAttrib(key, str(value)) for key, value in values.items()]
    translation = [
        sirius_sdk.aries_rfc.AttribTranslation("last_name", "Last Name"),
        sirius_sdk.aries_rfc.AttribTranslation("first_name", "First Name"),
        sirius_sdk.aries_rfc.AttribTranslation("issue_date", "Issue date"),
        sirius_sdk.aries_rfc.AttribTranslation("categories", "Categories")
    ]

    await issuer.issue(
        values=values,
        schema=schema,
        cred_def=cred_def,
        preview=preview,
        translation=translation,
        comment="Here is your driving school diploma",
        locale="en"
    )
