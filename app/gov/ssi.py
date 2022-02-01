import sirius_sdk
from django.conf import settings
from main.ssi.custom import RedisLogger, fetch_schema


async def issue_passport(
        connection_key: str, to: sirius_sdk.Pairwise, values: dict, photo_mime_type: str
):
    cred_def, schema = await fetch_schema(
        name="Passport",
        version="1.0",
        attrs=[
            "last_name",
            "first_name",
            "birthday",
            "place_of_birth",
            "issue_date",
            "expiry_date",
            "photo"
        ],
        did=settings.GOV["DID"]
    )
    logger = RedisLogger(connection_key)
    issuer = sirius_sdk.aries_rfc.Issuer(to, logger=logger)
    preview = [sirius_sdk.aries_rfc.ProposedAttrib(key, str(value)) for key, value in values.items() if key != "photo"]
    preview += [sirius_sdk.aries_rfc.ProposedAttrib(name="photo", value="Photo", mime_type=photo_mime_type)]
    translation = [
        sirius_sdk.aries_rfc.AttribTranslation("last_name", "Last Name"),
        sirius_sdk.aries_rfc.AttribTranslation("first_name", "First Name"),
        sirius_sdk.aries_rfc.AttribTranslation("birthday", "Birthday"),
        sirius_sdk.aries_rfc.AttribTranslation("place_of_birth", "Place of birth"),
        sirius_sdk.aries_rfc.AttribTranslation("issue_date", "Issue date"),
        sirius_sdk.aries_rfc.AttribTranslation("photo", "Photo")
    ]

    await issuer.issue(
        values=values,
        schema=schema,
        cred_def=cred_def,
        preview=preview,
        translation=translation,
        comment="Here is your passport",
        locale="en"
    )
