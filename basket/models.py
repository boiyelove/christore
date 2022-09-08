from django.db import models

# Create your models here.
from products.models import Product

class BasketItem(models.Model):
	basket = models.ForeignKey('Basket', null=True, blank=True)
	product = models.ForeignKey(Product)
	quantity = models.IntegerField(default=1)
	line_total = models.DecimalField(default=10.99, max_digits=1000, decimal_places=2)
	notes = models.TextField(null=True, blank=True)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add = False, auto_now=True)

	def __str__(self):
		try:
			return str(self.basket.id)
		except:
			return self.product.title

class Basket(models.Model):
	total = models.DecimalField(max_digits=100, decimal_places=2, default=0.00)
	timestamp = models.DateTimeField(auto_now_add= False, auto_now=True)
	updated = models.DateTimeField(auto_now_add=True, auto_now=False)

	def __str__(self):
		return "Basket id: %s" % (self.id)