import sirius_sdk
from django.conf import settings


DKMS_NAME = 'test_network'


class Logger:

    async def __call__(self, *args, **kwargs):
        print(dict(**kwargs))


async def reg_driver_license() -> (sirius_sdk.CredentialDefinition, sirius_sdk.Schema):
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
    ledger = await sirius_sdk.ledger(DKMS_NAME)
    schema = await ledger.ensure_schema_exists(anon_schema, settings.GOV["DID"])
    if not schema:
        ok, schema = await ledger.register_schema(anon_schema, settings.GOV["DID"])
        if ok:
            print("Driver license schema was registered successfully")
        else:
            print("Driver license schema was not registered")
            return None, None

    else:
        print("Driver license schema is already exists in the ledger")

    ok, cred_def = await ledger.register_cred_def(
        cred_def=sirius_sdk.CredentialDefinition(tag='TAG', schema=schema),
        submitter_did=settings.GOV["DID"])

    if not ok:
        print("Cred def was not registered")

    return cred_def, schema


async def issue_driver_license(
        to: sirius_sdk.Pairwise,
        cred_def: sirius_sdk.CredentialDefinition,
        schema: sirius_sdk.Schema, values: dict
):
    message = sirius_sdk.aries_rfc.Message(
        content="Welcome to the drive license issuer office!",
        locale="en"
    )
    print(message)
    await sirius_sdk.send_to(message, to)

    issuer = sirius_sdk.aries_rfc.Issuer(to, logger=Logger())
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

    ok = await issuer.issue(
        values=values,
        schema=schema,
        cred_def=cred_def,
        preview=preview,
        translation=translation,
        comment="Here is your driver license",
        locale="en"
    )
    if ok:
        print("Driver license was successfully issued")