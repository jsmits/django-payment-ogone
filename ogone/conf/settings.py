from django.conf import settings

PSPID = getattr(settings, "OGONE_PSPID", "dummy_pspid")
TEST_URL = getattr(settings, "OGONE_TEST_URL", 
    "https://secure.ogone.com/ncol/test/orderstandard.asp")
PROD_URL = getattr(settings, "OGONE_PROD_URL", 
    "https://secure.ogone.com/ncol/prod/orderstandard.asp")
PRODUCTION = getattr(settings, "OGONE_PRODUCTION", False)

# PSPID = 'jhmsmits'
LANGUAGE = 'nl_NL'
# LANGUAGE = 'en_US'
CURRENCY = 'EUR'

SHA1_PRE_SECRET = '%vvvzrzq(&9gh6m1+966'
SHA1_POST_SECRET = 'p%74z(mbrj%)rii$60_g'