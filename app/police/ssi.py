import sirius_sdk
from django.conf import settings
from main.ssi.custom import RedisLogger


async def fetch_driver_license_schema() -> (sirius_sdk.CredentialDefinition, sirius_sdk.Schema):
    schema_name = "Driver license"
    schema_id, anon_schema = await sirius_sdk.AnonCreds.issuer_create_schema(settings.GOV["DID"], schema_name, '1.0',
                                         ["last_name",
                                          "first_name",
                                          "birthday",
                                          "place_of_birth",
                                          "issue_date",
                                          "expiry_date",
                                          "issuer_code",
                                          "photo",
                                          "place_of_residence",
                                          "categories"
                                          ])
    ledger = await sirius_sdk.ledger(settings.DKMS_NAME)
    schema = await ledger.ensure_schema_exists(anon_schema, settings.GOV["DID"])
    if not schema:
        ok, schema = await ledger.register_schema(anon_schema, settings.GOV["DID"])
        if not ok:
            return None, None

    ok, cred_def = await ledger.register_cred_def(
        cred_def=sirius_sdk.CredentialDefinition(tag='TAG', schema=schema),
        submitter_did=settings.GOV["DID"])

    return cred_def, schema


async def issue_driver_license(
        connection_key: str, to: sirius_sdk.Pairwise, values: dict
):
    cred_def, schema = await fetch_driver_license_schema()
    logger = RedisLogger(connection_key)
    issuer = sirius_sdk.aries_rfc.Issuer(to, logger=logger)
    preview = [sirius_sdk.aries_rfc.ProposedAttrib(key, str(value)) for key, value in values.items()]
    translation = [
        sirius_sdk.aries_rfc.AttribTranslation("last_name", "Last Name"),
        sirius_sdk.aries_rfc.AttribTranslation("first_name", "First Name"),
        sirius_sdk.aries_rfc.AttribTranslation("birthday", "Birthday"),
        sirius_sdk.aries_rfc.AttribTranslation("place_of_birth", "Place of birth"),
        sirius_sdk.aries_rfc.AttribTranslation("issue_date", "Issue date"),
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
