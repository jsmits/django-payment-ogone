from ogone.conf import settings
from ogone.forms import OgoneForm, DynOgoneForm
from ogone.security import create_hash
from ogone.models import Order

def get_action():
    if settings.PRODUCTION == True:
        return settings.PROD.URL
    else:
        return settings.TEST_URL

def order_request(order, language=settings.LANGUAGE):
    pm = ''
    brand = ''
    if order.payment_method:
        if order.payment_method.lower() == 'ideal':
            pm = 'ideal'
            brand = ''
        elif order.payment_method.lower() in ['mastercard', 'visa']:
            pm = 'creditcard'
            brand = order.payment_method.lower()
    
    init_data = {
        'orderID': order.order_id,
        'amount': order.amount,
        'currency': order.currency,
        'language': language,
        'SHASign': order.signature,
        # URLs need an appended slash!
        'accepturl': 'http://localhost:8000/checkout/ogone/accepted/', # make this a reverse lookup?
        'cancelurl': 'http://localhost:8000/checkout/ogone/status/',
        # 'declineurl': 'http://localhost:8000/checkout/ogone/status/',
        # 'exceptionurl': 'http://localhost:8000/checkout/ogone/status/',
        'homeurl': 'NONE', # needed to remove the 'back to web shop' button
        'catalogurl': 'NONE', # needed to remove the 'back to web shop' button
        'PM': pm,
        'BRAND': brand,
    }
    
    form = DynOgoneForm(initial_data=init_data, auto_id=False)
    return {'action': get_action(), 'form': form}
    
def create_ogone_order(order_id, amount, currency, payment_method=None, language=settings.LANGUAGE):
    hash = create_hash(order_id, amount, currency, settings.PSPID, 
        settings.SHA1_PRE_SECRET)
    order = Order()
    order.order_id = order_id
    order.currency = currency
    order.amount = amount
    order.payment_method = payment_method
    order.signature = hash
    order.save()
    return order
    