from datetime import datetime
try:
    from decimal import Decimal
except ImportError:
    from django.utils._decimal import Decimal

from django.http import HttpResponse
from django.utils.translation import ugettext
from django.template import RequestContext, loader, Context
from django.shortcuts import render_to_response, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.dispatch import dispatcher
from django.conf import settings
from django.core.mail import mail_admins

from ogone.security import create_hash
from ogone.forms import TestPaymentForm, OgoneForm
from ogone.models import Order, OrderStatus
from ogone.conf import settings as ogone_settings
from ogone.utils import get_action, order_request
from ogone import signals
from ogone.utils import create_ogone_order

class InvalidSignatureException(Exception):
    pass
    
class InvalidParamsException(Exception):
    pass

def get_test_order_id():
    now = datetime.now()
    return now.strftime("%Y%m%d%H%M%S")

def test_form3(request):
    if request.method == 'POST':
        form = TestPaymentForm(request.POST)
        if form.is_valid():
            order_id = get_test_order_id()
            amount = form.cleaned_data['amount']
            currency = form.cleaned_data['currency']
            language = form.cleaned_data['language']
            order = create_ogone_order(order_id, amount, currency, language)
            order_form_data = order_request(order)
            return render_to_response('ogone/base_form.html', {
                'form': order_form_data['form'], 'action': order_form_data['action'], 
                'header': 'Process Payment', 'title': 'test payment'})
    else:
        form = TestPaymentForm()
    return render_to_response('ogone/test_payment.html', {'form': form})

# @login_required
def ogone(request, amount=1250, order_id=None, currency='EUR', order=None):
    order_id = order_id or get_test_order_id()
    order = order or get_object_or_404(Order, order_id=order_id)
    order_form_data = order_request(order)
    return render_to_response('ogone/to_ogone_form.html', {
        'form': order_form_data['form'], 'action': order_form_data['action'], 
        'header': '', 'title': ''})
        
def to_ogone(request):
    order_id = request.GET.get('order_id')
    order = get_object_or_404(Order, order_id=order_id)
    return ogone(request, amount=order.amount, order_id=order_id, order=order)
    
@require_http_methods(["POST", "GET"])
def order_status_update(request):
    params = request.POST or request.GET
    if not params:
        raise InvalidParamsException("no parameters in the request")
        
    order_id = params.get('orderID')
    # check for Order existence
    order = Order.objects.get(order_id=order_id) 
    amount = params.get('amount')
    currency = params.get('currency')
    payment_method = params.get('PM')
    acceptance = params.get('ACCEPTANCE')
    status = params.get('STATUS')
    card_number = params.get('CARDNO')
    pay_id = params.get('PAYID')
    error = params.get('NCERROR') # this is needed when NCERROR == [u'']
    brand = params.get('BRAND')
    ip = params.get('IP')
    signature = params.get('SHASIGN')

    # check signature
    hash = create_hash(order_id, currency, amount, payment_method, acceptance,
        status, card_number, pay_id, error, brand, ogone_settings.SHA1_POST_SECRET)
    if hash != signature:
        raise InvalidSignatureException("hash (%s) != signature" % hash)
        
    # set numeric fields to None if they are empty (i.e. == [u''])
    if not amount: amount = None
    if not status: status = None
    if not error:  error = None
    
    # store order status
    order_status = OrderStatus(order=order, amount=amount, currency=currency,
        payment_method=payment_method, acceptance=acceptance, status=status,
        card_number=card_number, pay_id=pay_id, error=error, brand=brand,
        signature=signature)
    order_status.save()
    
    # base the response on the status code (see status_codes.txt)
    # authorized and accepted
    if status:
        if status == u'9': 
            # send ogone_payment_accepted signal with amount converted to Decimal and cents
            signals.ogone_payment_accepted.send(sender=OrderStatus, order_id=order_id, 
                amount=Decimal(amount) * 100, currency=currency)
            # return the appropiate response
            return HttpResponse("your payment has been accepted")
        # cancelled
        elif status == u'1': 
            return HttpResponse("your payment request has been cancelled")
        elif int(status) in [0,2,4,41,5,51,52,59,6,61,62,63,7,71,72,73,74,75,
            8,81,82,83,84,85,91,92,93,94,95,97,98,99]:
            return HttpResponse("payment has not been processed")
        else:
            # mail_admins
            subject = 'Error (%s IP): %s' % ((request.META.get('REMOTE_ADDR') in settings.INTERNAL_IPS and 'internal' or 'EXTERNAL'), request.path)
            try:
                request_repr = repr(request)
            except:
                request_repr = "Request repr() unavailable"
            # message = "Unknown ogone status code: %s\n\n%s" % (status, request_repr)
            mail_admins(subject, message, fail_silently=True)
            return HttpResponse("payment has not been processed")
    else:
        return HttpResponse("payment has not been processed")
    
        