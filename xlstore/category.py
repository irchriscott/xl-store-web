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


class ProductCategoryController(object):

	def get_category_template(self, request):

		if 'company_name' in request.session:
			template = 'includes/add_category.html'
			category_context = {}
			category_context.update(csrf(request))
			category_context['category_form'] = CategoryForm()
			category_context['company'] = get_object_or_404(Company, name_dotted = request.session['company_name'])

			return render(request, template, category_context)


	def save_category(self, request):

		session_id = request.session['pk']
		company = Company.objects.get(pk=session_id)

		if request.method == 'POST':

			if filter_company_sessions(request) is not None:
				category_form = CategoryForm(request.POST)
				if category_form.is_valid():
					category = category_form.save(commit=False)
					category.company = Company.objects.get(pk=session_id)
					category.save()
					category_form = CategoryForm()
					messages.success(request, "Category Added Successfully !!!")
					return HttpResponseRedirect(reverse('comp_categories', kwargs={'company_name':request.session['company_name']}))
			else:
				messages.error(request, "Sorry, You're not the admin !!!")
				return HttpResponseRedirect(reverse('comp_categories', kwargs={'company_name':request.session['company_name']}))
		else:
			pass


	def get_single_category(self, request, company_name, category_id):

		template = "category.html"
		category_render = {}
		not_owner = 0
		category = get_object_or_404(Categories, pk=category_id)
		company = Company.objects.get(name_dotted=company_name)

		if 'company_name' in request.session:
			company_name = request.session['company_name']
			session_id = request.session['pk']

			product_form = ProductForm()
			category_edit_form = CategoryForm(instance=Categories.objects.get(pk=category_id))
			categories = Categories.objects.filter(company=session_id)
			company = Company.objects.get(name_dotted = company_name)

			category_render.update(csrf(request))
			category_render['session_company'] = company_name
			category_render['product_form'] = product_form
			category_render['category_edit_form'] = category_edit_form
			category_render['categories'] = categories
			category_render['post_form'] = PostForm()

			if category.company.pk != session_id:
				not_owner = "COMPANY CAN'T SEE OTHER COMPANIES'S CATEGORY UNLESS THERE ARE BLENDED BY A BOND"
			else:
				not_owner = 0
		elif 'username' in request.session:
			session_user = request.session['username']
			session_id = request.session['user']
			user = User.objects.get(pk=session_id)

			category_render['session_user'] = session_user
			category_render['user'] = user
			category_render['post_form'] = PostForm()
			category_render['session_profile'] = User.objects.get(pk=request.session['user'])

		product_category = Products.objects.filter(category=category_id).order_by('-posted_date')
		product_category_count = Products.objects.filter(category=category_id).count()

		category_render['product_category'] = product_category
		category_render['not_owner'] = not_owner
		category_render['company'] = company
		category_render['category'] = category
		category_render['product_category_count'] = product_category_count

		return render(request, template, category_render)


	def get_edit_category_template(self, request, category_id):
		
		if 'company_name' in request.session:
			template = "includes/edit_category.html"
			category_context = {}
			category_context.update(csrf(request))
			category_context['category_edit_form'] =  CategoryForm(instance=Categories.objects.get(pk=category_id))
			category_context['category'] = get_object_or_404(Categories, pk=category_id)
			
			return render(request, template, category_context)


	def edit_category(self, request, category_id):

		company_name = request.session['company_name']
		session_id = request.session['pk']

		if request.method == 'POST':

			if filter_company_sessions(request) is not None:

				category_form = CategoryForm(request.POST)
				if category_form.is_valid():
					category = Categories.objects.get(pk=category_id)
					category.name = category_form.cleaned_data['name']
					category.description = category_form.cleaned_data['description']
					category.save()
					messages.success(request, "Category Updated Successfully !!!")
					return HttpResponseRedirect(reverse('comp_profile', kwargs={'company_name':request.session['company_name'], 'category_id':category_id}))
				else:
					messages.error(request, category_form.errors)
					return HttpResponseRedirect(reverse('comp_profile', kwargs={'company_name':request.session['company_name'], 'category_id':category_id}))
			else:
				messages.error(request, "You're not the admin !!!")
				return HttpResponseRedirect(reverse('comp_profile', kwargs={'company_name':request.session['company_name'], 'category_id':category_id}))
