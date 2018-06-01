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


class CompanyRegister(TemplateView):

	template = "comp_regist.html"

	def get(self, request):
		form = CompanyForm()
		return render(request, self.template, {'form': form})

	def post(self, request):
		form = CompanyForm(request.POST, instance=Company(profile_image="default/default_company.jpg", registration_date=timezone.now()))
		if form.is_valid():
			form.save()
			messages.success(request, "You have been registered successfully !!!")
			return HttpResponseRedirect(reverse('login_comp'))
		else:
			form = CompanyForm()
			messages.error(request, form.errors)
			return HttpResponseRedirect(reverse('regist_comp'))

		return HttpResponseRedirect(reverse('login_comp'))


class CompanyController(object):

	def get_comp_login_page(self, request):

		log_comp = {}
		log_comp.update(csrf(request))

		if 'company_name' in request.session:
			try:
				del request.session['pk']
				del request.session['company_name']
			except KeyError:
				pass

			if 'ms' in request.session:
				try:
					del request.session['ms']
				except KeyError:
					pass
				if 'admin' in request.session:
					try:
						del request.session['admin']
					except KeyError:
						pass
				if 'teller' in request.session:
					try:
						del request.session['teller']
					except KeyError:
						pass
		elif 'username' in request.session:
			try:
				del request.session['user']
				del request.session['username']
			except KeyError:
				pass

		return render(request, "comp_login.html", log_comp)


	def get_comp_auth_page(self, request):

		logcomp_email = request.POST.get('logcomp_email', '')
		logcomp_password = request.POST.get('logcomp_password', '')
		comp_auth = CompanyAuth()
		company = comp_auth.authenticate_company(email=logcomp_email, password=logcomp_password)
		
		if company is not None:
			company_name = company.name

			request.session['company_email'] = company.email
			request.session['company_name'] = company.name_dotted
			request.session['pk'] = company.pk

			return HttpResponseRedirect(reverse('home'))
		else:
			return HttpResponseRedirect(reverse('invalid_comp'))


	def get_comp_profile(self, request, company_name):

		template = 'company.html'

		if 'company_name' in request.session:

			company_name = request.session['company_name']
			company = Company.objects.get(name_dotted = company_name)
			profile_image_form = CompanyProfileImage()
			cover_image_form = CompanyCoverImage()
			product_form = ProductForm()
			com_id = request.session['pk']
			categories = Categories.objects.filter(company=company.pk)
			product_category = Categories.objects.all()
			products_company = Products.objects.filter(company__id=company.pk).select_related('company').order_by('-posted_date')
			other_pictures = ProductPictures.objects.filter(product=products_company)

			paginator = Paginator(products_company, settings.PAGINATOR_ITEMS)
			page = request.GET.get('page')
			
			try:
				products = paginator.page(page)
			except PageNotAnInteger:
				products = paginator.page(1)
			except EmptyPage:
				products = paginator.page(paginator.num_pages)

			company_render = {}
			company_render.update(csrf(request))
			company_render['company'] = company
			company_render['session_company'] = company_name
			company_render['profile_image_form'] = profile_image_form
			company_render['cover_image_form'] = cover_image_form
			company_render['categories'] = categories
			company_render['product_form'] = product_form
			company_render['update_company'] = UpdateCompanyForm(instance=Company.objects.get(pk=com_id))
			company_render['products'] = products
			company_render['other_pictures'] = other_pictures
			company_render['product_category'] = product_category
			company_render['post_form'] = PostForm()

		elif 'username' in request.session:

			company = get_object_or_404(Company, name_dotted = company_name)
			categories = Categories.objects.filter(company=company.pk)
			product_category = Categories.objects.all()
			products_company = Products.objects.filter(company__id=company.pk).select_related('company').order_by('-posted_date')
			other_pictures = ProductPictures.objects.filter(product=products_company)
			session_user = request.session['username']
			session_id = request.session['user']
			user = get_object_or_404(User, user_name=session_user)
			check_follow = Followers.objects.filter(user=request.session['user'], company=company.pk)
			comp_trades = ProductTrade.objects.filter(user=request.session['user'], product__company=company.pk).order_by('-started_date')

			paginator = Paginator(products_company, settings.PAGINATOR_ITEMS)
			page = request.GET.get('page')
			
			try:
				products = paginator.page(page)
			except PageNotAnInteger:
				products = paginator.page(1)
			except EmptyPage:
				products = paginator.page(paginator.num_pages)

			company_render = {}
			company_render['company'] = company
			company_render['categories'] = categories
			company_render['products'] = products
			company_render['other_pictures'] = other_pictures
			company_render['product_category'] = product_category
			company_render['session_user'] = session_user
			company_render['user'] = user
			company_render['post_form'] = PostForm()
			company_render['check_follow'] = check_follow
			company_render['session_profile'] = User.objects.get(pk=request.session['user'])
			company_render['trades'] = comp_trades

		else:

			company = get_object_or_404(Company, name_dotted = company_name)
			categories = Categories.objects.filter(company=company.pk)
			product_category = Categories.objects.all()
			products_company = Products.objects.filter(company__id=company.pk).select_related('company').order_by('-posted_date')
			other_pictures = ProductPictures.objects.filter(product=products_company)

			paginator = Paginator(products_company, settings.PAGINATOR_ITEMS)
			page = request.GET.get('page')
			
			try:
				products = paginator.page(page)
			except PageNotAnInteger:
				products = paginator.page(1)
			except EmptyPage:
				products = paginator.page(paginator.num_pages)

			company_render = {}
			company_render['company'] = company
			company_render['categories'] = categories
			company_render['products'] = products
			company_render['other_pictures'] = other_pictures
			company_render['product_category'] = product_category
		
		return render(request, template, company_render)


	def get_comp_invalid_page(self, request):
		error = "Incorrect Email Address or Password"
		return render(request, "comp_login.html", {'error':error})


	def get_comp_logout_page(self, request):
		try:
			del request.session['pk']
			del request.session['company_name']
		except KeyError:
			pass
		if 'ms' in request.session:
			try:
				del request.session['ms']
			except KeyError:
				pass
			if 'admin' in request.session:
				try:
					del request.session['admin']
				except KeyError:
					pass
			if 'teller' in request.session:
				try:
					del request.session['teller']
				except KeyError:
					pass
		return HttpResponseRedirect('/home/')


	def update_comp_profile_image(self, request):

		session_id = request.session['pk']
		company_name = request.session['company_name']

		if request.method == 'POST':

			if filter_company_sessions(request) is not None:
				profile_image_form = CompanyProfileImage(request.POST, request.FILES)
				
				if profile_image_form.is_valid():
					company = Company.objects.get(pk=session_id)
					company.profile_image = profile_image_form.cleaned_data['profile_image']
					company.save()
					profile_image_form = CompanyProfileImage()
					cover_image_form = CompanyProfileImage()
					messages.success(request, "Profile Picture Modified Successfully !!!")
					return HttpResponseRedirect(reverse('comp_profile', kwargs={'company_name':request.session['company_name']}))		
			else:
				message.error(request, "Sorry, You're not the admin !!!")
				return HttpResponseRedirect(reverse('comp_profile', kwargs={'company_name':request.session['company_name']}))
		else:
			profile_image_form = CompanyProfileImage()

		return HttpResponseRedirect(reverse('comp_profile', kwargs={'company_name':request.session['company_name']}))


	def update_comp_cover_image(self, request):

		session_id = request.session['pk']
		company_name = request.session['company_name']
		
		if request.method == 'POST':
			
			if filter_company_sessions(request) is not None:
				cover_image_form = CompanyCoverImage(request.POST, request.FILES)
		        
		        if cover_image_form.is_valid():
					company = Company.objects.get(pk=session_id)
					company.cover_image = cover_image_form.cleaned_data['cover_image']
					company.save()
					cover_image_form = CompanyProfileImage()
					messages.add_message(request, messages.SUCCESS, "Cover Picture Modified Successfully !!!")
					return HttpResponseRedirect(reverse('comp_profile', kwargs={'company_name':request.session['company_name']}))
			else:
				messages.add_message(request, messages.ERROR, "Sorry, You're not the admin")
				return HttpResponseRedirect(reverse('comp_profile', kwargs={'company_name':request.session['company_name']}))
		else:
			cover_image_form = CompanyCoverImage()

		return HttpResponseRedirect(reverse('comp_profile', kwargs={'company_name':request.session['company_name']}))


	def update_company_profile(self, request):

		if 'company_name' in request.session:
			session_id = request.session['pk']
			
			if request.method == 'POST':
				
				if filter_company_sessions(request) is not None:
					update_company = UpdateCompanyForm(request.POST)
					
					if update_company.is_valid():
						company = Company.objects.get(pk=session_id)
						company.name = update_company.cleaned_data['name']
						company.phone_number = update_company.cleaned_data['phone_number']
						company.motto = update_company.cleaned_data['motto']
						company.description = update_company.cleaned_data['description']
						company.save()
						
						messages.success(request, "Profile Updated Successfully !!!")
						return HttpResponseRedirect(reverse('comp_profile', kwargs={'company_name':request.session['company_name']}))
					else:
						update_company = UpdateCompanyForm()
						return HttpResponseRedirect(reverse('comp_profile', kwargs={'company_name':request.session['company_name']}))
				else:
					messages.error(request, "Sorry, You're not the admin !!!")
					return HttpResponseRedirect(reverse('comp_profile', kwargs={'company_name':request.session['company_name']}))
			else:

				template = "includes/update_company.html"
				company_render = {}
				company_render.update(csrf(request))
				company_render['update_company'] = UpdateCompanyForm(instance=Company.objects.get(pk=session_id))

				return render(request, template, company_render)
		else:
			messages.error(request, "Login Please !!!")
			return HttpResponseRedirect(reverse('home'))


	def get_comp_posts(self, request, company_name):

		template = 'companyposts.html'

		if 'company_name' in request.session:

			company_name = request.session['company_name']
			company = Company.objects.get(name_dotted = company_name)
			profile_image_form = CompanyProfileImage()
			cover_image_form = CompanyCoverImage()
			product_form = ProductForm()
			com_id = request.session['pk']
			categories = Categories.objects.filter(company=company.pk)
			posts_all = Posts.objects.filter(company=company.pk).order_by('-posted_date')

			paginator = Paginator(posts_all, settings.PAGINATOR_ITEMS)
			page = request.GET.get('page')
			
			try:
				posts = paginator.page(page)
			except PageNotAnInteger:
				posts = paginator.page(1)
			except EmptyPage:
				posts = paginator.page(paginator.num_pages)

			post_render = {}
			post_render.update(csrf(request))
			post_render['company'] = company
			post_render['session_company'] = company_name
			post_render['profile_image_form'] = profile_image_form
			post_render['cover_image_form'] = cover_image_form
			post_render['categories'] = categories
			post_render['product_form'] = product_form
			post_render['update_company'] = UpdateCompanyForm(instance=Company.objects.get(pk=com_id))
			post_render['post_form'] = PostForm()
			post_render['posts'] = posts

		elif 'username' in request.session:

			company = get_object_or_404(Company, name_dotted = company_name)
			categories = Categories.objects.filter(company=company.pk)
			session_user = request.session['username']
			session_id = request.session['user']
			user = get_object_or_404(User, user_name=session_user)
			check_follow = Followers.objects.filter(user=request.session['user'], company=company.pk)
			posts_all = Posts.objects.filter(company=company.pk).order_by('-posted_date')

			paginator = Paginator(posts_all, settings.PAGINATOR_ITEMS)
			page = request.GET.get('page')
			
			try:
				posts = paginator.page(page)
			except PageNotAnInteger:
				posts = paginator.page(1)
			except EmptyPage:
				posts = paginator.page(paginator.num_pages)

			post_render = {}
			post_render.update(csrf(request))
			post_render['company'] = company
			post_render['categories'] = categories
			post_render['session_user'] = session_user
			post_render['user'] = user
			post_render['post_form'] = PostForm()
			post_render['check_follow'] = check_follow
			post_render['posts'] = posts
			post_render['session_profile'] = User.objects.get(pk=request.session['user'])
		
		else:

			company = get_object_or_404(Company, name_dotted = company_name)
			categories = Categories.objects.filter(company=company.pk)
			posts_all = Posts.objects.filter(company=company.pk).order_by('-posted_date')

			paginator = Paginator(posts_all, settings.PAGINATOR_ITEMS)
			page = request.GET.get('page')
			
			try:
				posts = paginator.page(page)
			except PageNotAnInteger:
				posts = paginator.page(1)
			except EmptyPage:
				posts = paginator.page(paginator.num_pages)

			post_render = {}
			post_render['company'] = company
			post_render['categories'] = categories
			post_render['posts'] = posts
		
		return render(request, template, post_render)


	def get_comp_categories(self, request, company_name):

		template = 'categories.html'

		if 'company_name' in request.session:

			company_name = request.session['company_name']
			company_id = request.session['pk']
			profile_image_form = CompanyProfileImage()
			cover_image_form = CompanyCoverImage()
			category_form = CategoryForm()
			product_form = ProductForm()
			categories = Categories.objects.filter(company=company_id).order_by('-created_date')
			products = Products.objects.filter(company__id=company_id).order_by('-posted_date')
			update_company = UpdateCompanyForm(instance=Company.objects.get(pk=company_id))
			product_category = Categories.objects.all()
			
			categories_render = {
				'company': Company.objects.get(name_dotted = company_name),
				'session_company': company_name,
				'profile_image_form':profile_image_form,
				'cover_image_form':cover_image_form,
				'category_form':category_form,
				'categories':categories,
				'product_form':product_form,
				'update_company':update_company,
				'product_category':product_category,
				'products':products,
				'post_form': PostForm(),
			}

		elif 'username' in request.session:

			company = get_object_or_404(Company, name_dotted = company_name)
			categories = Categories.objects.filter(company=company.pk).order_by('-created_date')
			products = Products.objects.filter(company__id=company.pk).order_by('-posted_date')
			session_user = request.session['username']
			session_id = request.session['user']
			user = User.objects.get(pk=session_id)
			product_category = Categories.objects.all()
			check_follow = Followers.objects.filter(user=request.session['user'], company=company.pk)
			comp_trades = ProductTrade.objects.filter(user=request.session['user'], product__company=company.pk).order_by('-started_date')

			categories_render = {
				'company': company,
				'categories':categories,
				'product_category':product_category,
				'session_user':session_user,
				'user':user,
				'post_form':PostForm(),
				'check_follow':check_follow,
				'products':products,
				'session_profile': User.objects.get(pk=request.session['user']),
				'trades': comp_trades,
				'category_comp': Company.objects.all()
			}

		else:

			company = get_object_or_404(Company, name_dotted = company_name)
			product_category = Categories.objects.all()
			categories = Categories.objects.filter(company=company.pk).order_by('-created_date')
			products = Products.objects.filter(company__id=company.pk).order_by('-posted_date')
			
			categories_render = {
				'company': company,
				'categories':categories,
				'product_category':product_category,
				'products':products, 
				'category_comp': Company.objects.all()
			}

		return render(request, template, categories_render)



	def get_comp_about(self, request, company_name):
		pass


	def get_comp_followers(self, request, company_name):

		template = "companyfollowers.html"
		followers_render = {}

		if 'company_name' in request.session:

			company_name = request.session['company_name']
			session_id = request.session['pk']

			product_form = ProductForm()
			profile_image_form = CompanyProfileImage()
			cover_image_form = CompanyCoverImage()
			categories = Categories.objects.filter(company=session_id)
			update_company = UpdateCompanyForm(instance=Company.objects.get(pk=session_id))
			company = Company.objects.get(name_dotted = company_name)
			followers = Followers.objects.filter(company=session_id)

			followers_render.update(csrf(request))
			followers_render['session_company'] = company_name
			followers_render['product_form'] = product_form
			followers_render['categories'] = categories
			followers_render['profile_image_form'] = profile_image_form
			followers_render['cover_image_form'] = cover_image_form
			followers_render['update_company'] = update_company
			followers_render['post_form'] = PostForm()
			followers_render['followers'] = followers
			followers_render['company'] = company

		elif 'username' in request.session:

			session_user = request.session['username']
			session_id = request.session['user']
			user = User.objects.get(pk=session_id)
			company = Company.objects.get(name_dotted = company_name)
			check_follow = Followers.objects.filter(user=request.session['user'], company=company.pk)

			followers_render['session_user'] = session_user
			followers_render['user'] = user
			followers_render['post_form'] = PostForm()
			followers_render['check_follow'] = check_follow
			followers_render['session_profile'] = User.objects.get(pk=request.session['user'])
			followers_render['companies_may_know'] = Company.objects.all()

		company = Company.objects.get(name_dotted = company_name)
		followers = Followers.objects.filter(company=company.pk)

		followers_render['followers'] = followers
		followers_render['company'] = company

		return render(request, template, followers_render)


	def user_follow_company(self, request):

		if request.method == 'POST':

			company_id = request.POST.get('company', '')
			company = Company.objects.get(pk=company_id)

			if 'username' in request.session:
				session_id = request.session['user']
				check_follow = Followers.objects.filter(user=session_id, company=company_id)
					
				if check_follow:
					messages.success(request, "Exist!!!")
					return HttpResponseRedirect(reverse('comp_profile', kwargs={'company_name':company.name_dotted}))
				
				else:
					follow = Followers(
							user=User.objects.get(pk=session_id),
							company=Company.objects.get(pk=company_id),
							follow_date=timezone.now()
						)
					follow.save()
					saveCompanyNotificationFromUser(
							request,
							User.objects.get(pk=session_id),
							Company.objects.get(pk=company.pk),
							session_id,
							'follow'
						)
					messages.success(request, "Saved!!!")
					return HttpResponseRedirect(reverse('comp_profile', kwargs={'company_name':company.name_dotted}))
			else:
				messages.error(request, "no session!!!")
				return HttpResponseRedirect(reverse('comp_profile', kwargs={'company_name':company.name_dotted}))

		return HttpResponseRedirect(reverse('comp_profile', kwargs={'company_name':company.name_dotted}))


	def get_comp_advertisments(self, request, company_name):

		template = 'comp_advert.html'

		if 'company_name' in request.session:

			company_name = request.session['company_name']
			company = Company.objects.get(name_dotted = company_name)
			profile_image_form = CompanyProfileImage()
			cover_image_form = CompanyCoverImage()
			product_form = ProductForm()
			com_id = request.session['pk']
			categories = Categories.objects.filter(company=company.pk)
			product_category = Categories.objects.all()
			advertisments = Advertisments.objects.filter(company=company.pk).order_by('-posted_date')

			advertisment_render = {}
			advertisment_render.update(csrf(request))
			advertisment_render['company'] = company
			advertisment_render['session_company'] = company_name
			advertisment_render['profile_image_form'] = profile_image_form
			advertisment_render['cover_image_form'] = cover_image_form
			advertisment_render['categories'] = categories
			advertisment_render['product_form'] = product_form
			advertisment_render['update_company'] = UpdateCompanyForm(instance=Company.objects.get(pk=com_id))
			advertisment_render['advertisments'] = advertisments
			advertisment_render['post_form'] = PostForm()

		elif 'username' in request.session:

			session_user = request.session['username']
			session_id = request.session['user']
			user = User.objects.get(pk=session_id)
			company = get_object_or_404(Company, name_dotted = company_name)
			categories = Categories.objects.filter(company=company.pk)
			product_category = Categories.objects.all()
			advertisments = Advertisments.objects.filter(company=company.pk).order_by('-posted_date')
			check_follow = Followers.objects.filter(user=request.session['user'], company=company.pk)

			advertisment_render = {}
			advertisment_render['company'] = company
			advertisment_render['categories'] = categories
			advertisment_render['advertisments'] = advertisments
			advertisment_render['session_user'] = session_user
			advertisment_render['user'] = user
			advertisment_render['post_form'] = PostForm()
			advertisment_render['check_follow'] = check_follow
			advertisment_render['session_profile'] = User.objects.get(pk=request.session['user'])
		
		else:
			
			company = get_object_or_404(Company, name_dotted = company_name)
			categories = Categories.objects.filter(company=company.pk)
			product_category = Categories.objects.all()
			advertisments = Advertisments.objects.filter(company=company.pk).order_by('-posted_date')

			advertisment_render = {}
			advertisment_render['company'] = company
			advertisment_render['categories'] = categories
			advertisment_render['advertisments'] = advertisments

		return render(request, template, advertisment_render)
