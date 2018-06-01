# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from django.template.context_processors import csrf
from django.views.generic import TemplateView
from xlstore.views import get_categories, saveUserNotificationFromUser, filter_company_sessions
from xlstore.views import saveCompanyNotificationFromUser, saveUserNotificationFromCompany
from xlstore.models import *
from xlstore.backends import *
from xlstore.forms import *
from xlstore_managment.views import ms_get_user_bills_and_carts, ms_get_user_bills_and_carts_company
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


class UserRegister(TemplateView):

	template = "user_regist.html"

	def get(self, request):
		form = UserForm()
		return render(request, self.template, {'form': form})


	def post(self, request):
		form = UserForm(request.POST, instance=User(profile_image="default/default_user.jpg", registration_date=timezone.now()))
		if form.is_valid():
			password = request.POST.get('password', '')
			conf_password = request.POST.get('conf_password', '')
			email = request.POST.get('email', '')
			email_auth = UserAuth()
			email_check = email_auth.check_email(email=email)

			if email_check is not None:
				form = UserForm()
				error = "Email already taken !!!"
				return render(request, "user_regist.html", {'form':form, 'error':error})
			else:
				if password == conf_password:
					form.save()
					form = UserForm()
					messages.success(request, "You have been registered successfully !!!")
					return HttpResponseRedirect(reverse('login_user'))
				else:
					form = UserForm()
					error = "Passwords didn't match !!!"
					return render(request, "user_regist.html", {'form':form, 'error':error})
				
		else:
			messages.error(request, form.errors)
			return HttpResponseRedirect(reverse('regist_user'))



