# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from xlstore.models import MS_Products
from xlstore.models import User
from xlstore_managment.models import MS_CompanyAdministrator

# Create your models here.


class EC_CompanySettings(models.Model):
	company = models.OneToOneField(MS_CompanyAdministrator)
	use_ecommerce = models.BooleanField(default=False)
	use_paypal = models.BooleanField(default=False)
	paypal = models.CharField(max_length=200, null=True, blank=True)
	mobile = models.BooleanField(default=False)

	def __unicode__(self):
		return self.use_ecommerce


class EC_MarketAccess(models.Model):
	company = models.ForeignKey(MS_CompanyAdministrator)
	user = models.ForeignKey(User)
	key = models.CharField(max_length=100, null=True, blank=True, unique=True)
	status = models.CharField(max_length=50)
	access_time = models.IntegerField(null=True, blank=True)
	time_from = models.DateTimeField(auto_created=True, null=True, blank=True)
	time_to = models.DateTimeField(auto_created=True, null=True, blank=True)
	key_date = models.DateField(auto_created=True)

	def __unicode__(self):
		return self.pk

	def get_sum_sum_sales(self):
		sales = EC_ShoppingCart.objects.filter(market=self.pk).count()
		return sales

	def get_access_market_json(self):
		return {
				"company": self.company.company.get_company_json(),
				"user": self.user.get_user_json(self.user.pk),
				"key": self.key,
				"status": self.status,
				"time": self.access_time,
				"from": self.time_from,
				"to": self.time_to
			}


class EC_ShoppingCart(models.Model):
	market = models.ForeignKey(EC_MarketAccess)
	status = models.CharField(max_length=100)
	total_net = models.DecimalField(max_digits=18, decimal_places=2, default='0')
	others_chargers = models.DecimalField(max_digits=18, decimal_places=2, default='0')
	total_paid = models.DecimalField(max_digits=18, decimal_places=2, default='0')
	payment_mode = models.CharField(max_length=30, null=True, blank=True)
	delivery = models.BooleanField(default=False)
	saved_date = models.DateTimeField(auto_created=True)
	finished_date = models.DateTimeField(auto_created=True, null=True, blank=True)

	def __unicode__(self):
		return self.market.key

	def get_items_cart(self):
		items = EC_ShoppingCartItems.objects.filter(cart=self.pk)
		return items

	def get_sum_items_cart(self):
		sum_items = EC_ShoppingCartItems.objects.filter(cart=self.pk).count()
		return sum_items

	def get_cart_total(self):
		total = 0
		items = EC_ShoppingCartItems.objects.filter(cart=self.pk)
		if items is not None:
			for item in items:
				total += item.total
		return total

	def get_shopping_cart_json(self):
		return {
					"id": self.pk,
					"user": self.market.user.get_user_json(self.market.user.pk),
					"company": self.market.company.company.get_company_json(),
					"key": self.market.key,
					"status": self.status,
					"total_net": self.total_net,
					"charges": self.others_chargers,
					"total_paid": self.total_paid,
					"payment_mode": self.payment_mode,
					"delivery": self.delivery,
					"saved_date": self.saved_date,
					"finished_date": self.finished_date
			   }


class EC_ShoppingCartItems(models.Model):
	cart = models.ForeignKey(EC_ShoppingCart)
	product = models.ForeignKey(MS_Products)
	quantity = models.IntegerField()
	item_price = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
	total = models.DecimalField(max_digits=18, decimal_places=2)
	saved_date = models.DateTimeField(auto_created=True)

	def __unicode__(self):
		return self.product.product.product.product_name