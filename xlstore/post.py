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


class PostController(object):

	helper = Helpers()

	def get_users_posts(self, request):

		user = request.session['user']
		user = User.objects.get(pk=user)
		posts = []

		if user.get_sum_posts() > 0:
			_user_posts = Posts.objects.filter(user=user.pk).order_by('-posted_date')
			if _user_posts is not None:
				for _post in _user_posts:
					posts.append(_post)

		if user.get_sum_companies() > 0:
			for _company in user.get_companies():
				_posts = Posts.objects.filter(company=_company.company.pk).order_by('-posted_date')
				if _posts is  not None:
					for post in _posts:
						posts.append(post)

		if user.get_sum_following() > 0:
			for _user in user.get_following():
				_posts = Posts.objects.filter(user=_user.following.pk).order_by('-posted_date')
				if _posts is not None:
					for post in _posts:
						posts.append(post)

		if user.get_sum_followers() > 0:
			for _user in user.get_followers():
				_posts = Posts.objects.filter(user=_user.follower_user.pk).order_by('-posted_date')
				if _posts is not None:
					for post in _posts:
						posts.append(post)


		return sorted(set(posts), key=lambda post: post.posted_date, reverse=True)


	def get_companies_posts(self, request):

		company = request.session['pk']
		company = Company.objects.get(pk=company)
		posts = []

		if company.get_sum_posts() > 0:
			_posts = Posts.objects.filter(company=company.pk).order_by('-posted_date')
			for _post in _posts:
				posts.append(_post)

		if company.get_sum_followers() > 0:
			for _user in company.get_followers():
				_posts = Posts.objects.filter(user=_user.user.pk).order_by('-posted_date')
				if _posts is not None:
					for _post in _posts:
						posts.append(_post)

		return sorted(set(posts), key=lambda post: post.posted_date, reverse=True)


	def get_posts_page(self, request):

		if 'company_name' in request.session:
			company_name = request.session['company_name']
			company_id = request.session['pk']
			product_form = ProductForm()
			category_form = CategoryForm()
			product_category = Categories.objects.all()
			posts_all = self.get_companies_posts(request)

			paginator = Paginator(posts_all, settings.PAGINATOR_ITEMS)
			page = request.GET.get('page')
			
			try:
				posts = paginator.page(page)
			except PageNotAnInteger:
				posts = paginator.page(1)
			except EmptyPage:
				posts = paginator.page(paginator.num_pages)

			posts_render = {
				'company': Company.objects.get(name_dotted = company_name),
				'session_company': company_name,
				'sum_categories': get_categories(request, company_id),
				'product_form':product_form,
				'category_form':category_form,
				'product_category':product_category,
				'categories': Categories.objects.filter(company=company_id),
				'post_form':PostForm(),
				'posts':posts,
			}
			
		elif 'username' in request.session:
			
			session_user = request.session['username']
			user = User.objects.get(user_name=session_user)
			post_form = PostForm()
			product_category = Categories.objects.all()
			companies = Company.objects.all()
			posts_all = self.get_users_posts(request)
			follow_users = User.objects.all()

			paginator = Paginator(posts_all, settings.PAGINATOR_ITEMS)
			page = request.GET.get('page')
			
			try:
				posts = paginator.page(page)
			except PageNotAnInteger:
				posts = paginator.page(1)
			except EmptyPage:
				posts = paginator.page(paginator.num_pages)

			posts_render = {
				'session_user':session_user,
				'user':user,
				'post_form':post_form,
				'companies_may_know':companies,
				'product_category':product_category,
				'session_profile': User.objects.get(pk=request.session['user']),
				'posts':posts,
				'follow_users':follow_users,
			}
		else:
			product_category = Categories.objects.all()
			posts_all = Posts.objects.all().order_by('-posted_date')

			paginator = Paginator(posts_all, settings.PAGINATOR_ITEMS)
			page = request.GET.get('page')
			
			try:
				posts = paginator.page(page)
			except PageNotAnInteger:
				posts = paginator.page(1)
			except EmptyPage:
				posts = paginator.page(paginator.num_pages)

			posts_render = {
				'product_category':product_category,
				'posts':posts,
				'category_comp': Company.objects.all()
			}
		return render(request, "posts.html", posts_render)


	def add_post(self, request):

		template = 'includes/add_post.html'
		users = [user.get_user_tag_json() for user in User.objects.all()]
		companies = [company.get_company_tag_json() for company in Company.objects.all()]
		products = [product.get_product_tag_json() for product in Products.objects.all()]
		user_comps = users + companies + products

		if 'username' in request.session:
			post_render = {}
			post_render.update(csrf(request))
			post_render['post_form'] = PostForm()
			post_render['session_user'] = request.session['username']
			post_render['all_tags'] = json.dumps(user_comps, default=str)

			return render(request, template, post_render)

		elif 'company_name' in request.session:
			products_comp = [product.get_product_tag_json() for product in Products.objects.filter(company=request.session['pk'])]
			all_tags = users + products_comp
			post_render = {}
			post_render.update(csrf(request))
			post_render['post_form'] = PostForm()
			post_render['session_company'] = request.session['company_name']
			post_render['users'] = json.dumps(all_tags, default=str)

			return render(request, template, post_render)


	def save_tagged_users_notification(self, request, post_text, post_id):
		
		data = self.helper.get_linked_post_text(post_text)
		users = set(data['users'])
		companies = set(data['companies'])
		products = set(data['products'])

		if len(users) > 0:
			for user in users:
				if 'username' in request.session:
					saveUserNotificationFromUser(
							request,
							User.objects.get(pk=request.session['user']),
							User.objects.get(pk=user['pk']),
							post_id,
							'user_tagged',
						)
				elif 'company_name' in request.session:
					saveUserNotificationFromCompany(
							request,
							Company.objects.get(pk=request.session['pk']),
							User.objects.get(pk=user['pk']),
							post_id,
							'user_tagged'
						)

		if len(companies) > 0:
			for company in companies:
				if 'username' in request.session:
					saveCompanyNotificationFromUser(
							request,
							User.objects.get(pk=request.session['user']),
							Company.objects.get(pk=company['pk']),
							post_id,
							'company_tagged'
						)

		if len(products) > 0:
			for product in products:
				if 'username' in request.session:
					saveCompanyNotificationFromUser(
							request,
							User.objects.get(pk=request.session['user']),
							Company.objects.get(name_dotted=product['company']),
							post_id,
							'company_product_tagged'
						)


	def save_post(self, request):
		if request.method == 'POST':
			
			post_form = PostForm(request.POST, request.FILES)
			post_text = request.POST.get('post_text','')
			data = self.helper.get_linked_post_text(post_text)
			
			if 'username' in request.session:
				
				session_user = request.session['username']
				session_id = request.session['user']
				
				if post_form.is_valid():
					post = post_form.save(commit=False)
					post.user = User.objects.get(pk=session_id)
					post.post_text = data['text']
					post.poster_type = 'user'
					post.posted_date = timezone.now()
					
					post.save()
					self.save_tagged_users_notification(request, post_text, post.pk)
					
					post_form = PostForm()
					messages.success(request, "Post Published Successfully !!!")

					return HttpResponseRedirect(reverse('user_profile', kwargs={'user_name':session_user}))
				else:
					messages.error(request, post_form.errors)
					return HttpResponseRedirect(reverse('user_profile', kwargs={'user_name':session_user}))
			
			elif filter_company_sessions(request) is not None:
				session_company = request.session['company_name']
				session_id = request.session['pk']

				if post_form.is_valid():
						
					post = post_form.save(commit=False)
					post.company = Company.objects.get(pk=session_id)
					post.post_text = data['text']
					post.poster_type = 'company'
					post.posted_date = timezone.now()
						
					post.save()
					self.save_tagged_users_notification(request, post_text, post.pk)
						
					post_form = PostForm()
					messages.success(request, "Post Published Successfully !!!")

					return HttpResponseRedirect(reverse('comp_profile', kwargs={'company_name':session_company}))
				else:
					messages.error(request, post_form.errors)
					return HttpResponseRedirect(reverse('comp_profile', kwargs={'company_name':session_company}))

			else:
				messages.error(request, "Sorry, You're not The Admin")
				return HttpResponseRedirect(reverse('comp_profile', kwargs={'company_name':session_company}))

		return HttpResponseRedirect(reverse('home_simple'))


	def get_edit_post(self, request, post_id):

		template = "includes/edit_post.html"
		post = get_object_or_404(Posts, pk=post_id)
		post_render = {}
		not_owner = 0
		if post.poster_type == 'company':
			if filter_company_sessions(request) is not None:
				if post.company.pk == request.session['pk']:
					not_owner = 1
					post_render['post'] = post
					post_render['session_company'] = request.session['company_name']
					post_render['edit_post_form'] = EditPost(instance=Posts.objects.get(pk=post_id))
				else:
					not_owner = 0
			else:
				not_owner = 0

		elif post.poster_type == 'user':
			if 'username' in request.session:
				if post.user.pk == request.session['user']:
					not_owner = 2
					post_render['post'] = post
					post_render['session_user'] = request.session['username']
					post_render['edit_post_form'] = EditPost(instance=Posts.objects.get(pk=post_id))
				else:
					not_owner = 0
			else:
				not_owner = 0

		post_render['not_owner'] = not_owner

		return render(request, template, post_render)


	def save_edit_post(self, request, post_id):

		if request.method == 'POST':
			edit_post = EditPost(request.POST)
			if edit_post.is_valid():
				post = Posts.objects.get(pk=post_id)
				post.post_text = edit_post.cleaned_data['post_text']
				post.save()

				edit_post_form = EditPost(instance=Posts.objects.get(pk=post_id))
				return HttpResponse("success")
			else:
				return HttpResponse('error')

		return HttpResponse("cool")


	def delete_post(self, request, post_id):

		if request.method == 'POST':
			post_id = request.POST.get('post', '')
			post = Posts.objects.get(pk=post_id)
			if 'username' in request.session:
				if post.poster_type == 'user':
					if post.user.pk == request.session['user']:
						post.is_deleted = True
						post.save()
						return HttpResponse("success")
			elif filter_company_sessions(request) is not None:
				if post.poster_type == 'company':
					if post.company.pk == request.session['pk']:
						post.is_deleted = True
						post.save()
						return HttpResponse('success')

		return HttpResponse('cool')


	def user_like_dislike_post(self, request):
		if request.method == 'POST':
			post = request.POST.get('post', '')
			mention = request.POST.get('mention', '')
			post_obj = Posts.objects.get(pk=post)
			if 'username' in request.session:
				session_id = request.session['user']
				check_mention = PostMention.objects.filter(post=post_obj.pk, mentioner=session_id)
				if check_mention:
					for this_mention in check_mention:
						mention_post = PostMention.objects.get(pk=this_mention.pk)
						mention_post.mention = mention
						mention_post.mention_date = timezone.now()
						mention_post.save()
					return HttpResponse('success')
				else:
					mention_post = PostMention(
							post=Posts.objects.get(pk=post),
							mentioner=User.objects.get(pk=session_id),
							mention=mention,
							mention_date=timezone.now()
						)
					mention_post.save()
					if post_obj.poster_type == 'user':
						saveUserNotificationFromUser(
								request,
								User.objects.get(pk=session_id),
								User.objects.get(pk=post_obj.user.pk),
								post_obj.pk,
								mention
							)
					elif post_obj.poster_type == 'company':
						saveCompanyNotificationFromUser(
								request,
								User.objects.get(pk=session_id),
								Company.objects.get(pk=post_obj.company.pk),
								post_obj.pk,
								mention
							)
					return HttpResponse('success')

		return HttpResponse('cool')


	def get_single_post_ajax(self, request, post_id):

		template = 'postajax.html'
		post_render = {}
		if 'username' in request.session:
			session_user = request.session['username']
			session_id = request.session['user']
			user = User.objects.get(pk=session_id)

			post_render['session_user'] = session_user
			post_render['user'] = user
		elif 'company_name' in request.session:
			session_company = request.session['company_name']
			session_id = request.session['pk']
			company = Company.objects.get(pk=session_id)

			post_render['session_company'] = session_company
			post_render['company'] = company

		post = get_object_or_404(Posts, pk=post_id)
		post_render['post'] = post
		post_render['post_reply_form'] = PostReplyForm()

		return render(request, template, post_render)