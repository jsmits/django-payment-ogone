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

from ogone.security import create_hash
from ogone.forms import TestPaymentForm, OgoneForm
from ogone.models import Order, OrderStatus
from ogone.conf import settings
from ogone.utils import get_action, order_request
from ogone import signals
from ogone.utils import create_ogone_order

def get_order_id():
    now = datetime.now()
    return now.strftime("%Y%m%d%H%M%S")

def test_form3(request):
    if request.method == 'POST':
        form = TestPaymentForm(request.POST)
        if form.is_valid():
            order_id = get_order_id()
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
    order_id = order_id or get_order_id()
    order = order or get_object_or_404(Order, order_id=order_id)
    order_form_data = order_request(order)
    return render_to_response('ogone/to_ogone_form.html', {
        'form': order_form_data['form'], 'action': order_form_data['action'], 
        'header': '', 'title': ''})
        
def to_ogone(request):
    order_id = request.GET.get('order_id')
    order = get_object_or_404(Order, order_id=order_id)
    print order.amount
    print order_id
    return ogone(request, amount=order.amount, order_id=order_id, order=order)
    # return HttpResponse("order_id: %s" % order_id)

@require_http_methods(["POST", "GET"])
def order_status_update(request):
    params = request.POST or request.GET
    if not params: 
        return HttpResponse("no params")
    order_id = params.get('orderID')
    amount = Decimal(params.get('amount'))
    currency = params.get('currency')
    payment_method = params.get('PM')
    acceptance = params.get('ACCEPTANCE')
    status = int(params.get('STATUS'))
    card_number = params.get('CARDNO')
    pay_id = params.get('PAYID')
    error = params.get('NCERROR')
    brand = params.get('BRAND')
    ip = params.get('IP')
    signature = params.get('SHASIGN')
    order = get_object_or_404(Order, order_id=order_id)
    # store in model
    hash = create_hash(order_id, currency, amount, payment_method, acceptance,
        status, card_number, pay_id, error, brand, settings.SHA1_POST_SECRET)
    if hash != signature:
        # wrong signature, mail_admins
        return HttpResponse("hash != signature")
    else:
        # process incoming status
        print "amount: %s" % amount
        print "amount (in cents): %s" % (amount * 100)
        order_status = OrderStatus(order=order, amount=amount, currency=currency,
            payment_method=payment_method, acceptance=acceptance, status=status,
            card_number=card_number, pay_id=pay_id, error=error, brand=brand,
            signature=signature)
        order_status.save()
        if status == 9: # authorized and accepted
            # send ogone_payment_accepted signal
            signals.ogone_payment_accepted.send(sender=OrderStatus, order_id=order_id, 
                amount=amount * 100, currency=currency)
    return HttpResponse("order_status_update processed")
    
        