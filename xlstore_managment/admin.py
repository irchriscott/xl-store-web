# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from xlstore_managment.models import MS_LicenceKey, MS_CompanyAdministrator
from xlstore_managment.forms import MS_LicenceKeyForm

# Register your models here.

@admin.register(MS_LicenceKey)
class AdminLicenceKey(admin.ModelAdmin):
	list_display = ('company', 'status', 'activated_date', 'expary_date')
	list_filter = ('company',)
	date_hierarchy = 'expary_date'
	search_fields = ['company__company__name', 'licence_key']
	form = MS_LicenceKeyForm

	def company_name(self, obj):
		return obj.company.company.name

	company_name.admin_order_field = '-company__company__company_name'