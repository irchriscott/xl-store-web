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


class PostReplyController(object):

	def get_post_reply(self, request, post_id):

		template = "includes/post_reply_form.html"
		post = get_object_or_404(Posts, pk=post_id)
		reply_context = {}

		if 'username' in request.session:
			reply_context['session_user'] = request.session['username']
		elif 'company_name' in request.session:
			reply_context['session_company'] = request.session['company_name']

		reply_context['post'] = post
		reply_context['post_reply_form'] = PostReplyForm()

		return render(request, template, reply_context)


	def save_post_reply(self, request, post_id):

		if request.method == 'POST':

			reply_form = PostReplyForm(request.POST, request.FILES)
			post_obj = Posts.objects.get(pk=post_id)

			if 'username' in request.session:
				session_user = request.session['user']
				if reply_form.is_valid():
					reply = reply_form.save(commit=False)
					reply.post = Posts.objects.get(pk=post_id)
					reply.user = User.objects.get(pk=session_user)
					reply.reply_type = 'user'
					reply.reply_date = timezone.now()
					reply.save()

					if post_obj.poster_type == 'user':

						saveUserNotificationFromUser(
							request,
							User.objects.get(pk=session_user),
							User.objects.get(pk=post_obj.poster.pk),
							post_obj.pk,
							"reply"
						)
						return HttpResponse('success')

					elif post_obj.poster_type == 'company':
						saveCompanyNotificationFromUser(
							request,
							User.objects.get(pk=session_user),
							Company.objects.get(pk=post_obj.company.pk),
							post_obj.pk,
							"reply"
						)
						return HttpResponse('success')

					return HttpResponse('success')

			elif filter_company_sessions(request) is not None:

				session_company = request.session['pk']

				if reply_form.is_valid():
					reply = reply_form.save(commit=False)
					reply.post = Posts.objects.get(pk=post_id)
					reply.company = Company.objects.get(pk=session_company)
					reply.reply_type = 'company'
					reply.reply_date = timezone.now()
					reply.save()

					if post_obj.poster_type == 'user':

						saveUserNotificationFromCompany(
								request,
								Company.objects.get(pk=session_company),
								User.objects.get(pk=post_obj.poster.pk),
								post_obj.pk,
								'reply'
							)
						return HttpResponse('success')	
					
		return HttpResponse('cool')


	def load_post_replies(self, request, post_id):

		template = "includes/post_replies.html"
		replies_render = {}

		if 'username' in request.session:

			replies_render['session_user'] = request.session['username']
			replies_render['user'] = User.objects.get(pk=request.session['user'])

		elif 'company_name' in request.session:

			replies_render['session_company'] = request.session['company_name']
			replies_render['company'] = Company.objects.get(pk=request.session['pk'])

		replies_render['replies'] = PostReplies.objects.filter(post=post_id).order_by('-reply_date')
		replies_render['post'] = Posts.objects.get(pk=post_id)

		return render(request, template, replies_render)


	def delete_post_reply(self, request, reply_id):

		if request.method == 'POST':

			reply_id = request.POST.get('reply', '')
			reply = PostReplies.objects.get(pk=reply_id)

			if 'username' in request.session:

				if reply.reply_type == 'user':
					if reply.user.pk == request.session['user']:
						reply.delete()
						return HttpResponse('success')

			elif filter_company_sessions(request) is not None:

				if reply.reply_type == 'company':
					if reply.company.pk == request.session['pk']:
						reply.delete()

						return HttpResponse('success')

		return HttpResponse('cool')


	def get_edit_post_reply(self, request, reply_id):

		template = "includes/edit_post_reply.html"
		reply = get_object_or_404(PostReplies, pk=reply_id)
		post = get_object_or_404(Posts, pk=reply.post.pk)
		not_owner = 0
		reply_render = {}

		if 'username' in request.session:

			if reply.reply_type == 'user':

				if reply.user.pk == request.session['user']:
					not_owner = 1
					edit_post_reply_form = PostReplyForm(instance=PostReplies.objects.get(pk=reply_id))
					reply_render['edit_post_reply_form'] = edit_post_reply_form
				else:
					not_owner = 0

		elif 'company_name' in request.session:

			if 'company_name' in request.session and 'ms' not in request.session:
				if reply.reply_type == 'company':
					if reply.company.pk == request.session['pk']:
						not_owner = 1
						edit_post_reply_form = PostReplyForm(instance=PostReplies.objects.get(pk=reply_id))
						reply_render['edit_post_reply_form'] = edit_post_reply_form
					else:
						not_owner = 0

			elif 'company_name' in request.session and 'ms' in request.session:
				if 'admin' in request.session:
					if reply.reply_type == 'company':
						if reply.company.pk == request.session['pk']:
							not_owner = 1
							edit_post_reply_form = PostReplyForm(instance=PostReplies.objects.get(pk=reply_id))
							reply_render['edit_post_reply_form'] = edit_post_reply_form
						else:
							not_owner = 0

		reply_render['reply'] = reply
		reply_render['post'] = post
		reply_render['not_owner'] = not_owner

		return render(request, template, reply_render)


	def edit_post_reply(self, request, reply_id):

		if request.method == 'POST':
			edit_reply_form = PostReplyForm(request.POST, request.FILES)

			if edit_reply_form.is_valid():
				reply = PostReplies.objects.get(pk=reply_id)
				reply.reply_text = edit_reply_form.cleaned_data['reply_text']
				reply.save()

		return HttpResponseRedirect(reverse('home'))
