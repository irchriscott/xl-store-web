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


class ProductCommentController(object):

	def product_add_comment(self, request):

		if request.method == 'POST':

			text = request.POST.get('text', '')
			product_id = request.POST.get('product', '')
			product = Products.objects.get(pk=product_id)

			if filter_company_sessions(request) is not None:
				company_id = request.session['pk']
				if product.company.pk == company_id:
					commenter = 'company'
					comment = ProductComments(
							product=Products.objects.get(pk=product_id),
							company=Company.objects.get(pk=company_id),
							commenter=commenter,
							comment=text,
							comment_date=timezone.now()
						)
					comment.save()

					return HttpResponse('success')

			elif 'username' in request.session:

				commenter = 'user'
				session_id = request.session['user']
				comment = ProductComments(
							product=Products.objects.get(pk=product_id),
							user=User.objects.get(pk=session_id),
							commenter=commenter,
							comment=text,
							comment_date=timezone.now()
						)

				comment.save()

				saveCompanyNotificationFromUser(
						request,
						User.objects.get(pk=session_id),
						Company.objects.get(pk=product.company.pk),
						product.pk,
						'comment'
					)

				return HttpResponse('success')

		return HttpResponse('cool')


	def get_edit_product_comment(self, request, comment_id):

		template = "includes/edit_product_comment.html"
		comment = get_object_or_404(ProductComments, pk=comment_id)
		product = get_object_or_404(Products, pk=comment.product.pk)

		not_owner = 0
		comment_context = {}

		if 'username' in request.session:
			if comment.commenter == 'user':
				if comment.user.pk == request.session['user']:
					not_owner = 1
					comment_context['comment_edit_form'] = ProductCommentForm(instance=ProductComments.objects.get(pk=comment_id))

		elif filter_company_sessions(request) is not None:
			
			if comment.commenter == 'company':
				if comment.company.pk == request.session['pk']:
					not_owner = 1
					comment_context['comment_edit_form'] = ProductCommentForm(instance=ProductComments.objects.get(pk=comment_id))
				else:
					not_owner = 0

		comment_context['comment'] = comment
		comment_context['product'] = product
		comment_context['not_owner'] = not_owner

		return render(request, template, comment_context)


	def edit_product_comment(self, request, comment_id):

		if request.method == 'POST':
			comment_form = ProductCommentForm(request.POST)

			if comment_form.is_valid():
				comment = ProductComments.objects.get(pk=comment_id)
				comment.comment = comment_form.cleaned_data['comment']
				comment.save()

				return HttpResponseRedirect(reverse('home'))


	def delete_product_comment(self, request, comment_id):

		if request.method == 'POST':

			comment_id = request.POST.get('comment', '')
			comment = ProductComments.objects.get(pk=comment_id)

			if 'username' in request.session:
				if comment.commenter == 'user':
					if comment.user.pk == request.session['user']:
						comment.delete()
						return HttpResponse('success')

			elif filter_company_sessions(request) is not None:
				if comment.commenter == 'company':
					if comment.company.pk == request.session['pk']:
						comment.delete()
						return HttpResponse('success')
		return HttpResponse('cool')


	def product_load_comments_main(self, request, product_id):

		template = "includes/comments_main.html"
		comment_render = {}

		if 'company_name' in request.session:
			comment_render['session_company'] = request.session['pk']
		elif 'username' in request.session:
			comment_render['session_user'] = request.session['user']

		comment_render['comments'] = ProductComments.objects.filter(product=product_id).order_by('comment_date')
		comment_render['product'] = Products.objects.get(pk=product_id)

		return render(request, template, comment_render)


	def product_load_comments_else(self, request, product_id):

		template = "includes/comments_else.html"
		comment_render = {}

		if 'company_name' in request.session:
			comment_render['session_company'] = request.session['pk']
		elif 'username' in request.session:
			comment_render['session_user'] = request.session['user']

		comment_render['comments'] = ProductComments.objects.filter(product=product_id).order_by('comment_date')

		return render(request, template, comment_render)