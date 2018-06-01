# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from time import *
from xlstore.models import Company
from xlstore.models import Products
from xlstore.models import User
from xlstore.models import ProductTrade
from datetime import datetime, timedelta
from xlstore.models import MS_Products
from xlstore.models import TradeAgreements
import datetime


# Create your models here.

def get_teller_img(instance, filename):
	return "tellers/%s_%s" % (str(time()).replace('.','_'), filename)


class MS_CompanyAdministrator(models.Model):
	company = models.OneToOneField(Company)
	email = models.EmailField(max_length=200, unique=True)
	username = models.CharField(max_length=200, blank=False, null=False)
	password = models.CharField(max_length=20)
	company_logo = models.ImageField(blank=True, null=True, upload_to='company_logos/%Y/%m/%d/')
	registration_date = models.DateTimeField(auto_created=True)

	def __unicode__(self):
		return self.company.name

	def get_currency(self):
		settings = MS_Settings.objects.get(company=self.pk)
		return settings.currency


class MS_CompanyMobile(models.Model):
	company = models.ForeignKey(MS_CompanyAdministrator)
	airline = models.CharField(max_length=20, null=True)
	number = models.CharField(max_length=20)

	def __unicode__(self):
		return self.number


class MS_LicenceKey(models.Model):
	company = models.OneToOneField(MS_CompanyAdministrator)
	licence_key = models.CharField(unique=True, max_length=255)
	status = models.CharField(max_length=120, default="desactivated")
	ammount = models.IntegerField(default='0')
	currency = models.CharField(default='USD', max_length=50)
	activated_date = models.DateField(auto_created=True)
	expary_date = models.DateField(auto_created=True)


	def __unicode__(self):
		return self.company.company.name


	def save(self, *args, **kwargs):
		
		activation = MS_LicenceKeyActivations(
				company=MS_LicenceKey.objects.get(company=self.company.pk),
				ammount=self.ammount,
				currency=self.currency,
				activated_date=datetime.datetime.now().date(),
				expary_date=self.expary_date
			)
		activation.save()

		super(MS_LicenceKey, self).save(*args, **kwargs)


class MS_CompanyTeller(models.Model):
	company = models.ForeignKey(MS_CompanyAdministrator)
	full_name = models.CharField(max_length=100)
	username = models.CharField(max_length=100)
	email = models.EmailField(max_length=100)
	teller_image = models.ImageField(upload_to=get_teller_img, blank=True, null=True)
	address = models.CharField(max_length=255)
	phone_number = models.CharField(max_length=100)
	password = models.CharField(max_length=100)
	is_admin = models.BooleanField(default=False)
	registration_date = models.DateTimeField(auto_created=True)

	def __str__(self):
		return self.full_name

	def __unicode__(self):
		return self.pk


class MS_LicenceKeyActivations(models.Model):
	company = models.ForeignKey(MS_LicenceKey)
	ammount = models.IntegerField(default='0')
	currency = models.CharField(default='USD', max_length=50)
	activated_date = models.DateField(auto_created=True)
	expary_date = models.DateField(auto_created=True)

	def __unicode__(self):
		return self.company.company.name


class MS_ProductEntry(models.Model):
	product = models.ForeignKey(MS_Products)
	quantity_before = models.IntegerField()
	quantity_added = models.IntegerField()
	item_price = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
	entry_date = models.DateTimeField(auto_created=True)


	def __unicode__(self):
		return self.product


	def get_total_entry(self):
		return self.quantity_added * self.item_price


class MS_Receipts(models.Model):
	company = models.ForeignKey(MS_CompanyAdministrator)
	user = models.ForeignKey(User, null=True, blank=True)
	teller = models.ForeignKey(MS_CompanyTeller, null=True, blank=True)
	receipt_number = models.IntegerField()
	username = models.CharField(max_length=100)
	email = models.CharField(max_length=100, null=True, blank=True)
	status = models.CharField(max_length=50, default='created')
	other_charges = models.DecimalField(max_digits=18, decimal_places=2, default='0')
	discount = models.DecimalField(max_digits=18, decimal_places=2, default='0')
	total_paid = models.DecimalField(max_digits=18, decimal_places=2, default='0')
	total_net = models.DecimalField(max_digits=18, decimal_places=2, default='0')
	paid_by = models.CharField(max_length=100, default='cash')
	saved_date_timezone = models.DateTimeField(auto_created=True)
	saved_date = models.DateField(auto_created=True)


	def __unicode__(self):
		return self.pk


class MS_ReceiptDetails(models.Model):
	receipt = models.ForeignKey(MS_Receipts)
	product = models.ForeignKey(MS_Products)
	quantity = models.IntegerField()
	item_price = models.DecimalField(max_digits=18, decimal_places=2, default='0', blank=True, null=True)
	total = models.IntegerField()
	is_trade = models.BooleanField(default=False)
	trade = models.ForeignKey(TradeAgreements, null=True, blank=True)
	is_discounted = models.BooleanField(default=False)
	discount = models.DecimalField(max_digits=18, decimal_places=2, default='0')
	saved_date = models.DateField(auto_created=True)


	def __unicode__(self):
		return self.receipt


class MS_Settings(models.Model):
	company = models.OneToOneField(MS_CompanyAdministrator)
	#Trade
	reduce_after_trade_agreed = models.BooleanField(default=False)
	allow_user_to_succeed = models.BooleanField(default=False)
	#MS
	print_bill = models.BooleanField(default=False)
	currency = models.CharField(max_length=255, blank=True, null=True)
	is_currency_changed = models.BooleanField(default=False)
	internationalize = models.BooleanField(default=False)
	access_market = models.BooleanField(default=False)
	time_market_access = models.IntegerField(default='30')
	#Security
	always_admin = models.BooleanField(default=False)
	#MS & SM
	comment_product = models.BooleanField(default=True)


	def __unicode__(self):
		return self.company


	def get_time_access(self):
		return self.time_market_access


	def get_currency(self):
		return self.currency



