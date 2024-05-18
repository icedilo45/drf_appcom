from django.db import models
from django.contrib.auth.models import User
from utils.models_abstracts import Model
from django_extensions.db.models import (
    TimeStampedModel,
    ActivatorModel,
    TitleSlugDescriptionModel
)

# Create your models here.

class Item(
    TimeStampedModel,
    ActivatorModel,
    TitleSlugDescriptionModel,
    Model):
    '''
    App Ecommerce Products. It stores single item in the AppCom Store
    '''
    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'Items'
        ordering = ['id']

    def __str__(self):
        return self.title
        
    stock = models.IntegerField(default=1)
    price = models.IntegerField(default=0)

    def amount(self):
        # Converts price in UDS to Cedi
        amount = float(self.price * 14.8)
        return amount
    
    def reduce_stock(self, qty):
        # Used to reduce stock as products are bought
        new_stock =  self.stock - int(qty)
        self.stock = new_stock
        self.save()

    def check_stock(self, qty):
        #used to check if order quantity exceeds stock levels
        if int(qty) > self.stock:
            return False
        return True
    
    def place_order(self, user, qty):
        #used to place an order
        if self.check_stock(qty):
            order = Order.objects.create(
                item = self,
                quantity = qty,
                user = user)
            self.reduce_stock(qty)
            return order
        else:
            return None


class Order(
    TimeStampedModel,
    ActivatorModel ,
    Model):
    """
    ecommerce.Order
    Stores a single order entry, related to :model:`ecommerce.Item` and
    :model:`auth.User`.
    """
    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        ordering = ['id']


    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    item = models.ForeignKey(Item, null=True, blank=True, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user.username} - {self.item.title}'