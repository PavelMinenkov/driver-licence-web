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
                "restrictions": {
                    "issuer_did": settings.GOV["DID"]
                }
            },
            "attr2_referent": {
                "name": "first_name",
                "restrictions": {
                    "issuer_did": settings.GOV["DID"]
                }
            },
            "attr3_referent": {
                "name": "birthday",
                "restrictions": {
                    "issuer_did": settings.GOV["DID"]
                }
            },
            "attr4_referent": {
                "name": "place_of_birth",
                "restrictions": {
                    "issuer_did": settings.GOV["DID"]
                }
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


async def ask_driver_school_diploma(connection_key: str, pairwise: sirius_sdk.Pairwise) -> (bool, dict):
    proof_request = {
        "nonce": await sirius_sdk.AnonCreds.generate_nonce(),
        "name": "Verify driver school diploma",
        "version": "1.0",
        "requested_attributes": {
            "attr1_referent": {
                "name": "categories",
                "restrictions": {
                    "issuer_did": settings.DRIVING_SCHOOL["DID"]
                }
            }
        }
    }

    ledger = await sirius_sdk.ledger(settings.DKMS_NAME)
    logger = RedisLogger(connection_key)
    verifier = sirius_sdk.aries_rfc.Verifier(pairwise, ledger, logger=logger)
    ok = await verifier.verify(proof_request=proof_request, comment="Verify driver school diploma")
    if ok:
        return ok, verifier.revealed_attrs
    else:
        return ok, None


async def issue_driver_license(
        connection_key: str, to: sirius_sdk.Pairwise, values: dict, photo_mime_type: str
):
    cred_def, schema = await fetch_schema(
        name="Driver licence",
        version="1.0",
        attrs=[
            "last_name",
            "first_name",
            "birthday",
            "place_of_birth",
            "issue_date",
            "expiry_date",
            "issuer_code",
            "photo",
            "place_of_residence",
            "categories"
        ],
        did=settings.POLICE["DID"]
    )
    values["issuer_code"] = "123"
    logger = RedisLogger(connection_key)
    issuer = sirius_sdk.aries_rfc.Issuer(
        holder=to,
        logger=logger
    )
    preview = [sirius_sdk.aries_rfc.ProposedAttrib(key, str(value)) for key, value in values.items() if key != "photo"]
    preview += [sirius_sdk.aries_rfc.ProposedAttrib(name="photo", value=values["photo"], mime_type=photo_mime_type)]
    translation = [
        sirius_sdk.aries_rfc.AttribTranslation("last_name", "Last Name"),
        sirius_sdk.aries_rfc.AttribTranslation("first_name", "First Name"),
        sirius_sdk.aries_rfc.AttribTranslation("birthday", "Birthday"),
        sirius_sdk.aries_rfc.AttribTranslation("place_of_birth", "Place of birth"),
        sirius_sdk.aries_rfc.AttribTranslation("issue_date", "Issue date"),
        sirius_sdk.aries_rfc.AttribTranslation("expiry_date", "Expiry date"),
        sirius_sdk.aries_rfc.AttribTranslation("issuer_code", "Issuer code"),
        sirius_sdk.aries_rfc.AttribTranslation("photo", "Photo"),
        sirius_sdk.aries_rfc.AttribTranslation("place_of_residence", "Place of residence"),
        sirius_sdk.aries_rfc.AttribTranslation("categories", "Categories")
    ]

    await issuer.issue(
        values=values,
        schema=schema,
        cred_def=cred_def,
        preview=preview,
        translation=translation,
        comment="Here is your driver license",
        locale="en"
    )
