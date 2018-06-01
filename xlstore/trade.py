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


class TradeController(object):

	def start_product_trade(self, request, product_id):

		product = get_object_or_404(Products, pk=product_id)

		if 'username' in request.session:
			session_id = request.session['user']
			check_trade = ProductTrade.objects.filter(user=session_id, product=product.pk).first()
			status = 'started'

			if check_trade:
				return HttpResponseRedirect(reverse('user_single_trade', kwargs={'trade_id':check_trade.pk}))
			else:
				trade = ProductTrade(
						user=User.objects.get(pk=session_id),
						product=Products.objects.get(pk=product.pk),
						status=status,
						started_date=timezone.now()
					)
				trade.save()
				trade_message = ProductTradeMessages(
						trade=ProductTrade.objects.get(pk=trade.pk),
						sender='team',
						receiver='both',
						text_message='started',
						date_time=timezone.now()
					)
				trade_message.save()
				messages.success(request, "Trade Started Successfully !!!")

				return HttpResponseRedirect(reverse('user_all_trades'))


	def get_user_trades(self, request):

		if 'username' in request.session:
			template = "trades_all.html"
			trade_context = {}
			end_status = ('fail', 'success', 'abort')
			trade_context['session_user'] = request.session['username']
			trade_context['session_profile'] = User.objects.get(pk=request.session['user'])
			trade_context['user'] = User.objects.get(pk=request.session['user'])
			trade_context['post_form'] = PostForm()
			trade_context['trades_list'] = ProductTrade.objects.filter(user=request.session['user'], status="started").order_by('-started_date')
			trade_context['end_status'] = end_status

			return render(request, template, trade_context)

		else:
			messages.error(request, "You Must Log In First !!!")
			return HttpResponseRedirect(reverse('login_user'))


	def get_company_trades(self, request):

		if 'company_name' in request.session:
			template = "trades_all.html"
			trade_context = {}
			trade_context['session_company'] = request.session['company_name']
			trade_context['company'] = Company.objects.get(pk=request.session['pk'])
			trade_context['post_form'] = PostForm()
			trade_context['product_form'] = ProductForm()
			trade_context['categories'] = Categories.objects.filter(company=request.session['pk'])
			trade_context['trades_list'] = ProductTrade.objects.filter(product__company=request.session['pk'], status="started").order_by('-started_date')

			return render(request, template, trade_context)
		else:
			messages.error(request, "You Must Log In First !!!")
			return HttpResponseRedirect(reverse('comp_login'))


	def get_user_single_trade(self, request, trade_id):

		template = "trade_chat.html"
		trade = get_object_or_404(ProductTrade, pk= trade_id)

		if 'username' in request.session:
			if request.session['user'] == trade.user.pk:
				trade_context = {}
				end_status = ('fail', 'success', 'abort')

				trade_context['session_user'] = request.session['username']
				trade_context['session_profile'] = User.objects.get(pk=request.session['user'])
				trade_context['user'] = User.objects.get(pk=request.session['user'])
				trade_context['post_form'] = PostForm()
				trade_context['trade'] = trade
				trade_context['end_status'] = end_status

				return render(request, template, trade_context)
			else:
				messages.error(request, "Not Allowed, Cheater!!!")
				return HttpResponseRedirect(reverse('home_simple'))

		return HttpResponseRedirect(reverse('home_simple'))


	def get_company_single_trade(self, request, trade_id):

		template = "trade_chat.html"
		trade = get_object_or_404(ProductTrade, pk= trade_id)

		if filter_company_sessions(request) is not None:
			if request.session['pk'] == trade.product.company.pk:
				trade_context = {}

				trade_context['session_company'] = request.session['company_name']
				trade_context['company'] = Company.objects.get(pk=request.session['pk'])
				trade_context['post_form'] = PostForm()
				trade_context['product_form'] = ProductForm()
				trade_context['categories'] = Categories.objects.filter(company=request.session['pk'])
				trade_context['trade'] = trade

				return render(request, template, trade_context)
			else:
				messages.error(request, "Not Allowed, Cheater!!!")
				return HttpResponseRedirect(reverse('home_simple'))

		return HttpResponseRedirect(reverse('home_simple'))


	def load_trade_messages(self, request, trade_id):

		template = "includes/trade_messages.html"
		trade = get_object_or_404(ProductTrade, pk=trade_id)
		messages_context = {}
		not_owner = 0

		if 'username' in request.session:
			if trade.user.pk == request.session['user']:
				not_owner = 1
				messages_context['session_user'] = request.session['username']

		elif filter_company_sessions(request) is not None:
			if trade.product.company.pk == request.session['pk']:
				not_owner = 1
				messages_context['session_company'] = request.session['company_name']
		else:
			not_owner = 0

		messages_context['not_owner'] = not_owner
		messages_context['messages'] = ProductTradeMessages.objects.filter(trade=trade.pk)

		return render(request, template, messages_context)


	def save_trade_message(self, request, trade_id):

		if request.method == 'POST':

			message_response = {}
			text_message = request.POST.get('message_text', '')
			message_response['message'] = text_message

			trade = ProductTrade.objects.get(pk=trade_id)
			trades_status = ["failed","stopped","succeeded"]

			if trade.status not in trades_status:
				if 'username' in request.session:
					user = User.objects.get(pk=request.session['user'])
					message_response['user'] = user
					trade_message = ProductTradeMessages(
							trade=ProductTrade.objects.get(pk=trade_id),
							sender='user',
							receiver='company',
							text_message=text_message,
							is_read=False,
							date_time=timezone.now()
						)
					trade_message.save()
					
				elif filter_company_sessions(request) is not None:

					company = Company.objects.get(pk=request.session['pk'])
					message_response['company'] = company
					trade_message = ProductTradeMessages(
							trade=ProductTrade.objects.get(pk=trade_id),
							sender='company',
							receiver='user',
							text_message=text_message,
							is_read=False,
							date_time=timezone.now()
						)
					trade_message.save()

			else:
				HttpResponse("Cant send message for trade status is %s" % trade.status)

			return HttpResponse("ok")


	def save_trade_message_images(self, request, trade_id):

		if request.method == 'POST':
			message_response = {}
			files = request.FILES.getlist('images')
			text_message = ''

			trade = ProductTrade.objects.get(pk=trade_id)
			trades_status = ["failed","stopped","succeeded"]

			if trade.status not in trades_status:
				if 'username' in request.session:
					user = User.objects.get(pk=request.session['user'])
					message_response['user'] = user
					for file in files:
						trade_message = ProductTradeMessages(
								trade=ProductTrade.objects.get(pk=trade_id),
								sender='user',
								receiver='company',
								text_message=text_message,
								image_message=file,
								is_read=False,
								date_time=timezone.now()
							)
						trade_message.save()
					
				elif filter_company_sessions(request) is not None:

					company = Company.objects.get(pk=request.session['pk'])
					message_response['company'] = company
					for file in files:
						trade_message = ProductTradeMessages(
								trade=ProductTrade.objects.get(pk=trade_id),
								sender='company',
								receiver='user',
								text_message=text_message,
								image_message=file,
								is_read=False,
								date_time=timezone.now()
							)
						trade_message.save()

			else:
				HttpResponse("Cant send message for trade status is %s" % trade.status)

			return HttpResponse("ok")


	def save_trade_message_location(self, request, trade_id):

		if request.method == 'POST':

			message_response = {}
			longitude = request.POST.get('longitude', '')
			latitude = request.POST.get('latitude', '')
			address = request.POST.get('address', '')
			text_message = ''
			trade = ProductTrade.objects.get(pk=trade_id)
			trades_status = ["failed","stopped","succeeded"]

			if trade.status not in trades_status:

				if 'username' in request.session:

					user = User.objects.get(pk=request.session['user'])
					message_response['user'] = user
					trade_message = ProductTradeMessages(
							trade=ProductTrade.objects.get(pk=trade_id),
							sender='user',
							receiver='company',
							text_message=text_message,
							address=address,
							longitude=longitude,
							latitude=latitude,
							is_read=False,
							date_time=timezone.now()
						)
					trade_message.save()
					
				elif filter_company_sessions(request) is not None:

					company = Company.objects.get(pk=request.session['pk'])
					message_response['company'] = company
					trade_message = ProductTradeMessages(
							trade=ProductTrade.objects.get(pk=trade_id),
							sender='company',
							receiver='user',
							text_message=text_message,
							address=address,
							longitude=longitude,
							latitude=latitude,
							is_read=False,
							date_time=timezone.now()
						)
					trade_message.save()

			else:
				HttpResponse("Cant send message for trade status %s" % trade.status)

			return HttpResponse("ok")


	def user_restart_trade(self, request, trade_id):

		if 'username' in request.session:

			trade = get_object_or_404(ProductTrade, pk=trade_id)

			if trade.check_trade_agreement is not None:
				trade.started_date = timezone.now()
				trade.status = "started"
				trade.save()
				trade_message = ProductTradeMessages(
					trade=ProductTrade.objects.get(pk=trade.pk),
					sender='team',
					receiver='both',
					text_message='started',
					date_time=timezone.now()
					)
				trade_message.save()
				
				messages.success(request, "Trade Has Restarted Successfully !!!")
				return redirect(reverse('user_single_trade', kwargs={'trade_id': trade.pk}))
			else:
				messages.error(request, "The Trade must be agreed at least once !!!")
				return redirect(reverse('user_all_trades'))


	@csrf_exempt
	def change_trade_status(self, request, trade_id):

		if request.method == "POST":

			status = request.POST.get('status','')
			trade = ProductTrade.objects.get(pk=trade_id)
			response = {status, ' ', trade.status}

			if status == "started":
				status_accept = ["stopped"]

				if 'username' in request.session or filter_company_sessions(request) is not None:
					if trade.status in status_accept:
						trade.status = status
						trade.save()
						trade_message = ProductTradeMessages(
							trade=ProductTrade.objects.get(pk=trade.pk),
							sender='team',
							receiver='both',
							text_message=status,
							date_time=timezone.now()
						)
						trade_message.save()
						return HttpResponse("ok")
					else:
						return HttpResponse("Cant change trade status, status is %s " % trade.status)
				else:
					return HttpResponse("login please")

			elif status == "stopped":
				status_accept = ["started"]

				if 'username' in request.session or filter_company_sessions(request) is not None:
					if trade.status in status_accept:
						trade.status = status
						trade.save()
						trade_message = ProductTradeMessages(
							trade=ProductTrade.objects.get(pk=trade.pk),
							sender='team',
							receiver='both',
							text_message=status,
							date_time=timezone.now()
						)
						trade_message.save()
						return HttpResponse("ok")
					else:
						return HttpResponse("Cant change trade status, status is %s " % trade.status)
				else:
					return HttpResponse("login please")

			elif status == "aborted":
				status_accept = ["started","stopped","failed"]

				if 'username' in request.session or filter_company_sessions(request) is not None:
					
					if trade.status in status_accept:
						p_trade_message = ProductTradeMessages.objects.filter(trade=trade.pk)
						for message in p_trade_message:
							message.delete()
						trade.started_date = timezone.now()
						trade.status = "started"
						trade.save()
						trade_message = ProductTradeMessages(
							trade=ProductTrade.objects.get(pk=trade.pk),
							sender='team',
							receiver='both',
							text_message='started',
							date_time=timezone.now()
						)
						trade_message.save()
						return HttpResponse("ok")
					else:
						return HttpResponse("Cant change trade status, status is %s " % trade.status)
				else:
					return HttpResponse("login please")

			elif status == "succeeded":
				status_accept = ["started","stopped"]

				if 'company_name' in request.session:
					
					if trade.status in status_accept:
						trade.status = status
						trade.end_date = timezone.now()
						trade.save()
						trade_message = ProductTradeMessages(
							trade=ProductTrade.objects.get(pk=trade.pk),
							sender='team',
							receiver='both',
							text_message=status,
							date_time=timezone.now()
						)
						trade_message.save()
						return HttpResponse("ok")
					else:
						return HttpResponse("Cant change trade status, status is %s " % trade.status)
				else:
					return HttpResponse("Only Companies can succeed a trade")

			elif status == "failed":
				status_accept = ["started","stopped"]

				if 'username' in request.session or filter_company_sessions(request) is not None:
					
					if trade.status in status_accept:
						trade.status = status
						trade.save()
						trade_message = ProductTradeMessages(
							trade=ProductTrade.objects.get(pk=trade.pk),
							sender='team',
							receiver='both',
							text_message=status,
							date_time=timezone.now()
						)
						trade_message.save()
						return HttpResponse(response)
					else:
						return HttpResponse("Cant change trade status, status is %s " % trade.status)
				else:
					return HttpResponse("login please")

			else:
				return HttpResponse("Wrong Status Sent")
		else:
			return HttpResponse("request error")


	def get_succeeded_company_trades(self, request):

		if 'company_name' in request.session:

			template = 'includes/company_succeeded_trades.html'
			trades = ProductTrade.objects.filter(product__company=request.session['pk'], status="succeeded").values('product').annotate(customers=Count('product'))
			
			return render_to_response(template, {
					'trade_products': trades,
					'session_company':request.session['company_name'],
					'products':Products.objects.filter(company=request.session['pk']),
					'succeeded_products':True
				})
		else:
			return HttpResponse("<p class='xl-error'>FOR COMPANIES ONLY</p>")


	def get_failed_company_trades(self, request):

		if 'company_name' in request.session:
			
			template = 'includes/company_failed_trades.html'
			trades = ProductTrade.objects.filter(product__company=request.session['pk']).exclude(status="succeeded").exclude(status="started").values('product').annotate(customers=Count('product'))
			
			return render_to_response(template, {
					'trade_products': trades,
					'session_company':request.session['company_name'],
					'products':Products.objects.filter(company=request.session['pk']),
					'failed_products':True
				})
		else:
			return HttpResponse("<p class='xl-error'>FOR COMPANIES ONLY</p>")


	def get_customers_succeeded_trade(self, request, product_id):
		
		if 'company_name' in request.session:
			
			template = 'includes/company_succeeded_trades.html'
			product = get_object_or_404(Products, pk=product_id)
			customers = ProductTrade.objects.filter(product=product.pk, status="succeeded").order_by('-started_date')
			
			return render_to_response(template, {
					'product':product,
					'customers': customers,
					'session_company':request.session['company_name'],
					'products':Products.objects.filter(company=request.session['pk']),
					'succeeded_customers':True
				})
		else:
			return HttpResponse("<p class='xl-error'>FOR COMPANIES ONLY</p>")


	def get_customers_failed_trade(self, request, product_id):
		
		if 'company_name' in request.session:
			
			template = 'includes/company_failed_trades.html'
			product = get_object_or_404(Products, pk=product_id)
			customers = ProductTrade.objects.filter(product=product.pk).exclude(status="succeeded").exclude(status="started").order_by('-started_date')
			
			return render_to_response(template, {
					'product':product,
					'customers': customers,
					'session_company':request.session['company_name'],
					'products':Products.objects.filter(company=request.session['pk']),
					'failed_customers':True
				})
		else:
			return HttpResponse("<p class='xl-error'>FOR COMPANIES ONLY</p>")


	@csrf_exempt
	def get_trades_products_company(self, request, trade_id):

		if 'company_name' in request.session:
			
			template = "includes/product_trades.html"
			trades = ProductTrade.objects.filter(product__company=request.session['pk']).values('product').annotate(customers=Count('product'))
			trade = ProductTrade.objects.get(pk=trade_id)
			
			return render_to_response(template, {
					'trade_products': trades,
					'company':Company.objects.get(pk=request.session['pk']),
					'session_company':request.session['company_name'],
					'products':Products.objects.filter(company=request.session['pk']),
					'trade':trade,
				})
		else:
			return HttpResponse("<p class='xl-error'>FOR COMPANIES ONLY</p>")


	def get_trades_customers(self, request, product_id, trade_id):
		
		if 'company_name' in request.session:
			
			template = "includes/user_trades.html"
			product = get_object_or_404(Products, pk=product_id)
			customers = ProductTrade.objects.filter(product=product.pk).order_by('-started_date')
			trade = ProductTrade.objects.get(pk=trade_id)
			
			return render_to_response(template, {
					'product':product,
					'session_company':request.session['company_name'],
					'customers':customers,
					'trade':trade,
				})
		else:
			return HttpResponse("<p class='xl-error'>FOR COMPANIES ONLY</p>")


	def get_trades_company_users(self, request, trade_id):

		if 'username' in request.session:
			
			template = "includes/company_trades.html"
			trades = ProductTrade.objects.filter(user=request.session['user']).values('product__company').annotate(products=Count('product__company'))
			trade = ProductTrade.objects.get(pk=trade_id)
			
			return render_to_response(template, {
					'trade_companies': trades,
					'user':User.objects.get(pk=request.session['user']),
					'session_user':request.session['username'],
					'companies':Company.objects.all(),
					'trade':trade
				})
		else:
			return HttpResponse("<p class='xl-error'>FOR USERS ONLY</p>")


	def get_trades_products_users(self, request, company_id, trade_id):
		
		if 'username' in request.session:
			
			template = "includes/prodcomp_trades.html"
			company = Company.objects.get(pk=company_id)
			products = ProductTrade.objects.filter(product__company=company.pk, user=request.session['user']).order_by('-started_date')
			trade = ProductTrade.objects.get(pk=trade_id)
			
			return render_to_response(template, {
					'company':company,
					'products':products,
					'session_user':request.session['username'],
					'trade':trade
				})
		else:
			return HttpResponse("<p class='xl-error'>FOR USERS ONLY</p>")


	def get_succeeded_user_trades(self, request):
		
		if 'username' in request.session:
			
			template = "includes/user_succeeded_trades.html"
			trades = ProductTrade.objects.filter(user=request.session['user'], status="succeeded").values('product__company').annotate(products=Count('product__company'))
			
			return render_to_response(template, {
					'trade_companies':trades,
					'user':User.objects.get(pk=request.session['user']),
					'session_user':request.session['username'],
					'companies':Company.objects.all(),
					'succeeded_trades':True
				})
		else:
			return HttpResponse("<p class='xl-error'>FOR USERS ONLY</p>")


	def get_succeeded_products_trades(self, request, company_id):

		if 'username' in request.session:
			
			template = "includes/user_succeeded_trades.html"
			company = Company.objects.get(pk=company_id)
			products = ProductTrade.objects.filter(product__company=company.pk, user=request.session['user'], status="succeeded").order_by('-started_date')
			products_agreed = TradeAgreements.objects.filter(trade__product__company=company.pk, trade__user=request.session['user'], trade__status="succeeded").order_by('-agreement_date')
			
			return render_to_response(template, {
					'company':company,
					'products':products,
					'session_user':request.session['username'],
					'succeeded_products':True,
					'agreed_products':products_agreed
				})
		else:
			return HttpResponse("<p class='xl-error'>FOR USERS ONLY</p>")


	def get_failed_user_trades(self, request):
		
		if 'username' in request.session:
			
			template = "includes/user_failed_trades.html"
			trades = ProductTrade.objects.filter(user=request.session['user']).exclude(status="started").exclude(status="succeeded").values('product__company').annotate(products=Count('product__company'))
			
			return render_to_response(template, {
					'trade_companies':trades,
					'user':User.objects.get(pk=request.session['user']),
					'session_user':request.session['username'],
					'companies':Company.objects.all(),
					'failed_trades':True
				})
		else:
			return HttpResponse("<p class='xl-error'>FOR USERS ONLY</p>")


	def get_failed_products_trades(self, request, company_id):

		if 'username' in request.session:
			
			template = "includes/user_failed_trades.html"
			company = Company.objects.get(pk=company_id)
			products = ProductTrade.objects.filter(product__company=company.pk, user=request.session['user']).exclude(status="started").exclude(status="succeeded").order_by('-started_date')
			
			return render_to_response(template, {
					'company':company,
					'products':products,
					'session_user':request.session['username'],
					'failed_products':True
				})
		else:
			return HttpResponse("<p class='xl-error'>FOR USERS ONLY</p>")