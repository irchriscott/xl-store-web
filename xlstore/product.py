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


class ProductController(object):

	def get_users_products(self, request):

		user = request.session['user']
		user = User.objects.get(pk=user)
		products = []

		if user.get_sum_companies() > 0:

			for company in user.get_companies():
				_these_product = Products.objects.filter(company=company.pk).order_by('-posted_date')
				if _these_product is not None:
					for product in _these_product:
						products.append(product)

			if user.get_sum_categories() > 0:

				for category in user.get_company_categories_list():
					_others_products = Products.objects.filter(company__category=category).order_by('-posted_date')
					if _others_products is not None:
						for product in _others_products:
							products.append(product)

			_products_else = Products.objects.all().order_by('?')[:20]
			if _products_else is not None and len(products) < 20:
				for _product in _products_else:
					products.append(_product) 


		elif user.get_sum_categories() > 0:

			for category in user.get_company_categories_list():
				_these_product = Products.objects.filter(company__category=category).order_by('-posted_date')
				if _these_product is not None:
					for product in _these_product:
						products.append(product)

			_products_else = Products.objects.all().order_by('?')[:20]

			if _products_else is not None and len(products) < 20:
				for _product in _products_else:
					products.append(_product) 

		else:

			_products = Products.objects.filter(company__country=user.country)

			for product in _products:
				products.append(product)

			if len(_products) < 20:
				
				_products_else = Products.objects.all().order_by('?')[:20]
				if _products_else is not None:
					for _product in _products_else:
						products.append(_product) 

		return sorted(set(products), key=lambda product: product.posted_date, reverse=True)


	def get_home_page(self, request):

		if 'company_name' in request.session:

			company_name = request.session['company_name']
			company_id = request.session['pk']
			product_form = ProductForm()
			category_form = CategoryForm()
			products_company = Products.objects.filter(company=company_id).order_by('-posted_date')
			product_category = Categories.objects.all()

			home_render = {
				'company': Company.objects.get(name_dotted = company_name),
				'session_company': company_name,
				'sum_categories': get_categories(request, company_id),
				'product_form':product_form,
				'category_form':category_form,
				'products_company':products_company,
				'product_category':product_category,
				'categories': Categories.objects.filter(company=company_id),
				'post_form':PostForm()
			}

		elif 'username' in request.session:

			session_user = request.session['username']
			user = User.objects.get(user_name=session_user)
			post_form = PostForm()
			users_products = Products.objects.all()
			product_category = Categories.objects.all()

			home_render = {
				'session_user':session_user,
				'user':user,
				'post_form':post_form,
				'users_products':self.get_users_products(request),
				'product_category':product_category,
				'session_profile': User.objects.get(pk=request.session['user'])
			}

		else:

			products_users = Products.objects.all().order_by('-posted_date')
			product_category = Categories.objects.all()
			other_pictures = ProductPictures.objects.filter(product=products_users)

			home_render = {
				'products_users':products_users,
				'product_category':product_category,
			}

		return render(request, "home.html", home_render)


	def get_products_page(self, request):

		if 'company_name' in request.session:

			company_name = request.session['company_name']
			company_id = request.session['pk']
			product_form = ProductForm()
			category_form = CategoryForm()
			products_company = Products.objects.filter(company=company_id).order_by('-posted_date')
			product_category = Categories.objects.all()

			paginator = Paginator(products_company, settings.PAGINATOR_ITEMS)
			page = request.GET.get('page')
			
			try:
				products = paginator.page(page)
			except PageNotAnInteger:
				products = paginator.page(1)
			except EmptyPage:
				products = paginator.page(paginator.num_pages)

			products_render = {
				'company': Company.objects.get(name_dotted = company_name),
				'session_company': company_name,
				'sum_categories': get_categories(request, company_id),
				'product_form':product_form,
				'category_form':category_form,
				'products':products,
				'product_category':product_category,
				'categories': Categories.objects.filter(company=company_id),
				'post_form': PostForm()
			}

		elif 'username' in request.session:

			session_user = request.session['username']
			user = User.objects.get(user_name=session_user)
			post_form = PostForm()
			products_all = self.get_users_products(request)
			product_category = Categories.objects.all()

			paginator = Paginator(products_all, settings.PAGINATOR_ITEMS)
			page = request.GET.get('page')
			
			try:
				products = paginator.page(page)
			except PageNotAnInteger:
				products = paginator.page(1)
			except EmptyPage:
				products = paginator.page(paginator.num_pages)

			products_render = {
				'session_user':session_user,
				'user':user,
				'post_form':post_form,
				'products':products,
				'product_category':product_category,
				'session_profile': User.objects.get(pk=request.session['user']),
				'category_comp': Company.objects.all()
			}

		else:

			products_users = Products.objects.all().order_by('-posted_date')
			product_category = Categories.objects.all()

			paginator = Paginator(products_users, settings.PAGINATOR_ITEMS)
			page = request.GET.get('page')
			
			try:
				products = paginator.page(page)
			except PageNotAnInteger:
				products = paginator.page(1)
			except EmptyPage:
				products = paginator.page(paginator.num_pages)

			products_render = {
				'products_users':products,
				'product_category':product_category,
				'category_comp': Company.objects.all()
			}
		
		return render(request, "products.html", products_render)


	def add_product(self, request):

		if 'company_name' in request.session:

			template = "includes/add_product.html"
			company_name = request.session['company_name']
			session_id = request.session['pk']

			product_form = ProductForm()
			categories = Categories.objects.filter(company=session_id)
			company = Company.objects.get(name_dotted = company_name)

			product_render = {}
			product_render["product_form"] = product_form
			product_render["categories"] = categories
			product_render["company"] = company

			return render(request, template, product_render)


	def save_product(self, request):

		session_id = request.session['pk']
		if request.method == 'POST':
			if filter_company_sessions(request) is not None:

				category = request.POST.get('category','')
				product_form = ProductForm(request.POST, request.FILES, instance=Products(
						company = Company.objects.get(pk=session_id),
						category = Categories.objects.get(pk=category)
					))
				if product_form.is_valid():
					product = product_form.save(commit=False)
					product.posted_date = timezone.now()
					product.save()
					messages.success(request, "Product Saved Successfully !!!")
					return HttpResponseRedirect(reverse('comp_profile', kwargs={'company_name':request.session['company_name']}))
				else:
					messages.error(request, product_form.errors)
					return HttpResponseRedirect(reverse('comp_profile', kwargs={'company_name':request.session['company_name']}))
			
			else:
				messages.error(request, "You're not the admin !!!")
				return HttpResponseRedirect(reverse('comp_profile', kwargs={'company_name':request.session['company_name']}))
		else:
			messages.error(request, "OOPS...!!! Something is wrong !!!")
			return HttpResponseRedirect(reverse('comp_profile', kwargs={'company_name':request.session['company_name']}))

		return HttpResponseRedirect(reverse('comp_profile', kwargs={'company_name':request.session['company_name']}))


	def get_similar_products(self, request, product):

		char_strings = ['~', '!', '%', '^', '&', '*', '(', ')', '+', '?', '<', '>', '|', ',', '.', '/', '[', ']', '{', '}', '=']
		product = Products.objects.get(pk=product)

		for char in char_strings:
			name = product.product_name.replace(char, '')

		name = name.split()
		products = []

		for _names in name:
			_name = _names.lower()
			_products = Products.objects.filter(product_name__icontains=_name).order_by('-posted_date')
			if _products is not None:
				for _product in _products:
					if _product.company.category.pk == product.company.category.pk and _product.pk != product.pk:
						products.append(_product)

		return sorted(set(products))


	def get_single_product(self, request, company_name, product_id):

		template = "product.html"
		product_render = {}
		not_owner = 0
		product = get_object_or_404(Products, pk=product_id)

		if 'company_name' in request.session:
			company_name = request.session['company_name']
			session_id = request.session['pk']

			product_form = ProductForm()
			more_images_form = ProductPicturesUpload()
			edit_product = EditProduct(instance=Products.objects.get(pk=product_id))
			categories = Categories.objects.filter(company=session_id)
			advertisment_form = AdvertismentsForm()
			company = Company.objects.get(name_dotted = company_name)
			
			product_render.update(csrf(request))
			product_render['session_company'] = company_name
			product_render['product_form'] = product_form
			product_render['edit_product'] = edit_product
			product_render['categories'] = categories
			product_render['more_images_form'] = more_images_form
			product_render['advertisment_form'] = advertisment_form
			product_render['post_form'] = PostForm()
			product_render['company'] = company

			if product.company.pk != session_id:
				not_owner = "COMPANY CAN'T SEE OTHER COMPANIES'S PRODUCT UNLESS THERE ARE BLENDED BY A BOND"
			else:
				not_owner = 0
		elif 'username' in request.session:

			session_user = request.session['username']
			session_id = request.session['user']
			user = User.objects.get(pk=session_id)
			company = Company.objects.get(name_dotted = company_name)

			product_render['session_user'] = session_user
			product_render['user'] = user
			product_render['post_form'] = PostForm()
			product_render['company'] = company
			product_render['session_profile'] = User.objects.get(pk=request.session['user'])

		category_product = Categories.objects.get(pk=product.category)
		other_pictures = ProductPictures.objects.filter(product=product)
		similar_product = Products.objects.filter(category=product.category).order_by('-posted_date')
		other_pictures_count = ProductPictures.objects.filter(product=product).count()
		other_pictures_count_else = int(ProductPictures.objects.filter(product=product).count()) - 1
		product_advertisment = Advertisments.objects.filter(product=product)
		company = Company.objects.get(name_dotted = company_name)

		product_render['company'] = company
		product_render['product_id'] = product_id
		product_render['product'] = product
		product_render['category_product'] = category_product
		product_render['other_pictures'] = other_pictures
		product_render['other_pictures_count'] = other_pictures_count
		product_render['other_pictures_count_else'] = other_pictures_count_else
		product_render['similar_product'] = self.get_similar_products(request, product.pk)
		product_render['not_owner'] = not_owner
		product_render['product_advertisment'] = product_advertisment

		return render(request, template, product_render)


	def user_interess_product(self, request):

		if request.method == 'POST':

			product_id = request.POST.get('product', '')
			product = Products.objects.get(pk=product_id)

			if 'username' in request.session:
				session_id = request.session['user']
				user = User.objects.get(pk=session_id)
				check_interess = ProductInteress.objects.filter(user=user.pk, product=product.pk)
					
				if check_interess:
					return HttpResponse('already')
				else:
					interess = ProductInteress(
							user=User.objects.get(pk=session_id),
							product=Products.objects.get(pk=product_id),
							interess_date=timezone.now()
						)
					interess.save()

					saveCompanyNotificationFromUser(
							request,
							User.objects.get(pk=session_id),
							Company.objects.get(pk=product.company.pk),
							product.pk,
							'interess'
						)

					return HttpResponse('Success !!!')
			else:
				return HttpResponse('session')

		return HttpResponse('cool')


	def user_like_dislike_product(self, request):

		if request.method == 'POST':

			product_id = request.POST.get('product', '')
			product = Products.objects.get(pk=product_id)
			mention = request.POST.get('mention', '')

			if 'username' in request.session:
				session_id = request.session['user']
				check_mention = ProductMention.objects.filter(user=session_id, product=product.pk)

				if check_mention:
					for this_mention in check_mention:
						mention_product = ProductMention.objects.get(pk=this_mention.pk)
						mention_product.mention = mention
						mention_product.mention_date = timezone.now()
						mention_product.save()
					return HttpResponse('update')
				else :
					mention_product = ProductMention(
							product=Products.objects.get(pk=product_id),
							user=User.objects.get(pk=session_id),
							mention=mention,
							mention_date=timezone.now()
						)
					mention_product.save()

					saveCompanyNotificationFromUser(
							request,
							User.objects.get(pk=session_id),
							Company.objects.get(pk=product.company.pk),
							product.pk,
							'%s_product' % mention
						)
					return HttpResponse('saved')

		return HttpResponse('cool')


	def get_single_product_ajax(self, request, product_id):

		template = "productajax.html"
		product_render = {}
		not_owner = 0
		product = get_object_or_404(Products, pk=product_id)
		other_pictures = ProductPictures.objects.filter(product=product)
		other_pictures_count = ProductPictures.objects.filter(product=product).count()
		other_pictures_count_else = int(ProductPictures.objects.filter(product=product).count()) - 1
		category_product = Categories.objects.get(pk=product.category)
		
		if 'company_name' in request.session:
			product_render['session_company'] = request.session['company_name']
			product_render['company'] = Company.objects.get(pk=request.session['pk'])

			if product.company.pk != request.session['pk']:
				not_owner = "COMPANY CAN'T SEE OTHER COMPANIES'S PRODUCT UNLESS THERE ARE BLENDED BY A BOND"
			else:
				not_owner = 0

		elif 'username' in request.session:
			product_render['session_user'] = request.session['username']
			product_render['user'] = User.objects.get(pk=request.session['user'])

		product_render['product'] = product
		product_render['other_pictures'] = other_pictures
		product_render['not_owner'] = not_owner
		product_render['other_pictures_count'] = other_pictures_count
		product_render['other_pictures_count_else'] = other_pictures_count_else
		product_render['category_product'] = category_product

		return render(request, template, product_render)


	def get_edit_product(self, request, product_id):

		if 'company_name' in request.session:

			template = 'includes/edit_product.html'
			edit_product = EditProduct(instance=Products.objects.get(pk=product_id))
			product_render = {}
			product_render.update(csrf(request))
			product_render['edit_product'] = edit_product
			product_render['product'] = get_object_or_404(Products, pk=product_id)

			return render(request, template, product_render)


	@csrf_exempt
	def edit_product(self, request, product_id):

		company_name = request.session['company_name']
		session_id = request.session['pk']

		if request.method == 'POST':
			if filter_company_sessions(request) is not None:
				edit_product = EditProduct(request.POST)
				if edit_product.is_valid():
					product = Products.objects.get(pk=product_id)
					product.product_name = edit_product.cleaned_data['product_name']
					product.price = edit_product.cleaned_data['price']
					product.currency = edit_product.cleaned_data['currency']
					product.product_description = edit_product.cleaned_data['product_description']
					product.save()
					messages.success(request, "Product Updated Successfully!!!")

					return HttpResponseRedirect('/company/'+request.session['company_name']+'/products/item='+product_id)
				else:
					messages.error(request, edit_product.errors)
					return HttpResponseRedirect('/company/'+request.session['company_name']+'/products/item='+product_id)
			else:
				messages.error(request, "You are Not an Admin !!!")
				return HttpResponseRedirect(reverse('single_product', kwargs={'company_name':request.session['company_name'], 'product_id':product_id}))
		else:
			messages.error(request, "OOPS")
			return HttpResponseRedirect(reverse('single_product', kwargs={'company_name':request.session['company_name'], 'product_id':product_id}))


	def get_upload_more_images(self, request, product_id):

		if 'company_name' in request.session:

			template = "includes/upload_more.html"
			more_images_form = ProductPicturesUpload()
			image_context = {}
			image_context.update(csrf(request))
			image_context['more_images_form'] = more_images_form
			image_context['product'] = get_object_or_404(Products, pk=product_id)

			return render(request, template, image_context)


	def upload_more_images(self, request, product_id):

		company_name = request.session['company_name']
		session_id = request.session['pk']

		if request.method == 'POST':
			if filter_company_sessions(request) is not None:
				product_images = ProductPicturesUpload(request.POST, request.FILES)
				files = request.FILES.getlist('image')

				if product_images.is_valid():
					company = Company.objects.get(pk=session_id)
					for file in files:
						product_image = ProductPictures(
								product = Products.objects.get(pk=product_id),
								image = file,
								uploaded_date=timezone.now()
							)
						product_image.save()

					messages.success(request, "Product Images Uploaded Successfully !!!")
					return HttpResponseRedirect(reverse('single_product', kwargs={'company_name':request.session['company_name'], 'product_id':product_id}))
				else:
					messages.error(request, product_images.errors)
					return HttpResponseRedirect(reverse('single_product', kwargs={'company_name':request.session['company_name'], 'product_id':product_id}))
			else:
				messages.error(request, "You are Not an Admin !!!")
				return HttpResponseRedirect(reverse('single_product', kwargs={'company_name':request.session['company_name'], 'product_id':product_id}))


	def get_advertise_product(self, request, product_id):

		if 'company_name' in request.session:
			template = 'includes/advertise.html'
			advertisment_form = AdvertismentsForm()

			advert_context = {}
			advert_context.update(csrf(request))
			advert_context['advertisment_form'] = advertisment_form
			advert_context['product'] = get_object_or_404(Products, pk=product_id)

			return render(request, template, advert_context)


	def get_product_advertisment(self, request, product_id):

		template = 'includes/advertisment.html'
		advert_context = {}
		product_advertisment = Advertisments.objects.filter(product=product_id)
		advert_context['product_advertisment'] = product_advertisment

		return render(request, template, advert_context)


	def advertise_product(self, request, product_id):

		company_name = request.session['company_name']
		session_id = request.session['pk']

		if request.method == 'POST':
			if filter_company_sessions(request) is not None:
				advertisment_form = AdvertismentsForm(request.POST, request.FILES, instance=Advertisments(
						company = Company.objects.get(pk=session_id),
						product = Products.objects.get(pk=product_id)
					))

				if advertisment_form.is_valid():
					advertisment = advertisment_form.save(commit=False)
					advertisment.posted_date = timezone.now()
					advertisment.save()
					messages.success(request, "Advertisment Added Successfully !!!")

					return HttpResponseRedirect(reverse('single_product', kwargs={'company_name':request.session['company_name'], 'product_id':product_id}))
				else:
					messages.error(request, advertisment_form.errors)
					return HttpResponseRedirect(reverse('single_product', kwargs={'company_name':request.session['company_name'], 'product_id':product_id}))
			else:
				messages.error(request, "You are Not an Admin !!!")
				return HttpResponseRedirect(reverse('single_product', kwargs={'company_name':request.session['company_name'], 'product_id':product_id}))
