# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext

from ogone.conf import settings

AMOUNT_CHOICES = (
    ('1250', "12,50"), 
    ('2500', "25,00"), 
    ('5000', "50,00"), 
    ('7500', "75,00"),
)

CURRENCIES = (
    ('EUR', 'EUR'),
    ('USD', 'USD'),
    ('GBP', 'GBP'),
)

LANGUAGES = (
    ('nl_NL', 'NL'),
    ('en_US', 'EN'),
    ('fr_FR', 'FR'),
)

class TestPaymentForm(forms.Form):
    # order_id = forms.IntegerField(label=ugettext('order_id'))
    amount = forms.ChoiceField(label=ugettext('amount'), choices=AMOUNT_CHOICES) 
    currency = forms.ChoiceField(label=ugettext('currency'), choices=CURRENCIES)
    language = forms.ChoiceField(label=ugettext('language'), choices=LANGUAGES)
    
class OgoneForm(forms.Form):
    # order parameters
    PSPID = forms.CharField(widget=forms.HiddenInput, initial=settings.PSPID)
    orderID = forms.CharField(widget=forms.HiddenInput)
    amount = forms.CharField(widget=forms.HiddenInput)
    currency = forms.CharField(widget=forms.HiddenInput)
    language = forms.CharField(widget=forms.HiddenInput)
    # sha1_signature
    SHASign = forms.CharField(widget=forms.HiddenInput)
    # lay out information
    TITLE = forms.CharField(widget=forms.HiddenInput)
    BGCOLOR = forms.CharField(widget=forms.HiddenInput)
    TXTCOLOR = forms.CharField(widget=forms.HiddenInput)
    TBLBGCOLOR = forms.CharField(widget=forms.HiddenInput)
    TBLTXTCOLOR = forms.CharField(widget=forms.HiddenInput)
    BUTTONBGCOLOR = forms.CharField(widget=forms.HiddenInput)
    BUTTONTXTCOLOR = forms.CharField(widget=forms.HiddenInput)
    LOGO = forms.CharField(widget=forms.HiddenInput)
    FONTTYPE = forms.CharField(widget=forms.HiddenInput)
    # dynamic template page
    TP = forms.CharField(widget=forms.HiddenInput)
    # post-payment redirection
    accepturl = forms.CharField(widget=forms.HiddenInput)
    declineurl = forms.CharField(widget=forms.HiddenInput)
    exceptionurl = forms.CharField(widget=forms.HiddenInput)
    cancelurl = forms.CharField(widget=forms.HiddenInput)
    # miscellaneous
    COM = forms.CharField(widget=forms.HiddenInput)
    CN = forms.CharField(widget=forms.HiddenInput)
    EMAIL = forms.CharField(widget=forms.HiddenInput)
    PM = forms.CharField(widget=forms.HiddenInput)
    BRAND = forms.CharField(widget=forms.HiddenInput)
    ownerZIP = forms.CharField(widget=forms.HiddenInput)
    owneraddress = forms.CharField(widget=forms.HiddenInput)
    
    def __init__(self, initial_data, *args, **kwargs):
        super(OgoneForm, self).__init__(*args, **kwargs)
        # forms.Form.__init__(self, *args, **kwargs)
        for name, value in initial_data.items():
            self.fields[name].initial = value
            
class DynOgoneForm(forms.Form):
    """dynamic ogone form"""
    PSPID = forms.CharField(widget=forms.HiddenInput, initial=settings.PSPID)

    def __init__(self, initial_data, *args, **kwargs):
        super(DynOgoneForm, self).__init__(*args, **kwargs)
        for name, value in initial_data.items():
            self.fields[name] = forms.CharField(widget=forms.HiddenInput, 
                initial=value)
    