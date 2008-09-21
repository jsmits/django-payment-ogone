from ogone.conf import settings
from ogone.forms import OgoneForm, DynOgoneForm
from ogone.security import create_hash
from ogone.models import Order

def get_action():
    if settings.PRODUCTION == True:
        return settings.PROD.URL
    else:
        return settings.TEST_URL

def order_request(order_id, amount, currency, user=None, language=settings.LANGUAGE):
    order = Order()
    order.order_id = order_id
    order.amount = amount
    order.currency = currency
    order.user = user
    order.save()
    hash = create_hash(order_id, amount, currency, settings.PSPID, 
        settings.SHA1_PRE_SECRET)
    init_data = {
        'orderID': order_id,
        'amount': amount,
        'currency': currency,
        'language': language,
        'SHASign': hash,
        'accepturl': 'http://localhost:8000/accepted', # make this a reverse lookup?
        'cancelurl': 'http://localhost:8000/accepted',
        # 'PM': 'CreditCard',
        # 'PM': 'ideal',
        # 'BRAND': 'VISA',
        # 'PM': 'paypal',
    }
    form = DynOgoneForm(initial_data=init_data, auto_id=False)
    return {'action': get_action(), 'form': form}
    