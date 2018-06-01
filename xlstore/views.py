# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from django.contrib import auth
from django.template.context_processors import csrf
from pip._vendor.requests import Response
from xlstore.models import *
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import TemplateView
from xlstore.backends import *
from xlstore.forms import *
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from django.template import RequestContext
from django.contrib import messages
from django.urls import reverse
from django.views.generic.edit import FormView
from django.core.signing import Signer
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q, Count, Sum
from django import template
from django.conf import settings
import json
import random
import string

# Create your views here.

helper = Helpers()

register = template.Library()

@register.simple_tag(name='cache_bust')
def cache_bust():

	if settings.DEBUG:                                                                                                                   
		version = uuid.uuid1()
	else:
		version = os.environ.get('PROJECT_VERSION')
		if version is None:
			version = '1'

	return 'async_v={version}'.format(version=version)


def saveUserNotificationFromUser(request, user, concern, notification_id, about):
	notification = UserNotifications(
			user=user,
			concern=concern,
			notification_maker='user',
			notification_id=notification_id,
			about=about,
			is_read=False,
			posted_date=timezone.now()
		)
	notification.save()
	return HttpResponse(notification.about)


def saveUserNotificationFromCompany(request, company, concern, notification_id, about):
	notification = UserNotifications(
			company=company,
			concern=concern,
			notification_maker='company',
			notification_id=notification_id,
			about=about,
			is_read=False,
			posted_date=timezone.now()
		)
	notification.save()
	return HttpResponse(notification.about)


def saveCompanyNotificationFromUser(request, user, concern, notification_id, about):
	notification = CompanyNotifications(
			user=user,
			concern=concern,
			notification_id=notification_id,
			about=about,
			is_read=False,
			posted_date=timezone.now()
		)
	notification.save()
	return HttpResponse(notification.about)


def getUserIpAddress(request):
    return {'ip_address': request.META['REMOTE_ADDR']}


def return_response(params):
	response = HttpResponse(params, content_type="application/json")
	response['Access-Control-Allow-Origin'] = "*"
	response['Access-Control-Allow-Headers'] = "origin, x-requested-with, content-type"
	response['Access-Control-Allow-Methods'] = "PUT, GET, POST, DELETE, OPTIONS"
	return response


def get_categories(request, company_id):
	categories = Categories.objects.filter(company=company_id).count()
	return categories


def filter_company_sessions(request):
	if 'company_name' in request.session and 'ms' not in request.session:
		return True
	elif 'company_name' in request.session and 'ms' in request.session:
		if 'admin' in request.session:
			return True
		else:
			return None
	else:
		return None


def get_categories(request, company_id):
	categories = Categories.objects.filter(company=company_id).count()
	return categories


def load_geo_map(request, source, any_id):
	template = "includes/map.html"
	if source == "trade":
		if 'username' in request.session or filter_company_sessions(request) is not None:
			message = ProductTradeMessages.objects.get(pk=any_id)
			if message.trade.user.pk == request.session['user'] or message.trade.product.company.pk == request.session['pk']:
				map_render = {}
				map_render['session'] = True
				map_render['longitude'] = message.longitude
				map_render['latitude'] = message.latitude
				map_render['address'] = message.address

				return render_to_response(template, map_render)
			else:
				return HttpResponse("<p class='xl-error'>YOU ARE NOT THE OWNER</p>")
		else:
			return HttpResponseRedirect(reverse('home_simple'))

	elif source == "address":
		address = Address.objects.get(pk=any_id)
		
		map_render = {}
		map_render['longitude'] = address.longitude
		map_render['latitude'] = address.latitude
		map_render['address'] = address.address

		return render_to_response(template, map_render)

	else:
		return HttpResponse("Unknown Map Source")


#Search Form


def search_products_comp_users(request):
	
	products = []
	users = []
	companies = []

	search = request.GET.get('search')
	searches = search.split()

	if 'company_name' in request.session:
		_products = Products.objects.filter(company=request.session['pk'], product_name__icontains=search)
		if _products is not None:
			for product in _products:
				products.append(product.get_product_json())

		_company = Company.objects.get(pk=request.session['pk'])
		companies.append(_company.get_company_json())
	else:
		_products = Products.objects.filter(product_name__icontains=search)
		_companies = Company.objects.filter(name__icontains=search)
		if _products is not None:
			for product in _products:
				products.append(product.get_product_json())

		if _companies is not None:
			for company in _companies:
				companies.append(company.get_company_json())

		if len(searches) > 1:
			for _search in searches:
				_products = Products.objects.filter(product_name__icontains=_search)
				_companies = Company.objects.filter(name__icontains=_search)
				if _products is not None:
					for _product in _products:
						products.append(_product.get_product_json())

				if _companies is not None:
					for _company in _companies:
						companies.append(_company.get_company_json())


	_users = User.objects.filter(full_name__icontains=search)
	_users_else = User.objects.filter(user_name__icontains=search)

	if _users is not None:
		for user in _users:
			users.append(user.get_user_json(user.pk))

	if _users_else is not None:
		for _user in _users_else:
			users.append(_user.get_user_json(_user.pk))

	if len(searches) > 1:
		for _search in searches:
			_users_ = User.objects.filter(full_name__icontains=_search)
			_users_else_ = User.objects.filter(user_name__icontains=_search)

			if _users_ is not None:
				for user in _users_:
					users.append(user.get_user_json(user.pk))

			if _users_else_ is not None:
				for user in _users_else_:
					users.append(user.get_user_json(user.pk))

	data = {'search': search, 'products': products, 'companies': companies, 'users': users}
	
	return return_response(json.dumps(data, indent=4, sort_keys=False, default=str))


#For Application & Helpers


def api_get_products(request):
	products = Products.objects.all()
	products = serializers.serialize('json', products)
	return HttpResponse(products, content_type="application/json")


def api_get_users_tags(request):
	users = [user.get_user_tag_json() for user in User.objects.all()]
	response = HttpResponse(json.dumps(users, indent=4, default=str), content_type='application/json')
	response['Access-Control-Allow-Origin'] = "*"
	return response


def api_search_get_all_products(request):
	products = [product.get_product_json() for product in Products.objects.all().order_by('-posted_date')]
	products = json.dumps(products, indent=4, sort_keys=True, default=str)
	return return_response(products)


def api_search_get_all_users(request):
	allowed_chars = ''.join((string.lowercase, string.uppercase, string.digits))
	token = ''.join(random.choice(allowed_chars) for _ in range(16))

	users = [user.get_user_json(token) for user in User.objects.all()]
	users = json.dumps(users, indent=4, sort_keys=True, default=str)
	return return_response(users)


def api_search_get_all_companies(request):
	companies = [company.get_company_json() for company in Company.objects.all()]
	companies = json.dumps(companies, indent=4, sort_keys=True, default=str)
	return return_response(companies)

