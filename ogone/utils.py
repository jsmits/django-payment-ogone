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
    init_data = {
        'orderID': order.order_id,
        'amount': order.amount,
        'currency': order.currency,
        'language': language,
        'SHASign': order.signature,
        'accepturl': 'http://localhost:8000/checkout/ogone/accepted', # make this a reverse lookup?
        'cancelurl': 'http://localhost:8000/checkout/ogone/accepted',
        # 'PM': 'CreditCard',
        # 'PM': 'ideal',
        # 'BRAND': 'VISA',
        # 'PM': 'paypal',
    }
    print init_data
    form = DynOgoneForm(initial_data=init_data, auto_id=False)
    return {'action': get_action(), 'form': form}
    
def create_ogone_order(order_id, amount, currency, language=settings.LANGUAGE):
    print "secret: %s" % settings.SHA1_PRE_SECRET
    print "create ogone order, id: %s" % order_id
    hash = create_hash(order_id, amount, currency, settings.PSPID, 
        settings.SHA1_PRE_SECRET)
    order = Order()
    order.order_id = order_id
    order.amount = amount
    order.currency = currency
    order.signature = hash
    order.save()
    return order
    