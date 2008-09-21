from django.conf import settings

PSPID = getattr(settings, "OGONE_PSPID")
TEST_URL = getattr(settings, "OGONE_TEST_URL", 
    "https://secure.ogone.com/ncol/test/orderstandard.asp")
PROD_URL = getattr(settings, "OGONE_PROD_URL", 
    "https://secure.ogone.com/ncol/prod/orderstandard.asp")
PRODUCTION = getattr(settings, "OGONE_PRODUCTION", False)

LANGUAGE = 'nl_NL'
# LANGUAGE = 'en_US'
CURRENCY = 'EUR'

SHA1_PRE_SECRET = getattr(settings, "OGONE_SHA1_PRE_SECRET", '')
SHA1_POST_SECRET = getattr(settings, "OGONE_SHA1_POST_SECRET", '')