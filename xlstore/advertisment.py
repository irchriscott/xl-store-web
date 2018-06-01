# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from django.template.context_processors import csrf
from xlstore.models import *
from django.views.generic import TemplateView
from xlstore.views import get_categories, saveUserNotificationFromUser, filter_company_sessions
from xlstore.views import saveCompanyNotificationFromUser, saveUserNotificationFromCompany
from xlstore.backends import *
from xlstore.forms import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from django.template import RequestContext
from django.contrib import messages
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q, Count, Sum
from django import template
from django.conf import settings
import json
import random
import string


class AdvertismentController(object):

	def get_advertisments_page(self, request):

		if 'company_name' in request.session:

			company_name = request.session['company_name']
			company_id = request.session['pk']
			product_form = ProductForm()
			category_form = CategoryForm()
			advertisments_company = Advertisments.objects.filter(company=company_id).order_by('-posted_date')

			advertisments_render = {
				'company': Company.objects.get(name_dotted = company_name),
				'session_company': company_name,
				'sum_categories': get_categories(request, company_id),
				'product_form':product_form,
				'category_form':category_form,
				'advertisments_company':advertisments_company,
				'categories': Categories.objects.filter(company=company_id),
				'post_form' : PostForm()
			}

		elif 'username' in request.session:

			session_user = request.session['username']
			user = User.objects.get(user_name=session_user)
			post_form = PostForm()
			advertisments_users = Advertisments.objects.all().order_by('-posted_date')
			advertisments_place = Advertisments.objects.filter(company__country=user.country).order_by('-posted_date')
			
			advertisments_render = {
				'session_user':session_user,
				'user':user,
				'post_form':post_form,
				'advertisments_users':advertisments_users,
				'advertisments_place':advertisments_place,
				'session_profile': User.objects.get(pk=request.session['user']),
				'category_comp': Company.objects.all()
			}

		else:

			advertisments_users = Advertisments.objects.all().order_by('-posted_date')
			
			advertisments_render = {
				'advertisments_users':advertisments_users,
				'category_comp': Company.objects.all()
			}
		
		return render(request, "advertisments.html", advertisments_render)