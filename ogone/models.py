from django.db import models
from django.contrib.auth.models import User

class Order(models.Model):
    """Order request."""
    user = models.ForeignKey(User, null=True)
    order_id = models.CharField(max_length=20)
    currency = models.CharField(blank=True, max_length=5)
    amount = models.IntegerField(blank=True, null=True)
    signature = models.CharField(blank=True, null=True, max_length=40)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return "%s" % self.order_id
        
    def is_payed(self):
        if self.status == 9:
            return True
        else:
            return False
     
class OrderStatus(models.Model):
    """Order status."""
    order = models.ForeignKey(Order)
    amount = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=10)
    currency = models.CharField(blank=True, max_length=5)
    payment_method = models.CharField(blank=True, null=True, max_length=30)
    acceptance = models.IntegerField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    card_number = models.CharField(blank=True, null=True, max_length=30)
    pay_id = models.CharField(blank=True, null=True, max_length=10)
    error = models.IntegerField(blank=True, null=True)
    brand = models.CharField(blank=True, null=True, max_length=30)
    signature = models.CharField(blank=True, null=True, max_length=40)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return "%s, status: %s" % (self.order, self.status)