class UserController(object):

	def get_user_login_page(self, request):

		log_user = {}
		log_user.update(csrf(request))

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
		return render(request, "user_login.html", log_user)


	def get_user_logout_page(self, request):

		try:
			del request.session['user']
			del request.session['username']
		except KeyError:
			pass
		return HttpResponseRedirect(reverse('home'))


	def get_user_invalid_page(self, request):
		error = "Incorrect Email Address or Password"
		return render(request, "user_login.html", {'error':error})


	def get_user_auth_page(self, request):

		log_email = request.POST.get('log_email', '')
		log_password = request.POST.get('log_password', '')
		user_auth = UserAuth()
		user = user_auth.authenticate_user(email=log_email, password=log_password)

		if user is not None:
			username = user.user_name

			request.session['user'] = user.pk
			request.session['username'] = user.user_name

			return HttpResponseRedirect(reverse('home'))
		else:
			return HttpResponseRedirect(reverse('invalid_user'))

			
	@csrf_exempt
	def load_company_categories_users(self, request):

		if 'username' in request.session:

			if request.method == "POST":

				user = User.objects.get(pk=request.session['user'])
				category = request.POST.get('category', '')
				category = CompanyCategories.objects.get(pk=category)

				if user.pk not in category.get_category_users_list():
					user_like = UserCategories(
							user=User.objects.get(pk=user.pk),
							category=CompanyCategories.objects.get(pk=category.pk),
							follow_date=timezone.now()
						)
					user_like.save()

					return HttpResponse("ok")
				else:
					return HttpResponse("liked")
			else:

				template = "includes/company_categories.html"
				categories = CompanyCategories.objects.all()

				return render_to_response(template, {
							'categories':categories,
							'session_user': request.session['username'],
							'user': User.objects.get(pk=request.session['user'])
							})
		else:
			return HttpResponse("<p class='xl-error'>ONLY FOR USERS</p>")


	def load_company_category_users(self, request, category):

		if 'username' in request.session:

			template = "includes/company_category.html"
			session_user = request.session['username']
			session_id = request.session['user']

			category = CompanyCategories.objects.get(pk=category)
			categories = CompanyCategories.objects.all();

			category_render = {}
			category_render.update(csrf(request))
			category_render['session_user'] = session_user
			category_render['session_profile'] = User.objects.get(pk=session_id)
			category_render['category'] = category
			category_render['categories'] = categories
			category_render['companies'] = Company.objects.filter(category__pk=category.pk)

			return render(request, template, category_render)
		else:
			messages.error(request, "Login as User !!!")
			return HttpResponseRedirect(reverse('home'))


	def get_user_profile(self, request, user_name):

		template = "user.html"
		user = get_object_or_404(User, user_name=user_name)
		user_render = {}

		if 'username' in request.session:

			session_user = request.session['username']
			session_id = request.session['user']
			companies = Company.objects.all()
			followed_company = Followers.objects.filter(user=session_id)
			products_company = Products.objects.all().count()
			check_follow = UserFollow.objects.filter(follower_user=session_id, following=user.pk)

			user_render['session_user'] = session_user
			user_render['profile_image_form'] = UserProfileImage()
			user_render['cover_image_form'] = UserCoverImage()
			user_render['update_user_profile'] = UpdateUserProfile(instance=User.objects.get(pk=session_id))
			user_render['companies_may_know'] = companies
			user_render['followed_company'] = followed_company
			user_render['products_company'] = products_company
			user_render['post_form'] = PostForm()
			user_render['session_profile'] = User.objects.get(pk=session_id)
			user_render['check_follow'] = check_follow

		elif 'company_name' in request.session:

			session_company = request.session['company_name']
			session_id = request.session['pk']
			company = Company.objects.get(pk=session_id)
			product_form = ProductForm()
			categories = Categories.objects.filter(company=company.pk)

			user_render['session_company'] = session_company
			user_render['company'] = company
			user_render['product_form'] = product_form
			user_render['categories'] = categories
			user_render['sum_categories'] = get_categories(request, session_id)
			user_render['post_form'] = PostForm()


		posts_all = Posts.objects.filter(user=user.pk).order_by('-posted_date')
		paginator = Paginator(posts_all, settings.PAGINATOR_ITEMS)
		page = request.GET.get('page')
			
		try:
			posts = paginator.page(page)
		except PageNotAnInteger:
			posts = paginator.page(1)
		except EmptyPage:
			posts = paginator.page(paginator.num_pages)

		user_render['user_posts'] = posts
		user_render['user'] = user

		return render(request, template, user_render)


	def update_user_cover_image(self, request):

		username = request.session['username']
		user = request.session['user']

		if request.method == 'POST':

			cover_image_form = UserCoverImage(request.POST, request.FILES)
			if cover_image_form.is_valid():
				user = User.objects.get(pk=user)
				user.cover_image = cover_image_form.cleaned_data['cover_image']
				user.save()
				cover_image_form = UserCoverImage()
				messages.success(request, "Cover Image Updated Successfully !!!")
				return HttpResponseRedirect(reverse('user_profile', kwargs={'user_name':username}))
			else:
				messages.error(request, cover_image_form.errors)
				return HttpResponseRedirect(reverse('user_profile', kwargs={'user_name':username}))

		return HttpResponseRedirect(reverse('user_profile', kwargs={'user_name':username}))


	def update_user_profile_image(self, request):

		username = request.session['username']
		user = request.session['user']

		if request.method == 'POST':
			profile_image_form = UserProfileImage(request.POST, request.FILES)

			if profile_image_form.is_valid():
				user = User.objects.get(pk=user)
				user.profile_image = profile_image_form.cleaned_data['profile_image']
				user.save()
				profile_image_form = UserProfileImage()
				messages.success(request, "Profile Image Updated Successfully !!!")
				
				return HttpResponseRedirect(reverse('user_profile', kwargs={'user_name':username}))
			else:
				messages.error(request, profile_image_form.errors)
				return HttpResponseRedirect(reverse('user_profile', kwargs={'user_name':username}))

		return HttpResponseRedirect(reverse('user_profile', kwargs={'user_name':username}))


	def update_user_profile(self, request):

		if 'username' in request.session:

			username = request.session['username']
			user_id = request.session['user']

			if request.method == 'POST':
				update_user_profile = UpdateUserProfile(request.POST)

				if update_user_profile.is_valid():
					user = User.objects.get(pk=user_id)
					user.full_name = update_user_profile.cleaned_data['full_name']
					user.country = update_user_profile.cleaned_data['country']
					user.town = update_user_profile.cleaned_data['town']
					user.phone_number = update_user_profile.cleaned_data['phone_number']
					user.biography = update_user_profile.cleaned_data['biography']
					user.save()

					update_user_profile = UpdateUserProfile()
					messages.success(request, "User Profile Updated Successfully !!!")
					return HttpResponseRedirect(reverse('user_profile', kwargs={'user_name':username}))
				else:
					messages.error(request, update_user_profile.errors)
					return HttpResponseRedirect(reverse('user_profile', kwargs={'user_name':username}))

			else:

				template = "includes/update_user.html"
				user_render = {}
				user_render.update(csrf(request))
				user_render['update_user_profile'] = UpdateUserProfile(instance=User.objects.get(pk=user_id))

				return render(request, template, user_render)
		else:
			messages.error(request, "Login Please !!!")
			return HttpResponseRedirect(reverse('home'))


	def add_address(self, request):

		if 'username' in request.session:
			if request.method == "POST":

				longitude = request.POST.get('longitude', '')
				latitude = request.POST.get('latitude', '')
				address = request.POST.get('address', '')
				user = User.objects.get(pk=request.session['user'])

				if user.get_user_address() is None:
					address_obj = Address(
							user=User.objects.get(pk=request.session['user']),
							address=address,
							latitude=latitude,
							longitude=longitude,
							added_date=timezone.now()
						)
					address_obj.save()
					
					return HttpResponse("ok")
				else:
					return HttpResponse("Cant Add Another Address")
			else:

				template = "includes/add_address.html"
				user_render = {}
				user_render['session_user'] = request.session['username']
				user_render.update(csrf(request))
				return render(request, template, user_render)

		elif filter_company_sessions(request) is not None:

			if request.method == "POST":

				longitude = request.POST.get('longitude', '')
				latitude = request.POST.get('latitude', '')
				address = request.POST.get('address', '')

				address_obj = Address(
						company=Company.objects.get(pk=request.session['pk']),
						address=address,
						latitude=latitude,
						longitude=longitude,
						added_date=timezone.now()
					)
				address_obj.save()
				
				return HttpResponse("ok")
			else:

				template = "includes/add_address.html"
				company_render = {}
				company_render['session_company'] = request.session['company_name']
				company_render.update(csrf(request))
				return render(request, template, company_render)
		else:
			return HttpResponseRedirect(reverse('home'))


	def get_user_following_page(self, request, user_name):

		template = "userfollowing.html"
		user = get_object_or_404(User, user_name=user_name)
		following_render = {}

		if 'username' in request.session:

			session_user = request.session['username']
			session_id = request.session['user']
			products_company = Products.objects.all().count()
			follow_users = User.objects.all()
			check_follow = UserFollow.objects.filter(follower_user=session_id, following=user.pk)

			following_render['session_user'] = session_user
			following_render['profile_image_form'] = UserProfileImage()
			following_render['cover_image_form'] = UserCoverImage()
			following_render['update_user_profile'] = UpdateUserProfile(instance=User.objects.get(pk=session_id))
			following_render['follow_users'] = follow_users
			following_render['products_company'] = products_company
			following_render['post_form'] = PostForm()
			following_render['session_profile'] = User.objects.get(pk=session_id)
			following_render['check_follow'] = check_follow

		elif 'company_name' in request.session:

			session_company = request.session['company_name']
			session_id = request.session['pk']
			company = Company.objects.get(pk=session_id)
			product_form = ProductForm()
			categories = Categories.objects.filter(company=company.pk)

			following_render['session_company'] = session_company
			following_render['company'] = company
			following_render['product_form'] = product_form
			following_render['categories'] = categories
			following_render['sum_categories'] = get_categories(request, session_id)
			following_render['post_form'] = PostForm()

		following_render['followers'] = UserFollow.objects.filter(follower_user=user.pk).order_by('-follow_date')
		following_render['user'] = user

		return render(request, template, following_render)


	def get_user_followers_page(self, request, user_name):

		template = "userfollowers.html"
		user = get_object_or_404(User, user_name=user_name)
		followers_render = {}

		if 'username' in request.session:

			session_user = request.session['username']
			session_id = request.session['user']
			products_company = Products.objects.all().count()
			follow_users = User.objects.all()
			check_follow = UserFollow.objects.filter(follower_user=session_id, following=user.pk)

			followers_render['session_user'] = session_user
			followers_render['profile_image_form'] = UserProfileImage()
			followers_render['cover_image_form'] = UserCoverImage()
			followers_render['update_user_profile'] = UpdateUserProfile(instance=User.objects.get(pk=session_id))
			followers_render['follow_users'] = follow_users
			followers_render['products_company'] = products_company
			followers_render['post_form'] = PostForm()
			followers_render['session_profile'] = User.objects.get(pk=session_id)
			followers_render['check_follow'] = check_follow

		elif 'company_name' in request.session:

			session_company = request.session['company_name']
			session_id = request.session['pk']
			company = Company.objects.get(pk=session_id)
			product_form = ProductForm()
			categories = Categories.objects.filter(company=company.pk)

			followers_render['session_company'] = session_company
			followers_render['company'] = company
			followers_render['product_form'] = product_form
			followers_render['categories'] = categories
			followers_render['sum_categories'] = get_categories(request, session_id)
			followers_render['post_form'] = PostForm()

		followers_render['followers'] = UserFollow.objects.filter(following=user.pk).order_by('-follow_date')
		followers_render['user'] = user

		return render(request, template, followers_render)


	def user_follow_user(self, request):

		if request.method == 'POST':

			user = request.POST.get('user', '')
			user_to_follow = User.objects.get(pk=user)

			if 'username' in request.session:
				session_id = request.session['user']

				if user != session_id:
					check_follow = UserFollow.objects.filter(follower_user=session_id, following=user)
					if check_follow:

						return HttpResponse('already')
					else:
						follow_user = UserFollow(
								following=User.objects.get(pk=user),
								follower_user=User.objects.get(pk=session_id),
								follow_date=timezone.now()
							)
						follow_user.save()

						saveUserNotificationFromUser(
							request,
							User.objects.get(pk=session_id),
							User.objects.get(pk=user_to_follow.pk),
							user_to_follow.pk,
							'follow'
						)

						return HttpResponse('success')

		return HttpResponse('cool')


	def get_user_companies_page(self, request, user_name):

		template = "usercompanies.html"
		user = get_object_or_404(User, user_name=user_name)
		companies_render = {}

		if 'username' in request.session:

			session_user = request.session['username']
			session_id = request.session['user']
			companies = Company.objects.all()
			followed_company = Followers.objects.filter(user=session_id)
			products_company = Products.objects.all().count()
			check_follow = UserFollow.objects.filter(follower_user=session_id, following=user.pk)

			companies_render['session_user'] = session_user
			companies_render['profile_image_form'] = UserProfileImage()
			companies_render['cover_image_form'] = UserCoverImage()
			companies_render['update_user_profile'] = UpdateUserProfile(instance=User.objects.get(pk=session_id))
			companies_render['companies_may_know'] = companies
			companies_render['followed_company'] = followed_company
			companies_render['products_company'] = products_company
			companies_render['post_form'] = PostForm()
			companies_render['session_profile'] = User.objects.get(pk=session_id)
			companies_render['check_follow'] = check_follow

		elif 'company_name' in request.session:

			session_company = request.session['company_name']
			session_id = request.session['pk']
			company = Company.objects.get(pk=session_id)
			product_form = ProductForm()
			categories = Categories.objects.filter(company=company.pk)

			companies_render['session_company'] = session_company
			companies_render['company'] = company
			companies_render['product_form'] = product_form
			companies_render['categories'] = categories
			companies_render['sum_categories'] = get_categories(request, session_id)
			companies_render['post_form'] = PostForm()

		companies_render['user_companies'] = Followers.objects.filter(user=user.pk)
		companies_render['user'] = user

		return render(request, template, companies_render)


	def get_user_interess_page(self, request, user_name):

		template = "userinteress.html"
		user = get_object_or_404(User, user_name=user_name)
		interess_render = {}

		if 'username' in request.session:

			session_user = request.session['username']
			session_id = request.session['user']
			companies = Company.objects.all()
			followed_company = Followers.objects.filter(user=session_id)
			products_company = Products.objects.all().count()
			check_follow = UserFollow.objects.filter(follower_user=session_id, following=user.pk)

			interess_render['session_user'] = session_user
			interess_render['profile_image_form'] = UserProfileImage()
			interess_render['cover_image_form'] = UserCoverImage()
			interess_render['update_user_profile'] = UpdateUserProfile(instance=User.objects.get(pk=session_id))
			interess_render['companies_may_know'] = companies
			interess_render['followed_company'] = followed_company
			interess_render['products_company'] = products_company
			interess_render['post_form'] = PostForm()
			interess_render['session_profile'] = User.objects.get(pk=session_id)
			interess_render['check_follow'] = check_follow

		elif 'company_name' in request.session:
			
			session_company = request.session['company_name']
			session_id = request.session['pk']
			company = Company.objects.get(pk=session_id)
			product_form = ProductForm()
			categories = Categories.objects.filter(company=company.pk)

			interess_render['session_company'] = session_company
			interess_render['company'] = company
			interess_render['product_form'] = product_form
			interess_render['categories'] = categories
			interess_render['sum_categories'] = get_categories(request, session_id)
			interess_render['post_form'] = PostForm()
			interess_render['trades'] = ProductTrade.objects.filter(user=user.pk, product__company=company.pk).order_by('-started_date')

		interess_render['interesses'] = ProductInteress.objects.filter(user=user.pk).order_by('-interess_date')
		interess_render['user'] = user

		return render(request, template, interess_render)


	def get_user_bills_and_carts(self, request):
		if 'username' in request.session:
			template = "includes/user_bills_carts.html"
			session_user = request.session['username']
			session_id = request.session['user']
			
			ubc_render = {}
			ubc_render.update(csrf(request))

			ubc_render["session_user"] = session_user
			ubc_render["bills_carts"] = ms_get_user_bills_and_carts(session_id)
			ubc_render['companies'] = Company.objects.all()

			return render(request, template, ubc_render)
		else:
			return HttpResponse("User Session Required")


	def get_user_bills_and_carts_company(self, request, company):
		if 'username' in request.session:
			template = "includes/user_bills_carts_company.html"
			session_user = request.session['username']
			session_id = request.session['user']

			company = get_object_or_404(Company, pk=company)
			data = ms_get_user_bills_and_carts_company(session_id, company.pk)

			ubc_render = {}
			ubc_render.update(csrf(request))
			ubc_render['session_user'] = session_user
			ubc_render['session_profile'] = User.objects.get(pk=session_id)
			ubc_render['bills_carts'] = ms_get_user_bills_and_carts(session_id)
			ubc_render['company'] = company
			ubc_render['check_follow'] = Followers.objects.filter(user=session_id, company=company.pk)
			ubc_render['bills'] = data['bills']
			ubc_render['carts'] = data['carts']
			ubc_render['sum_bills'] = data['sum_bills']
			ubc_render['sum_carts'] = data['sum_carts']

			return render(request, template, ubc_render)
		else:
			messages.error(request, "User Session Required")
			return HttpResponseRedirect(reverse('home'))
