# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from pip._vendor.requests import Response
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import TemplateView
from django.core.urlresolvers import reverse
from django.core import serializers
from django.core.mail import send_mail
from django.utils import timezone
from django.template import RequestContext
from django.contrib import messages
from django.db.models import Q, Count, Sum
from django.db.models.functions import TruncMonth, TruncYear
from xlstore.models import *
from xlstore.forms import *
from xlstore_managment.forms import *
from xlstore_managment.models import *
from xlstore_ecommerce.models import *
from xlstore_managment.helpers import intword
from xlstore.views import getUserIpAddress
from django.core.signing import Signer
from datetime import datetime, timedelta, date
from xlstore_managment.backends import MS_CompanyAuthentication, send_bill_email
from django.conf import settings
from json import dumps
from operator import itemgetter
import uuid
import random
import string
import pygal
import itertools
import pytz


utc = pytz.UTC
today_now = datetime.now().replace(tzinfo=utc)

# Create your views here.

def send_email_service(subject, message, from_email, to_email):
	send_mail(subject, 
				message, 
				from_email, 
				[to_email],
				fail_silently=False)
	return HttpResponse("message sent")


def check_ms_licence_key(request):
	if check_all_sessions(request) is not False:
		licence = MS_LicenceKey.objects.get(company=request.session['ms'])
		today = datetime.now().date()
		expary_date = licence.expary_date
		remaining = expary_date - today
		zero_date = datetime.now().date() - datetime.now().date()

		if remaining > zero_date:
			return remaining
		else:
			return False


def check_sm_ms_sessions(request):
	if 'company_name' in request.session and 'ms' in request.session:
		return True
	else:
		return False


def check_all_sessions(request):
	if check_sm_ms_sessions(request) is not False and 'admin' in request.session:
		return True
	else:
		return False


def get_month_name(month):
	months = ["January", "Febuary", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
	for position, value in enumerate(months):
		return months[int(month) - 1]
		

def get_month_days(month, year):
	month = int(month)
	if month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12:
		return 31
	elif month == 4 or month == 6 or month == 9 or month == 11:
		return 30
	elif month == 2:
		if int(year) % 4 == 0:
			return 29
		else:
			return 28


class MS_Welcome(TemplateView):

	template = "managment/welcome.html"

	def get(self, request):
		if 'company_name' in request.session:
			if 'ms' in request.session:
				return HttpResponseRedirect('/managment/hms_c/')
			else:
				company_name = request.session['company_name']
				company = Company.objects.get(name_dotted = company_name)
				product_form = ProductForm()
				com_id = request.session['pk']
				categories = Categories.objects.filter(company=company.pk)

				welcome_context = {}
				welcome_context.update(csrf(request))
				welcome_context['company'] = company
				welcome_context['session_company'] = company_name
				welcome_context['categories'] = categories
				welcome_context['product_form'] = product_form
				welcome_context['post_form'] = PostForm()

				return render(request, self.template, welcome_context)
		else:
			messages.error(request, "Only Companies Can Visite This Page !!!")
			return HttpResponseRedirect('/')


	def post(self, request):
		if request.method == "POST":
			if 'company_name' in request.session:
				is_admin = "admin"
				username = request.POST.get('username', '')
				password = request.POST.get('password', '')
				admin = request.POST.get('admin', '')
				company = Company.objects.get(pk=request.session['pk'])

				signer = Signer()
				value = signer.unsign('admin:CloCO3wWhcf5Yj7ygFAD0ZO156U')

				auth = MS_CompanyAuthentication()

				check_admin = auth.ms_authenticate(company=request.session['pk'], username=username, password=password)

				if check_admin is not None:
					request.session['ms'] = check_admin.pk
					if admin == "on":
						request.session['admin'] = is_admin

						messages.success(request, "You are Logged In As Admin !!!")
						return HttpResponseRedirect('/managment/hms_c/')
					else:
						messages.success(request, "You are Logged In As User !!!")
						return HttpResponseRedirect('/managment/hms_c/')
				else:
					messages.error(request, "Login Failed !!!")
					return HttpResponseRedirect('/managment/welcome/')

			else:
				messages.error(request, "Only Companies can Login Here!!!")
				return HttpResponseRedirect('/managment/welcome/')


class MS_SignUp(TemplateView):

	template = "managment/signup.html"

	def get(self, request):
		if 'company_name' in request.session:
			signup_context = {}
			company_name = request.session['company_name']
			company = Company.objects.get(name_dotted = company_name)
			product_form = ProductForm()
			com_id = request.session['pk']
			categories = Categories.objects.filter(company=company.pk)

			signup_context = {}
			signup_context.update(csrf(request))
			signup_context['company'] = company
			signup_context['session_company'] = company_name
			signup_context['categories'] = categories
			signup_context['product_form'] = product_form
			signup_context['post_form'] = PostForm()

			return render(request, self.template, signup_context)
		else:
			messages.error(request, "Only Companies Can Visite This Page !!!")
			return HttpResponseRedirect('/')


	def post(self, request):
		if request.method == 'POST':
			if 'company_name' in request.session:
				username = request.POST.get('username', '')
				password = request.POST.get('password', '')
				conf_password = request.POST.get('conf_password', '')
				company = Company.objects.get(pk=request.session['pk']);
				check_cms = MS_CompanyAdministrator.objects.filter(company=request.session['pk'])

				if check_cms is not None:
					messages.error(request, "You're already have an account. Login Please !!!")
					return HttpResponseRedirect('/managment/welcome/')
				else:
					if password == conf_password:
						is_admin = "admin"
						licence_key = uuid.uuid4()
						allowed_chars = ''.join((string.lowercase, string.uppercase, string.digits))
						unique_id = ''.join(random.choice(allowed_chars) for _ in range(32))

						signer = Signer()
						password_encoded = signer.sign(password)

						MS_instance = MS_CompanyAdministrator(
								company=Company.objects.get(pk=request.session['pk']),
								email=company.email,
								username=username,
								password=password,
								registration_date=today_now
							)
						MS_instance.save()

						expary_date = datetime.now().date() + timedelta(days=14)

						licence_instance = MS_LicenceKey(
								company=MS_CompanyAdministrator.objects.get(pk=MS_instance.pk),
								licence_key=licence_key,
								status="trial",
								activated_date=datetime.now().date(),
								expary_date=expary_date
							)

						licence_instance.save()

						ms_settings = MS_Settings(
								company=MS_CompanyAdministrator.objects.get(pk=MS_instance.pk)
							)

						ms_settings.save()

						request.session['ms'] = MS_instance.pk
						request.session['admin'] = is_admin

						messages.success(request, "Managment System Set Up !!!")
						return HttpResponseRedirect('/managment/thanks/')
					else:
						messages.error(request, "Password don't match !!!")
						return HttpResponseRedirect('/managment/signup/')
			else:
				messages.error(request, "Only Companies Can Visite This Page !!!")
				return HttpResponseRedirect('/')


def get_thanks_page(request):
	if check_sm_ms_sessions(request) is not False:
		template = "managment/thanksign.html"
		company_name = request.session['company_name']
		company = Company.objects.get(name_dotted = company_name)
		product_form = ProductForm()
		com_id = request.session['pk']
		categories = Categories.objects.filter(company=company.pk)
		ms_session = MS_CompanyAdministrator.objects.get(pk=request.session['ms'])
		licence_session = MS_LicenceKey.objects.get(company=ms_session.pk)

		thanks_context = {}
		thanks_context.update(csrf(request))
		thanks_context['company'] = company
		thanks_context['session_company'] = company_name
		thanks_context['categories'] = categories
		thanks_context['product_form'] = product_form
		thanks_context['post_form'] = PostForm()
		thanks_context['ms_session'] = ms_session
		thanks_context['licence_session'] = licence_session

		return render(request, template, thanks_context)
	else:
		messages.error(request, "Login Please !!!")
		return HttpResponseRedirect('/managment/welcome/')


def admin_session(request):
	if 'admin' in request.session:
		return True
	else:
		return None


def activate_ms_admin(request):
	if check_sm_ms_sessions(request) is not False:
		if request.method == "POST":
			admin_password = request.POST.get('admin_password', '')
			get_admin = MS_CompanyAdministrator.objects.get(pk=request.session['ms'])
			is_admin = "admin"

			if admin_password == get_admin.password:
				request.session['admin'] = is_admin
				return HttpResponseRedirect('/managment/hms_c/')
			else:
				messages.error(request, "Wrong Admin Password !!!")
				return HttpResponseRedirect('/managment/hms_c/')
	else:
		messages.error(request, "Login Please !!!")
		return HttpResponseRedirect('/managment/welcome/')


def desactivate_ms_admin(request):
	if check_sm_ms_sessions(request) is not False:
		try:
			del request.session['admin']
		except KeyError:
			pass

		return HttpResponseRedirect('/managment/hms_c/')
	else:
		messages.error(request, "Login Please !!!")
		return HttpResponseRedirect('/managment/welcome/')


def logout_ms(request):
	if check_sm_ms_sessions(request) is not False:
		try:
			del request.session['ms']
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
		except KeyError:
			pass

		return HttpResponseRedirect('/managment/welcome/')


def get_home_managment_system(request):
	if check_sm_ms_sessions(request) is not False:
		template = "managment/home.html"
		company_name = request.session['company_name']
		company = Company.objects.get(name_dotted = company_name)
		product_form = ProductForm()
		com_id = request.session['pk']
		categories = Categories.objects.filter(company=company.pk)
		ms_session = MS_CompanyAdministrator.objects.get(pk=request.session['ms'])
		licence_session = MS_LicenceKey.objects.get(company=ms_session.pk)

		home_context = {}
		home_context.update(csrf(request))

		if 'teller' in request.session:
			home_context['teller_session'] = True
			home_context['teller'] = MS_CompanyTeller.objects.get(pk=request.session['teller'])

		home_context['company'] = company
		home_context['session_company'] = company_name
		home_context['categories'] = categories
		home_context['product_form'] = product_form
		home_context['post_form'] = PostForm()
		home_context['ms_session'] = ms_session
		home_context['licence_session'] = licence_session
		home_context['admin_session'] = admin_session(request)

		return render(request, template, home_context)
	else:
		messages.error(request, "Login Please !!!")
		return HttpResponseRedirect('/managment/welcome/')


def get_products_managment_system(request):
	if check_sm_ms_sessions(request) is not False:
		template = "managment/products.html"
		company_name = request.session['company_name']
		company = Company.objects.get(name_dotted = company_name)
		product_form = ProductForm()
		com_id = request.session['pk']
		categories = Categories.objects.filter(company=company.pk)
		ms_session = MS_CompanyAdministrator.objects.get(pk=request.session['ms'])
		licence_session = MS_LicenceKey.objects.get(company=ms_session.pk)
		products = MS_Products.objects.filter(product__company=request.session['pk']).order_by('-last_entry_stock')

		product_context = {}
		product_context.update(csrf(request))

		if 'teller' in request.session:
			product_context['teller_session'] = True
			product_context['teller'] = MS_CompanyTeller.objects.get(pk=request.session['teller'])

		product_context['company'] = company
		product_context['session_company'] = company_name
		product_context['categories'] = categories
		product_context['product_form'] = product_form
		product_context['post_form'] = PostForm()
		product_context['ms_session'] = ms_session
		product_context['licence_session'] = licence_session
		product_context['admin_session'] = admin_session(request)
		product_context['products'] = products

		return render(request, template, product_context)
	else:
		messages.error(request, "Login Please !!!")
		return HttpResponseRedirect('/managment/welcome/')


class AddFreshProduct(TemplateView):

	template = "managment/add_product.html"

	def get(self, request):
		if check_sm_ms_sessions(request) is not False:
			company_name = request.session['company_name']
			company = Company.objects.get(name_dotted = company_name)
			product_form = ProductForm()
			categories = Categories.objects.filter(company=company.pk)
			ms_session = MS_CompanyAdministrator.objects.get(pk=request.session['ms'])
			licence_session = MS_LicenceKey.objects.get(company=ms_session.pk)

			product_context = {}
			product_context.update(csrf(request))
			product_context['company'] = company
			product_context['session_company'] = company_name
			product_context['categories'] = categories
			product_context['product_form'] = product_form
			product_context['ms_session'] = ms_session
			product_context['licence_session'] = licence_session
			product_context['admin_session'] = admin_session(request)

			return render(request, self.template, product_context)
		else:
			messages.error(request, "Login Please !!!")
			return HttpResponseRedirect('/managment/welcome/')


	def post(self, request):
		if request.method == "POST":
			to_post = False
			category = request.POST.get('category','')
			product_name = request.POST.get('product_name', '')
			image = request.FILES.get('image', '')
			price = request.POST.get('price', '')
			currency = request.POST.get('currency', '')
			product_description = request.POST.get('product_description', '')
			to_be_posted = request.POST.get('to_be_posted', '')

			if to_be_posted == 'on':
				to_post = True
			else:
				to_post = False

			product_form = ProductForm(request.POST, request.FILES, instance=Products(
					company = Company.objects.get(pk=request.session['pk']),
					category = Categories.objects.get(pk=category),
					is_to_be_posted=to_post,
					is_deleted=False,
					posted_date=today_now
				))
			if product_form.is_valid():

				product = product_form.save()

				product_code = request.POST.get('product_code', '')
				initial_stock = request.POST.get('initial_stock', '')
				item_price = request.POST.get('item_price','')

				ms_product = MS_Products(
						product=Products.items.get(pk=product.pk),
						price=price,
						stock=initial_stock,
						product_code=product_code,
						last_entry_stock=today_now
					)
				ms_p = ms_product.save()

				ms_entry = MS_ProductEntry(
						product=MS_Products.objects.get(pk=ms_product.pk),
						quantity_before=0,
						quantity_added=initial_stock,
						item_price=item_price,
						entry_date=today_now
					)
				ms_entry.save()

				messages.success(request, "Product Saved Successfully !!!")
				return HttpResponseRedirect('/managment/pms_c/')
			else:
				messages.error(request, product_form.errors)
				return HttpResponseRedirect('/managment/pms_c/')


class AddFromProduct(TemplateView):

	template = "managment/add_from_product.html"
	
	def get(self, request):
		if check_sm_ms_sessions(request) is not False:
			product_context = {}
			product_context['admin_session'] = admin_session(request)
			product_context['products'] = Products.items.filter(company=request.session['pk']).order_by('-posted_date')
			product_context['ms_products'] = MS_Products.objects.filter(product__company=request.session['pk'])
			product_context['product_category'] = Categories.objects.filter(company=request.session['pk'])
			product_context['setting'] = MS_Settings.objects.get(company=request.session['ms'])
			return render(request, self.template, product_context)
		else:
			messages.error(request, "Login Please !!!")
			return HttpResponseRedirect('/managment/welcome/')


	def post(self, request):
		if request.method == "POST":
			if check_sm_ms_sessions(request) is not False:
				product = request.POST.get('product', '')
				product_code = request.POST.get('product_code','')
				quantity = request.POST.get('quantity', '')
				item_price = request.POST.get('item_price','')
				check_pms = MS_Products.objects.filter(product=product)
				product_details = Products.items.get(pk=product)
				if check_pms:
					return HttpResponse("Item Already Exist")
				else:
					ms_product = MS_Products(
							product=Products.items.get(pk=product),
							price=product_details.price,
							stock=quantity,
							product_code=product_code,
							last_entry_stock=today_now
						)
					ms_p = ms_product.save()

					ms_entry = MS_ProductEntry(
							product=MS_Products.objects.get(pk=ms_product.pk),
							quantity_before=0,
							quantity_added=quantity,
							item_price=item_price,
							entry_date=today_now
						)
					ms_entry.save()

				add_response = {"product":product,"product_code":product_code,"quantity":quantity}
				return HttpResponse(add_response)
			else:
				messages.error(request, "Login Please")
				return HttpResponseRedirect('/managment/welcome/')



def get_all_ms_products(request):
	if check_sm_ms_sessions(request) is not False:
		template = "managment/all_products.html"
		product_context = {}
		product_context.update(csrf(request))
		product_context['products'] = MS_Products.objects.filter(product__company=request.session['pk']).order_by('-last_entry_stock')
		product_context['admin_session'] = admin_session(request)
		product_context['product_category'] = Categories.objects.filter(company=request.session['pk'])
		product_context['setting'] = MS_Settings.objects.get(company=request.session['ms'])
		return render(request, template, product_context)
	else:
		messages.error(request, "Login Please !!!")
		return HttpResponseRedirect('/managment/welcome/')


def get_product_categories(request, category_id):
	if check_sm_ms_sessions(request) is not False:
		template = "managment/all_products.html"
		product_context = {}
		product_context.update(csrf(request))
		product_context['products'] = MS_Products.objects.filter(product__category=category_id, product__company=request.session['pk']).order_by('-last_entry_stock')
		product_context['admin_session'] = admin_session(request)
		product_context['product_category'] = Categories.objects.filter(company=request.session['pk'])
		return render(request, template, product_context)
	else:
		messages.error(request, "Login Please !!!")
		return HttpResponseRedirect('/managment/welcome/')


@csrf_exempt
def update_ms_product(request, product_id):
	if check_sm_ms_sessions(request) is not False:
		admin = admin_session(request)
		if admin == True:
			if request.method == "POST":

				quantity = request.POST.get('quantity', '')
				stock_before = request.POST.get('stock', '')
				sum_stock = request.POST.get('sum_stock', '')
				item_price = request.POST.get('item_price', '')

				if quantity is not "" or quantity is not 0:

					ms_product = MS_Products.objects.get(pk=product_id)
					ms_product.stock = sum_stock
					ms_product.last_entry_stock = today_now
					ms_product.save()

					ms_entry = MS_ProductEntry(
							product=MS_Products.objects.get(pk=product_id),
							quantity_before=int(stock_before),
							quantity_added=int(quantity),
							item_price=item_price,
							entry_date=today_now
						)
					ms_entry.save()

					return HttpResponse("MS Product Updated !!!!")
				else:
					return HttpResponse("Quantity can't be empty or 0 !!!")
		else:
			return HttpResponse("Only For Admins !!!")
	else:
		return HttpResponse("Login Please !!!")


@csrf_exempt
def is_to_be_posted_toggle(request):
	if check_sm_ms_sessions(request) is not False:
		if admin_session(request) == True:
			product_id = request.POST.get('product','')
			product = Products.items.get(pk=product_id)
			if product.is_to_be_posted == True:
				product.is_to_be_posted = False
			elif product.is_to_be_posted == False:
				product.is_to_be_posted = True
				product.posted_date = today_now
			product.save()
			return HttpResponse(product.is_to_be_posted)
		else:
			return HttpResponse("Only For Admins !!!")
	else:
		return HttpResponse("Login Please !!!")


def get_all_ms_cart_products(request):
	if check_sm_ms_sessions(request) is not False:
		template = "managment/products_cart.html"
		product_context = {}
		product_context.update(csrf(request))

		if 'teller' in request.session:
			product_context['teller_session'] = True
			product_context['teller'] = MS_CompanyTeller.objects.get(pk=request.session['teller'])

		product_context['products'] = MS_Products.objects.filter(product__company=request.session['pk']).order_by('-last_entry_stock')
		product_context['admin_session'] = admin_session(request)
		product_context['session_cart'] = True if 'bill' in request.session else False
		product_context['product_category'] = Categories.objects.filter(company=request.session['pk'])
		product_context['setting'] = MS_Settings.objects.get(company=request.session['ms'])
		return render(request, template, product_context)
	else:
		messages.error(request, "Login Please !!!")
		return HttpResponseRedirect('/managment/welcome/')


def  filter_ms_cart_product(request):
	if request.method == "POST":
		search_key = request.POST.get('search_key', '')
		search_by = request.POST.get('search_by', '')
		template = "managment/products_cart.html"

		product_context = {}
		product_context.update(csrf(request))

		if search_by == "N":
			product_context['products'] = MS_Products.objects.filter(product__company=request.session['pk'], product__product_name__contains=search_key).order_by('-last_entry_stock')
		elif search_by == "C":
			product_context['products'] = MS_Products.objects.filter(product__company=request.session['pk'], product_code__contains=search_key).order_by('-last_entry_stock')

		product_context['session_cart'] = True if 'bill' in request.session else False
		product_context['admin_session'] = admin_session(request)
		product_context['product_category'] = Categories.objects.filter(company=request.session['pk'])

		return render(request, template, product_context)


def get_next_bill(request):
	if check_sm_ms_sessions(request) is not False:
		template = "managment/receipt_content.html"
		bill_context = {}
		next_billID = 1

		last_bill_id = MS_Receipts.objects.filter(company=request.session['ms']).order_by('receipt_number').last()

		if last_bill_id:
			if 'bill' in request.session:
				last_bill_check = MS_Receipts.objects.get(pk=request.session['bill'])

				if last_bill_check:
					if last_bill_check.status == "success":
						next_billID = last_bill_check.receipt_number + 1
					else:
						next_billID = last_bill_check.receipt_number
						bill_content = MS_ReceiptDetails.objects.filter(receipt=last_bill_check.pk)

						user_trades = None

						if last_bill_check.user:
							user_trades = TradeAgreements.objects.filter(trade__user=last_bill_check.user.pk, trade__product__company=request.session['pk']).exclude(is_finished=True)
						else:
							user_trades = None

						sum_amount_bill = 0

						for bill in bill_content:
							sum_amount_bill = sum_amount_bill + int(bill.total)

						bill_context['bill_content'] = bill_content
						bill_context['current_bill'] = last_bill_check
						bill_context['sum_amount_bill'] = sum_amount_bill
						bill_context['admin_session'] = admin_session(request)
						bill_context['today'] = datetime.now
						bill_context['user_trades'] = user_trades
			else:
				next_billID = last_bill_id.receipt_number + 1
		else:
			next_billID = 1

		if 'teller' in request.session:
			bill_context['teller_session'] = True
			bill_context['teller'] = MS_CompanyTeller.objects.get(pk=request.session['teller']) 
		
		bill_context['next_billID'] = next_billID
		bill_context['company'] = MS_CompanyAdministrator.objects.get(pk=request.session['ms'])
		bill_context['setting'] = MS_Settings.objects.get(company=request.session['ms'])
		
		return render(request, template, bill_context)


def create_this_bill(request):
	if request.method == "POST":
		if check_sm_ms_sessions(request) is not False:
			user_id = request.POST.get('user_id','')
			user_name = request.POST.get('name','')
			user_email = request.POST.get('email','')
			bill_number = 1

			last_bill_id = MS_Receipts.objects.filter(company=request.session['ms']).order_by('receipt_number').last()

			if last_bill_id:
				bill_number = last_bill_id.receipt_number + 1
			else:
				bill_number = 1

			if user_id != "":
				ms_receipt = MS_Receipts(
						company=MS_CompanyAdministrator.objects.get(pk=request.session['ms']),
						user=User.objects.get(pk=user_id),
						teller=MS_CompanyTeller.objects.get(pk=request.session['teller']) if 'teller' in request.session else None,
						receipt_number=bill_number,
						status="created",
						saved_date_timezone=today_now,
						saved_date=datetime.now().date()
					)
				ms_receipt.save()

				request.session['bill'] = ms_receipt.pk
			else:
				ms_receipt = MS_Receipts(
						company=MS_CompanyAdministrator.objects.get(pk=request.session['ms']),
						username=user_name,
						teller=MS_CompanyTeller.objects.get(pk=request.session['teller']) if 'teller' in request.session else None,
						email=user_email,
						receipt_number=bill_number,
						status="created",
						saved_date_timezone=today_now,
						saved_date=datetime.now().date()
					)
				ms_receipt.save()
				
				request.session['bill'] = ms_receipt.pk

			return HttpResponse("Bill Created")
		else:
			return HttpResponse("NOT ALLOWED")
	else:
		if check_all_sessions(request) is not None or 'teller' in request.session:
			template = "managment/create_bill.html"
			bill_context = {}
			bill_context.update(csrf(request))
			bill_context['session_admin'] = admin_session(request)
			bill_context['teller_session'] = True if 'teller' in request.session else False

			return render(request, template, bill_context)



def load_users_for_bill(request):
	if request.method == "POST":
		search_user_key = request.POST.get('search_user_key', '')
		template = "managment/reciept_users.html"
		user_context = {}
		user_context['users'] = User.objects.filter(
			Q(user_name__contains=search_user_key) |
			Q(full_name__contains=search_user_key)
			).order_by('-user_name')

		user_context['search_key'] = search_user_key
		user_context['session_pk'] = request.session['pk']

		return render(request, template, user_context)


def decrease_items(request, quantity, product_id):
	product = MS_Products.objects.get(pk=product_id)
	count = int(product.stock) - int(quantity)
	product.stock = count
	product.save()

	return product.stock


def increase_items(request, quantity, product_id):
	product = MS_Products.objects.get(pk=product_id)
	product.stock += quantity
	product.save()

	return product.stock


def add_items_to_bill(request):
	if request.method == "POST":
		if check_sm_ms_sessions(request) is not False:
			if 'bill' in request.session:
				bill_id = request.session['bill']
				product_id = request.POST.get('product', '')
				quantity = request.POST.get('quantity','')
				product = MS_Products.objects.get(pk=product_id)
				total = float(quantity) * float(product.product.price)

				check_item = MS_ReceiptDetails.objects.filter(receipt=bill_id, product=product_id)

				if int(quantity) > 0:

					if int(product.stock) >= int(quantity):

						if check_item:
							for item_id in check_item:
								if item_id.is_trade == True:
									return HttpResponse("Cant Update Trade Item")
								else:
									item = MS_ReceiptDetails.objects.get(pk=item_id.pk)
									count = int(item.quantity) + int(quantity)
									item.quantity = count
									sum_total = int(item.total) + int(total)
									item.total = sum_total
									item.save()

									decrease_items(request, quantity, product_id)
									return HttpResponse("Item Updated to The Cart")

								return HttpResponse("Item Updated to The Cart")
						else:
							receipt_item = MS_ReceiptDetails(
									receipt=MS_Receipts.objects.get(pk=bill_id),
									product=MS_Products.objects.get(pk=product_id),
									quantity=quantity,
									item_price=product.product.price,
									total=total,
									saved_date=datetime.now().date()
								)
							receipt_item.save()

							decrease_items(request, quantity, product_id)
							return HttpResponse("Item Added To The Cart")
					else:
						return HttpResponse("failed")
				else:
					return HttpResponse("negative")
			else:
				return HttpResponse("No Session Bill. Please Create One")


def update_bill_item(request):
	if check_sm_ms_sessions(request) is not False:
		if 'bill' in request.session:
			product_id = request.POST.get('product','')
			quantity = request.POST.get('quantity','')
			item_id = request.POST.get('item', '')
			ms_product = MS_Products.objects.get(pk=product_id)

			if int(quantity) > 0:

				if int(ms_product.stock) >= int(quantity):

					check_item = MS_ReceiptDetails.objects.filter(receipt=request.session['bill'], product=product_id)
					
					for item_id in check_item:

						if item_id.is_trade == True:

							return HttpResponse("Cant Update Trade Item")

						else:

							item = MS_ReceiptDetails.objects.get(pk=item_id.pk)

							if int(quantity) > int(item.quantity):
								item_added = int(quantity) - int(item.quantity)
								amount_added = int(item_added) * int(ms_product.product.price)
								item.quantity = int(item_added) + int(item.quantity)
								item.total = int(amount_added) + int(item.total)
								item.save()

								decrease_items(request, item_added, product_id)
								return HttpResponse("Quantity Increased")

							elif int(quantity) < int(item.quantity):
								item_removed = int(item.quantity) - int(quantity)
								amount_removed = int(item_removed) * int(ms_product.product.price)
								item.quantity = int(item.quantity) - int(item_removed)
								item.total = int(item.total) - int(amount_removed)
								item.save()

								increase_items(request, item_removed, product_id)
								return HttpResponse("Quantity Decreased")

							else:
								return HttpResponse("Nothing has changed")

				elif int(ms_product.stock) <= int(quantity):

					item = MS_ReceiptDetails.objects.get(pk=item_id)

					if int(quantity) < int(item.quantity):
						item_removed = int(item.quantity) - int(quantity)
						amount_removed = int(item_removed) * int(ms_product.product.price)
						item.quantity = int(item.quantity) - int(item_removed)
						item.total = int(item.total) - int(amount_removed)
						item.save()

						increase_items(request, item_removed, product_id)
						return HttpResponse("Quantity Decreased")

					else:
						return HttpResponse("Nothing has changed")

				else:
					return HttpResponse("negative")
			else:
				return HttpResponse("failed")


@csrf_exempt
def remove_bill_item(request):
	if check_sm_ms_sessions(request) is not False:
		if 'bill' in request.session:
			if request.method == "POST":
				bill = request.session['bill']
				item_id = request.POST.get('item', '')
				quantity = request.POST.get('quantity', '')
				product = request.POST.get('product', '')

				ms_product = MS_Products.objects.get(pk=product)
				item = MS_ReceiptDetails.objects.get(pk=item_id)

				if item.is_trade == True:
					return HttpResponse("Cant Delete")
				else:
					item.delete()

					increase_items(request, int(quantity), product)

					return HttpResponse("Item Deleted")
			else:
				return HttpResponse("Request not Posted")
		else:
			return HttpResponse("No Session Bill")
	else:
		return HttpResponse("You must log in")


def finish_current_bill(request):
	if check_sm_ms_sessions(request) is not False:
		if 'bill' in request.session:
			bill_id = request.session['bill']
			total = request.POST.get('total', '')
			total_net = request.POST.get('total_net','')
			discount = request.POST.get('discount','')
			paid_by = request.POST.get('paid_by','')
			bill_content = request.POST.get('bill_content', '')

			ms_receipt = MS_Receipts.objects.get(pk=bill_id)

			ms_receipt.status="success"
			ms_receipt.discount=discount
			ms_receipt.total_paid=total
			ms_receipt.total_net=total_net
			ms_receipt.paid_by=paid_by
			ms_receipt.saved_date=datetime.now().date()
			ms_receipt.save()

			send_bill_email(request, ms_receipt.pk)
				
			try:
				del request.session['bill']
			except KeyError:
				pass

			return HttpResponse("Bill Finished !!!")


#MS BILLS


def get_all_ms_bills(request):
	if check_all_sessions(request) is not False or 'teller' in request.session:
		template = "managment/bills.html"
		company_name = request.session['company_name']
		company = Company.objects.get(name_dotted = company_name)
		product_form = ProductForm()
		com_id = request.session['pk']
		categories = Categories.objects.filter(company=company.pk)
		ms_session = MS_CompanyAdministrator.objects.get(pk=request.session['ms'])
		licence_session = MS_LicenceKey.objects.get(company=ms_session.pk)
		today = datetime.now().date()
		dates_bill = MS_Receipts.objects.filter(company=request.session['ms'], saved_date__lt=today).values('saved_date').annotate(receipts=Count('saved_date')).order_by('-saved_date')
		today_bills_count = MS_Receipts.objects.filter(company=request.session['ms'], saved_date=today)
		today_count = 0
		
		if today_bills_count:
			for bill in today_bills_count:
				today_count += 1
		else:
			today_count = 0


		bill_context = {}
		bill_context.update(csrf(request))

		if 'teller' in request.session:
			bill_context['teller_session'] = True
			bill_context['teller'] = MS_CompanyTeller.objects.get(pk=request.session['teller'])

		bill_context['company'] = company
		bill_context['session_company'] = company_name
		bill_context['categories'] = categories
		bill_context['product_form'] = product_form
		bill_context['post_form'] = PostForm()
		bill_context['ms_session'] = ms_session
		bill_context['licence_session'] = licence_session
		bill_context['admin_session'] = admin_session(request)
		bill_context['dates_bill'] = dates_bill
		bill_context['today'] = today
		bill_context['today_count'] = today_count
		bill_context['dates_month'] = group_dates_since_begining(request)

		return render(request, template, bill_context)
	else:
		messages.error(request, "Login as Admin Please !!!")
		return HttpResponseRedirect('/managment/welcome/')


def get_today_bills(request):
	if check_all_sessions(request) is not False or 'teller' in request.session:
		template = "managment/bill_list.html"
		bill_context = {}
		today = datetime.now().date()
		today_bills = MS_Receipts.objects.filter(company=request.session['ms'], saved_date=today).order_by('-receipt_number')

		total = 0
		discount = 0
		total_net = 0

		if today_bills:
			for bill in today_bills:
				total += bill.total_paid
				discount += bill.discount
				total_net += bill.total_net

		if 'teller' in request.session:
			bill_context['teller_session'] = True
			bill_context['teller'] = MS_CompanyTeller.objects.get(pk=request.session['teller'])

		bill_context['today'] = today
		bill_context['bills'] = today_bills
		bill_context['admin_session'] = admin_session(request)
		bill_context['total_paid'] = total
		bill_context['discount'] = discount
		bill_context['total_net'] = total_net
		bill_context['setting'] = MS_Settings.objects.get(company=request.session['ms'])

		return render(request, template, bill_context)
	else:
		messages.error(request, "Login as Admin Please !!!")
		return HttpResponseRedirect('/managment/welcome/')


def load_bill_by_date(request, bill_date):
	if check_all_sessions(request) is not False or 'teller' in request.session:
		template = "managment/bill_list.html"
		bill_context = {}
		today = datetime.now().date()
		bills_date = MS_Receipts.objects.filter(company=request.session['ms'], saved_date=bill_date).order_by('-receipt_number')

		total = 0
		discount = 0
		total_net = 0

		if bills_date:
			for bill in bills_date:
				total += bill.total_paid
				discount += bill.discount
				total_net += bill.total_net


		if 'teller' in request.session:
			bill_context['teller_session'] = True
			bill_context['teller'] = MS_CompanyTeller.objects.get(pk=request.session['teller'])

		bill_context['today'] = today
		bill_context['admin_session'] = admin_session(request)
		bill_context['bills'] = bills_date
		bill_context['total_paid'] = total
		bill_context['discount'] = discount
		bill_context['total_net'] = total_net
		bill_context['setting'] = MS_Settings.objects.get(company=request.session['ms'])

		return render(request, template, bill_context)
	else:
		messages.error(request, "Login as Admin Please !!!")
		return HttpResponseRedirect('/managment/welcome/')


def load_bill_by_month_year(request, month, year):
	if check_all_sessions(request) is not False or 'teller' in request.session:
		template = "managment/bill_list.html"
		bill_context = {}
		today = datetime.now().date()
		bills_date = MS_Receipts.objects.filter(company=request.session['ms'], saved_date__month=month, saved_date__year=year).order_by('-receipt_number') if int(month) != 0 else MS_Receipts.objects.filter(company=request.session['ms'], saved_date__year=year).order_by('-receipt_number')

		total = 0
		discount = 0
		total_net = 0

		if bills_date:
			for bill in bills_date:
				total += bill.total_paid
				discount += bill.discount
				total_net += bill.total_net

		if 'teller' in request.session:
			bill_context['teller_session'] = True
			bill_context['teller'] = MS_CompanyTeller.objects.get(pk=request.session['teller'])

		bill_context['today'] = today
		bill_context['admin_session'] = admin_session(request)
		bill_context['bills'] = bills_date
		bill_context['total_paid'] = total
		bill_context['discount'] = discount
		bill_context['total_net'] = total_net
		bill_context['setting'] = MS_Settings.objects.get(company=request.session['ms'])

		return render(request, template, bill_context)
	else:
		messages.error(request, "Login as Admin Please !!!")
		return HttpResponseRedirect('/managment/welcome/')


def load_bill_single_bill(request, bill_id):
	
	template = "managment/load_bill.html"
	bill_context = {}
	today = datetime.now().date()
	bill = get_object_or_404(MS_Receipts, pk=bill_id)
	bill_content = MS_ReceiptDetails.objects.filter(receipt=bill.pk)
	
	if 'username' in request.session:
		
		if bill.user.pk == request.session['user']:
			
			bill_context['bill'] = bill
			bill_context['session_user'] = True
			bill_context['bill_content'] = bill_content
			bill_context['setting'] = MS_Settings.objects.get(company=bill.company.pk)

			return render(request, template, bill_context)
		else:
			return HttpResponse("Not Owner")

	elif check_all_sessions(request) is not False or 'teller' in request.session:

		if bill.company.pk == request.session['ms']:
		
			if 'teller' in request.session:
				
				bill_context['teller_session'] = True
				bill_context['teller'] = MS_CompanyTeller.objects.get(pk=request.session['teller'])

			bill_context['admin_session'] = admin_session(request)
			bill_context['bill'] = bill
			bill_context['bill_content'] = bill_content
			bill_context['setting'] = MS_Settings.objects.get(company=request.session['ms'])

			return render(request, template, bill_context)
		else:
			return HttpResponse("Not Owner")
	else:
		return HttpResponse("User or Company Session Required")


def get_searched_bill(request):
	if check_all_sessions(request) is not False or 'teller' in request.session:
		if request.method == "POST":
			search_key = request.POST.get('search_key','')
			search_by = request.POST.get('search_by', '')
			template = "managment/bill_list.html"
			bill_context = {}
			today = datetime.now().date()

			if search_by == "N":
				bills = MS_Receipts.objects.filter(company=request.session['ms'], receipt_number=search_key)
			elif search_by == "U":
				bills = MS_Receipts.objects.filter(company=request.session['ms'], user__user_name__contains=search_key)
			elif search_by == "A":
				bills = MS_Receipts.objects.filter(company=request.session['ms'], email__contains=search_key)
			else:
				bills = MS_Receipts.objects.filter(company=request.session['ms'], saved_date=today)

			total = 0
			discount = 0
			total_net = 0

			if bills:
				for bill in bills:
					total += bill.total_paid
					discount += bill.discount
					total_net += bill.total_net

			if 'teller' in request.session:
				bill_context['teller_session'] = True
				bill_context['teller'] = MS_CompanyTeller.objects.get(pk=request.session['teller'])

			bill_context['today'] = today
			bill_context['admin_session'] = admin_session(request)
			bill_context['bills'] = bills
			bill_context['total_paid'] = total
			bill_context['discount'] = discount
			bill_context['total_net'] = total_net

			return render(request, template, bill_context)
	else:
		messages.error(request, "Login as Admin Please !!!")
		return HttpResponseRedirect('/managment/welcome/')


def get_sum_users_bills_company(user, company):
	bills = MS_Receipts.objects.filter(user=user, company__company=company).count()
	return bills


def get_sum_user_carts_company(user, company):
	carts = EC_ShoppingCart.objects.filter(market__user=user, market__company__company=company).count()
	return carts


def ms_get_user_bills_and_carts(user):

	user = User.objects.get(pk=user)
	companies = MS_CompanyAdministrator.objects.all()
	bills_and_carts = []

	if companies is not None:
		for company in companies:
			check_follow = Followers.objects.filter(user=user.pk, company=company.company.pk)
			total = int(get_sum_users_bills_company(user.pk, company.company.pk)) + int(get_sum_user_carts_company(user.pk, company.company.pk))
			bills_and_carts.append({
										"company": company.company.pk, 
										"bills": get_sum_users_bills_company(user.pk, company.company.pk), 
										"carts": get_sum_user_carts_company(user.pk, company.company.pk), 
										"all": total,
										"name": company.company.name,
										"image": company.company.get_profile_image(),
										"followed": True if check_follow else False
									})

	if bills_and_carts is not None:
		for (p,v) in enumerate(bills_and_carts):
			if v["bills"] is 0 and v["carts"] is 0:
				bills_and_carts.remove(v)

	return bills_and_carts


def ms_get_user_bills_and_carts_company(user, company):
	user = User.objects.get(pk=user)
	bills = MS_Receipts.objects.filter(user=user.pk, company__company=company).order_by('-saved_date')
	carts = EC_ShoppingCart.objects.filter(market__user=user.pk, market__company__company=company).order_by('-saved_date')

	return {"bills": bills, "carts": carts, "sum_bills": get_sum_users_bills_company(user.pk, company), "sum_carts": get_sum_user_carts_company(user.pk, company)}


#FOR INVENTORY


def get_inventory_managment_system(request):
	if check_all_sessions(request) is not False:
		template = "managment/managment.html"
		company_name = request.session['company_name']
		company = Company.objects.get(name_dotted = company_name)
		product_form = ProductForm()
		com_id = request.session['pk']
		categories = Categories.objects.filter(company=company.pk)
		ms_session = MS_CompanyAdministrator.objects.get(pk=request.session['ms'])
		licence_session = MS_LicenceKey.objects.get(company=ms_session.pk)

		inv_context = {}
		inv_context.update(csrf(request))
		inv_context['company'] = company
		inv_context['session_company'] = company_name
		inv_context['categories'] = categories
		inv_context['product_form'] = product_form
		inv_context['post_form'] = PostForm()
		inv_context['ms_session'] = ms_session
		inv_context['licence_session'] = licence_session
		inv_context['admin_session'] = admin_session(request)

		return render(request, template, inv_context)
	else:
		messages.error(request, "Login as Admin Please !!!")
		return HttpResponseRedirect('/managment/welcome/')


#product inventory


def get_product_managment_ms(request):
	if check_all_sessions(request) is not False:
		template = "managment/ms_products.html"
		company_name = request.session['company_name']
		company = Company.objects.get(name_dotted = company_name)
		product_form = ProductForm()
		com_id = request.session['pk']
		categories = Categories.objects.filter(company=company.pk)
		ms_session = MS_CompanyAdministrator.objects.get(pk=request.session['ms'])
		licence_session = MS_LicenceKey.objects.get(company=ms_session.pk)

		msp_context = {}
		msp_context.update(csrf(request))
		msp_context['company'] = company
		msp_context['session_company'] = company_name
		msp_context['categories'] = categories
		msp_context['product_form'] = product_form
		msp_context['post_form'] = PostForm()
		msp_context['ms_session'] = ms_session
		msp_context['licence_session'] = licence_session
		msp_context['admin_session'] = admin_session(request)

		return render(request, template, msp_context)
	else:
		messages.error(request, "Login as Admin Please !!!")
		return HttpResponseRedirect('/managment/welcome/')


def get_msp_all_products(request):
	if check_all_sessions(request) is not False:
		template = "managment/msproducts/products.html"
		today = datetime.today()
		msp_context = {}
		msp_context['products'] = MS_Products.objects.filter(product__company=request.session['pk']).order_by('-last_entry_stock')
		msp_context['month'] = today.month
		msp_context['year'] = today.year
		return render(request, template, msp_context)


#(to be checked)
def check_month_end_year(month):
	today = datetime.now().day
	if int(month) == 1:
		return 13
	elif int(month) == 1 and int(today) == 1:
		return 0
	else:
		return month


def check_else_year(month, year):
	if int(month) == 1:
		return int(year) - 1
	else:
		return int(year)


def get_msp_single_product(request, product_id, month, year):

	if check_all_sessions(request) is not False:
		template = "managment/msproducts/product_details.html"
		product = get_object_or_404(MS_Products, pk=product_id)

		if product.product.company.pk == request.session['pk']:
			smsp_context = {}

			today_day = datetime.now().day
			month_else = check_month_end_year(month)
			year_else = check_else_year(month, year)

			last_date = datetime(int(year), int(month), get_month_days(month, year)) if int(month_else) != 0 else datetime(int(year), 12, 31)
			previous_last_date = datetime(int(year_else), int(month_else) - 1, get_month_days(int(month_else) - 1, int(year_else))) if int(month_else) != 0 else datetime(int(year_else), 12, 31)

			entries = MS_ProductEntry.objects.filter(product=product.pk, entry_date__lt=last_date).order_by('-entry_date')
			entries_month = MS_ProductEntry.objects.filter(product=product.pk, entry_date__lt=last_date, entry_date__gt=previous_last_date) if int(month) != 0 else MS_ProductEntry.objects.filter(product=product.pk, entry_date__year=year)
			previous_entry = MS_ProductEntry.objects.filter(product=product.pk, entry_date__lt=previous_last_date) if int(month) != 0 else MS_ProductEntry.objects.filter(product=product.pk, entry_date__year__lt = int(year))

			sales = MS_ReceiptDetails.objects.filter(product=product.pk, saved_date__month=month, saved_date__year=year) if int(month) != 0 else MS_ReceiptDetails.objects.filter(product=product.pk, saved_date__year = int(year))
			all_sales = MS_ReceiptDetails.objects.filter(product=product.pk, saved_date__lt=last_date)
			previous_sales = MS_ReceiptDetails.objects.filter(product=product.pk, saved_date__lt=previous_last_date) if int(month) != 0 else MS_ReceiptDetails.objects.filter(product=product.pk, saved_date__year__lt = int(year) - 1)

			total_p_q = 0
			total_p_t = 0
			total_s_q = 0
			total_s_t = 0
			total_s_all_t = 0
			total_s_all_q = 0
			total_em_p_q = 0
			total_em_p_t = 0
			total_ps_q = 0
			total_pe_q = 0

			if previous_entry:
				for entry in previous_entry:
					total_pe_q += entry.quantity_added

			if previous_sales:
				for sale in previous_sales:
					total_ps_q += sale.quantity	

			if entries:
				for entry in entries:
					total_p_q += entry.quantity_added
					total_p_t += (entry.item_price * entry.quantity_added)

			if entries_month:
				for entry in entries_month:
					total_em_p_q += entry.quantity_added
					total_em_p_t += (entry.item_price * entry.quantity_added)

			if sales:
				for sale in sales:
					total_s_t += sale.total
					total_s_q += sale.quantity

			if all_sales:
				for sale in all_sales:
					total_s_all_t += sale.total
					total_s_all_q += sale.quantity

			current_stock = total_p_q - total_s_all_q
			total_stock = current_stock * product.product.price
			
			stock_met = total_pe_q - total_ps_q
			total_stock_met = stock_met * product.product.price
			
			stock_total = stock_met + total_em_p_q
			total_stock_total = stock_total * product.product.price


			smsp_context['product_purchases'] = entries
			smsp_context['purchase_quantity'] = total_p_q
			smsp_context['purchase_total'] = total_p_t
			smsp_context['sale_quantity'] = total_s_q
			smsp_context['sale_total'] = total_s_t
			smsp_context['current_stock'] = current_stock
			smsp_context['total_stock'] = total_stock
			smsp_context['stock_met'] = stock_met
			smsp_context['total_stock_met'] = total_stock_met
			smsp_context['stock_month'] = total_em_p_q
			smsp_context['total_stock_month'] = total_em_p_t
			smsp_context['stock_total'] = stock_total
			smsp_context['total_stock_total'] = total_stock_total

			first_entry = MS_ProductEntry.objects.filter(product=product.pk).first()
			first_entry_date = first_entry.entry_date
			today = datetime.now()

			dates = []

			for y in range(first_entry_date.year, today.year + 1):
				dates.append({"month":0, "year":y, "value":y})
				if first_entry_date.month != 1 and first_entry_date.year == y:
					if first_entry_date.month < today.month:
						for m in range(first_entry_date.month, today.month + 1):
							dates.append({"month":m, "year":y, "value":"%s, %s" % (get_month_name(m), y)})
					else:
						for m in range(first_entry_date.month, 13):
							dates.append({"month":m, "year":y, "value":"%s, %s" % (get_month_name(m), y)})
				else:
					if y == today.year:
						for m in range(1, today.month + 1):
							dates.append({"month":m, "year":y, "value":"%s, %s" % (get_month_name(m), y)})
					else:
						for m in range(1, 13):
							dates.append({"month":m, "year":y, "value":"%s, %s" % (get_month_name(m), y)})

			sales_month = MS_ReceiptDetails.objects.filter(product=product.pk, saved_date__month=month, saved_date__year=year).values('saved_date','item_price').annotate(total_totals=Sum('total'), total_quantity=Sum('quantity')).order_by('-saved_date')
			sales_year = MS_ReceiptDetails.objects.filter(product=product.pk, saved_date__year=year).values('item_price').annotate(saved_date=TruncMonth('saved_date'), total_totals=Sum('total'), total_quantity=Sum('quantity')).order_by('-saved_date') 

			smsp_context['product'] = product
			smsp_context['category'] = Categories.objects.get(pk=product.product.category)
			smsp_context['edit_product'] = EditProduct(instance=Products.items.get(pk=product.product.pk))
			smsp_context['product_sales'] = sales_year if int(month) == 0 else sales_month 
			smsp_context['setting'] = MS_Settings.objects.get(company=request.session['ms'])
			smsp_context['month'] = int(month)
			smsp_context['year'] = int(year)
			smsp_context['t_month'] = today.month
			smsp_context['t_year'] = today.year
			smsp_context['month_text'] = get_month_name(month)
			smsp_context['dates'] = dates[::-1]

			return render(request, template, smsp_context)
	else:
		messages.error(request, "Login as Admin Please !!!")
		return HttpResponseRedirect('/managment/welcome/')


def get_ms_single_product_edit(request, product_id, month, year):
	if check_all_sessions(request) is not False:
		smsp_context = {}
		template = "managment/msproducts/edit_ms_product.html"
		product = get_object_or_404(MS_Products, pk=product_id)
		smsp_context['product'] = product
		smsp_context['month'] = int(month)
		smsp_context['year'] = int(year)
		smsp_context['edit_product'] = EditProduct(instance=Products.items.get(pk=product.product.pk))

		return render(request, template, smsp_context)


def get_msp_single_product_charts(request, product_id, month, year):
	if check_all_sessions(request) is not False:
		template = "managment/msproducts/product_chart.html"
		product = get_object_or_404(MS_Products, pk=product_id)
		if product.product.company.pk == request.session['pk']:
			smsp_context = {}

			sales = MS_ReceiptDetails.objects.filter(product=product.pk, saved_date__month=month, saved_date__year=year).values('saved_date').annotate(total_totals=Sum('total'), total_quantity=Sum('quantity')) if int(month) != 0 else MS_ReceiptDetails.objects.filter(product=product.pk, saved_date__year=year).values('item_price').annotate(saved_date=TruncMonth('saved_date'), total_totals=Sum('total'), total_quantity=Sum('quantity'))
			first_date = MS_ReceiptDetails.objects.filter(product=product.pk).first()
			last_date = MS_ReceiptDetails.objects.filter(product=product.pk).last()
			smsp_context['l_day'] = last_date.saved_date.day if last_date else None
			smsp_context['f_day'] = first_date.saved_date.day if first_date else None

			line_chart = pygal.StackedLine(interpolate='cubic')
			line_chart.title = 'Sales Evolution For %s, %s' % (get_month_name(month), year) if int(month) != 0 else 'Sales Evolution For %s' % year
			line_chart.x_labels = map(str, [p["saved_date"] for p in sales]) if int(month) != 0 else map(str, ["%s (%s)" % (get_month_name(p["saved_date"].month), intword(p["item_price"])) for p in sales])
			line_chart.add(product.product.product_name, [p["total_quantity"] for p in sales])
			smsp_context['graph'] = line_chart.render_data_uri()

			smsp_context['product'] = product
			smsp_context['product_purchases'] = MS_ProductEntry.objects.filter(product=product.pk).order_by('-entry_date')
			return render(request, template, smsp_context)
	else:
		messages.error(request, "Login as Admin Please !!!")
		return HttpResponseRedirect('/managment/welcome/')


#daily inventory

def get_month_receipts(request, month, year):
	if int(month) != 0:
		receipts = MS_Receipts.objects.filter(company=request.session['ms'], saved_date__month=month, saved_date__year=year)
		receipts_count = 0
		if receipts:
			for receipt in receipts:
				receipts_count += 1
		return int(receipts_count)
	else:
		receipts = MS_Receipts.objects.filter(company=request.session['ms'], saved_date__year=year)
		receipts_count = 0
		if receipts:
			for receipt in receipts:
				receipts_count += 1
		return int(receipts_count)


def group_dates_since_begining(request):
	first_sale = MS_Receipts.objects.filter(company=request.session['ms']).first()
	first_sale_date = first_sale.saved_date
	today = datetime.now().date()

	dates = []

	for y in range(first_sale_date.year, today.year + 1):
		dates.append({"month":0, "year":y, "value":y, "receipts":get_month_receipts(request, 0, y)})
		if first_sale_date.month != 1 and first_sale_date.year == y:
			if first_sale_date.month < today.month:
				for m in range(first_sale_date.month, today.month + 1):
					dates.append({"month":m, "year":y, "value":"%s, %s" % (get_month_name(m), y), "receipts":get_month_receipts(request, m, y)})
			else:
				for m in range(first_sale_date.month, 13):
					dates.append({"month":m, "year":y, "value":"%s, %s" % (get_month_name(m), y), "receipts":get_month_receipts(request, m, y)})
		else:
			if y == today.year:
				for m in range(1, today.month + 1):
					dates.append({"month":m, "year":y, "value":"%s, %s" % (get_month_name(m), y), "receipts":get_month_receipts(request, m, y)})
			else:
				for m in range(1, 13):
					dates.append({"month":m, "year":y, "value":"%s, %s" % (get_month_name(m), y), "receipts":get_month_receipts(request, m, y)})
	return dates[::-1]


def get_daily_managment_ms(request):
	if check_all_sessions(request) is not False:
		template = "managment/ms_day.html"
		company_name = request.session['company_name']
		company = Company.objects.get(name_dotted = company_name)
		product_form = ProductForm()
		com_id = request.session['pk']
		categories = Categories.objects.filter(company=company.pk)
		ms_session = MS_CompanyAdministrator.objects.get(pk=request.session['ms'])
		licence_session = MS_LicenceKey.objects.get(company=ms_session.pk)
		today = datetime.now().date()

		dates_day = MS_Receipts.objects.filter(company=request.session['ms'], saved_date__lt=today).values('saved_date').annotate(receipts=Count('saved_date')).order_by('-saved_date')
		today_count_customers = MS_Receipts.objects.filter(company=request.session['ms'], saved_date=today)
		
		today_count = 0
		
		if today_count_customers:
			for bill in today_count_customers:
				today_count += 1
		else:
			today_count = 0

		msd_context = {}
		msd_context.update(csrf(request))
		msd_context['company'] = company
		msd_context['session_company'] = company_name
		msd_context['categories'] = categories
		msd_context['product_form'] = product_form
		msd_context['post_form'] = PostForm()
		msd_context['ms_session'] = ms_session
		msd_context['licence_session'] = licence_session
		msd_context['admin_session'] = admin_session(request)
		msd_context['dates'] = dates_day
		msd_context['today_count'] = today_count
		msd_context['today'] = today
		msd_context['dates_month'] = group_dates_since_begining(request)
		msd_context['ip'] = getUserIpAddress(request)

		return render(request, template, msd_context)
	else:
		messages.error(request, "Login as Admin Please !!!")
		return HttpResponseRedirect('/managment/welcome/')


def get_daily_managment_ms_day(request, date):
	if check_all_sessions(request) is not False:
		template = "managment/msday/day_details.html"
		
		msd_context = {}

		day_totals = MS_Receipts.objects.filter(company=request.session['ms'], saved_date=date)
		customers = 0
		discounts = 0
		total_paid = 0
		total_net = 0

		if day_totals:
			for day in day_totals:
				customers += 1
				discounts += day.discount
				total_paid += day.total_paid
				total_net += day.total_net
		else:
			customers = 0
			discounts = 0
			total_paid = 0
			total_net = 0

		day_products = MS_ReceiptDetails.objects.filter(receipt__company=request.session['ms'], saved_date=date).values('product').annotate(customers=Count('product'), quantities=Sum('quantity'), totals=Sum('total')).order_by('-saved_date')
		msd_context['day_products'] = day_products
		msd_context['date'] = date
		msd_context['products'] = MS_Products.objects.filter(product__company=request.session['pk']) 
		msd_context['customers'] = customers
		msd_context['customers_detail'] = MS_Receipts.objects.filter(company=request.session['ms'], saved_date=date).order_by('-receipt_number')
		msd_context['discount'] = discounts
		msd_context['total_paid'] = total_paid
		msd_context['total_net'] = total_net
		msd_context['company'] = get_object_or_404(MS_CompanyAdministrator, pk=request.session['ms'])
		msd_context['setting'] = MS_Settings.objects.get(company=request.session['ms'])
		msd_context['today'] = datetime.now()
		
		return render(request, template, msd_context)
	else:
		messages.error(request, "Login as Admin Please !!!")
		return HttpResponseRedirect('/managment/welcome/')


def get_month_ms_quantities(product, month, year):
	details = MS_ReceiptDetails.objects.filter(product=product, saved_date__month=month, saved_date__year=year) if int(month) != 0 else MS_ReceiptDetails.objects.filter(product=product, saved_date__year=year)
	sum_quantities = 0
	for det in details:
		sum_quantities += det.quantity
	return sum_quantities


def get_month_ms_totals(product, month, year):
	details = MS_ReceiptDetails.objects.filter(product=product, saved_date__month=month, saved_date__year=year) if int(month) != 0 else MS_ReceiptDetails.objects.filter(product=product, saved_date__year=year)
	sum_totals = 0
	for det in details:
		sum_totals += det.total
	return sum_totals


def get_monthly_managment_ms_day(request, month, year):
	if check_all_sessions(request) is not False:
		template = "managment/msday/day_details.html"
		
		msd_context = {}

		day_totals = MS_Receipts.objects.filter(company=request.session['ms'], saved_date__month=month, saved_date__year=year) if int(month) != 0 else MS_Receipts.objects.filter(company=request.session['ms'], saved_date__year=year)
		customers = 0
		discounts = 0
		total_paid = 0
		total_net = 0

		if day_totals:
			for day in day_totals:
				customers += 1
				discounts += day.discount
				total_paid += day.total_paid
				total_net += day.total_net
		else:
			customers = 0
			discounts = 0
			total_paid = 0
			total_net = 0

		day_products = MS_ReceiptDetails.objects.filter(receipt__company=request.session['ms'], saved_date__month=month, saved_date__year=year).values('product').annotate(customers=Count('product'), quantities=Sum('quantity'), totals=Sum('total')).order_by('-saved_date') if int(month) != 0 else MS_ReceiptDetails.objects.filter(receipt__company=request.session['ms'], saved_date__year=year).values('product').annotate(customers=Count('product'), quantities=Sum('quantity'), totals=Sum('total')).order_by('-saved_date')
		day_product = []

		for day in day_products:
			day_product.append({"product": day["product"], "customers": day["customers"], "quantities": day["quantities"], "totals": day["totals"]})

		days_product = sorted(day_product, key = itemgetter('product')) #day_product.sort(key =lambda item : int(item["product"]))

		month_product = []

		for key, group in itertools.groupby(days_product, lambda item: int(item["product"])):
			month_product.append({
									"product": key, 
									"customers": sum(item["customers"] for item in group), 
									"quantities": get_month_ms_quantities(key, month, year), 
									"totals": get_month_ms_totals(key, month, year)
								})
		

		msd_context['day_products'] = month_product
		msd_context['date'] = "%s, %s" % (get_month_name(month), year) if int(month) != 0 else "%s" % year
		msd_context['products'] = MS_Products.objects.filter(product__company=request.session['pk']) 
		msd_context['customers'] = customers
		msd_context['customers_detail'] = MS_Receipts.objects.filter(company=request.session['ms'], saved_date__month=month, saved_date__year=year).order_by('-receipt_number') if int(month) != 0 else MS_Receipts.objects.filter(company=request.session['ms'], saved_date__year=year).order_by('-receipt_number')
		msd_context['discount'] = discounts
		msd_context['total_paid'] = total_paid
		msd_context['total_net'] = total_net
		msd_context['company'] = get_object_or_404(MS_CompanyAdministrator, pk=request.session['ms'])
		msd_context['setting'] = MS_Settings.objects.get(company=request.session['ms'])
		msd_context['month'] = int(month)
		msd_context['year'] = int(year)
		msd_context['today'] = datetime.now()

		return render(request, template, msd_context)
	else:
		messages.error(request, "Login as Admin Please !!!")
		return HttpResponseRedirect('/managment/welcome/')


def get_date_sales(product, date):
	sales = MS_ReceiptDetails.objects.filter(product=product, saved_date__lt=date)
	sales_count = 0
	for sale in sales:
		sales_count += sale.quantity
	return int(sales_count)


def get_date_stock(product, date):
	date = datetime.strptime(date, '%Y-%m-%d') + timedelta(days=1)
	purchases = MS_ProductEntry.objects.filter(product=product, entry_date__lt=date)
	purchases_count = 0
	for purchase in purchases:
		purchases_count += purchase.quantity_added
	return int(purchases_count)


def get_daily_managment_ms_day_chart(request, date):
	if check_all_sessions(request) is not False:
		template = "managment/msday/day_chart.html"
		
		msd_context = {}

		day_products = MS_ReceiptDetails.objects.filter(receipt__company=request.session['ms'], saved_date=date).values('product__product__product_name','product').annotate(customers=Count('product'), quantities=Sum('quantity'), totals=Sum('total'))
		stock = MS_Products.objects.filter(product__company=request.session['pk'])
		
		stocks = []

		for product in day_products:
			p_stock = get_date_stock(product["product"], date) - get_date_sales(product["product"], date)
			stocks.append({"product":product["product"], "stock":p_stock})

		line_chart = pygal.Bar()
		line_chart.title = 'Product Sales For %s' % date
		line_chart.x_labels = map(str, [s["product__product__product_name"] for s in day_products])
		line_chart.add("Products Stocks", [s["stock"] for s in stocks if s["product"] in [p["product"] for p in day_products]])
		line_chart.add("Products Sold", [s["quantities"] for s in day_products])
		
		msd_context['graph'] = line_chart.render_data_uri()
		msd_context['date'] = date
		msd_context['year'] = datetime.strptime(date, '%Y-%m-%d').year

		return render(request, template, msd_context)
	else:
		messages.error(request, "Login as Admin Please !!!")
		return HttpResponseRedirect('/managment/welcome/')


def get_date_sales_m(product, month, year):
	month = check_month_end_year(month)
	date = datetime(int(year), int(month) - 1, get_month_days(int(month) - 1, year)) if int(month) != 0 else datetime(int(year), 12, 31)
	sales = MS_ReceiptDetails.objects.filter(product=product, saved_date__lt=date)
	sales_count = 0
	for sale in sales:
		sales_count += sale.quantity
	return int(sales_count)


def get_date_stock_m(product, month, year):
	date = datetime(int(year), int(month), get_month_days(month, year)) + timedelta(days=1) if int(month) != 0 else datetime(int(year), 12, 31) + timedelta(days=1)
	purchases = MS_ProductEntry.objects.filter(product=product, entry_date__lt=date)
	purchases_count = 0
	for purchase in purchases:
		purchases_count += purchase.quantity_added
	return int(purchases_count)


def get_date_purchases_m(product, month, year):
	month_else = check_month_end_year(month)
	year_else = check_else_year(month, year)
	last_date = datetime(int(year), int(month), get_month_days(month, year)) if int(month) != 0 else datetime(int(year), 12, 31)
	previous_last_date = datetime(int(year_else), int(month_else) - 1, get_month_days(int(month_else) - 1, year_else)) if int(month) != 0 else datetime(int(year_else), 12, 31)
	purchases = MS_ProductEntry.objects.filter(product=product, entry_date__lt=last_date, entry_date__gt=previous_last_date) if int(month) != 0 else MS_ProductEntry.objects.filter(product=product, entry_date__year=year)
	purchases_count = 0
	for purchase in purchases:
		purchases_count += purchase.quantity_added
	return int(purchases_count)


def get_monthly_managment_ms_day_chart(request, month, year):
	if check_all_sessions(request) is not False:
		template = "managment/msday/day_chart.html"
		
		msd_context = {}

		day_products = MS_ReceiptDetails.objects.filter(receipt__company=request.session['ms'], saved_date__month=month, saved_date__year=year).values('product__product__product_name','product').annotate(customers=Count('product'), quantities=Sum('quantity'), totals=Sum('total')) if int(month) != 0 else MS_ReceiptDetails.objects.filter(receipt__company=request.session['ms'], saved_date__year=year).values('product__product__product_name','product').annotate(customers=Count('product'), quantities=Sum('quantity'), totals=Sum('total'))
		stock = MS_Products.objects.filter(product__company=request.session['pk'])
		
		stocks = []
		
		for product in day_products:
			p_stock = get_date_stock_m(product["product"], month, year) - get_date_sales_m(product["product"], month, year)
			stocks.append({"product":product["product"], "stock":p_stock, "purchase": get_date_purchases_m(product["product"], month, year)})

		line_chart = pygal.Bar()
		line_chart.title = 'Product Sales For %s, %s' % (get_month_name(month), year) if int(month) != 0 else 'Product Sales For %s' % year
		line_chart.x_labels = map(str, [s["product__product__product_name"] for s in day_products])
		line_chart.add("Products Stocks", [s["stock"] for s in stocks if s["product"] in [p["product"] for p in day_products]])
		line_chart.add("Products Purchased", [s["purchase"] for s in stocks if s["product"] in [p["product"] for p in day_products]])
		line_chart.add("Products Sold", [s["quantities"] for s in day_products])
		
		msd_context['graph'] = line_chart.render_data_uri()
		msd_context['date'] = '%s, %s' % (get_month_name(month), year) if int(month) != 0 else '%s' % year
		msd_context['year'] = int(year)

		return render(request, template, msd_context)
	else:
		messages.error(request, "Login as Admin Please !!!")
		return HttpResponseRedirect('/managment/welcome/')


#USERS Inventory


def get_customers_managment_ms(request):
	if check_all_sessions(request) is not False:
		template = "managment/ms_users.html"
		company_name = request.session['company_name']
		company = Company.objects.get(name_dotted = company_name)
		product_form = ProductForm()
		com_id = request.session['pk']
		categories = Categories.objects.filter(company=company.pk)
		ms_session = MS_CompanyAdministrator.objects.get(pk=request.session['ms'])
		licence_session = MS_LicenceKey.objects.get(company=ms_session.pk)

		msc_context = {}
		msc_context.update(csrf(request))
		msc_context['company'] = company
		msc_context['session_company'] = company_name
		msc_context['categories'] = categories
		msc_context['product_form'] = product_form
		msc_context['post_form'] = PostForm()
		msc_context['ms_session'] = ms_session
		msc_context['licence_session'] = licence_session
		msc_context['admin_session'] = admin_session(request)

		return render(request, template, msc_context)
	else:
		messages.error(request, "Login as Admin Please !!!")
		return HttpResponseRedirect('/managment/welcome/')


def get_msc_all_customers(request):
	if check_all_sessions(request) is not False:
		template = "managment/mscustomers/customers.html"
		msc_context = {}
		msc_context['customers'] = MS_Receipts.objects.filter(company=request.session['ms']).values('user').annotate(sales=Count('user')).exclude(user=None)
		msc_context['users'] = User.objects.all()
		msc_context['anonymous_customers'] = MS_Receipts.objects.filter(company=request.session['ms'], user=None).count()
		return render(request, template, msc_context)
	else:
		messages.error(request, "Login as Admin Please !!!")
		return HttpResponseRedirect('/managment/welcome/')


def get_msc_single_customers(request, user_id):
	if check_all_sessions(request) is not False:
		template = "managment/mscustomers/customer_details.html"
		msc_context = {}
		user_bills = MS_Receipts.objects.filter(user=user_id, company=request.session['ms']).order_by('-receipt_number')
		total = 0
		discount = 0
		total_net = 0

		if user_bills:
			for bill in user_bills:
				total +=bill.total_paid
				discount += bill.discount
				total_net += bill.total_net
		else:
			total = 0
			discount = 0
			total_net = 0

		msc_context['user'] = User.objects.get(pk=user_id)
		msc_context['user_bills'] = user_bills
		msc_context['total'] = total
		msc_context['discount'] = discount
		msc_context['total_net'] = total_net
		msc_context['setting'] = MS_Settings.objects.get(company=request.session['ms'])

		return render(request, template, msc_context)
	else:
		messages.error(request, "Login as Admin Please !!!")
		return HttpResponseRedirect('/managment/welcome/')


def get_msc_anonymous_customers(request):
	if check_all_sessions(request) is not False:
		template = "managment/mscustomers/customer_details.html"
		msc_context = {}
		user_bills = MS_Receipts.objects.filter(user=None, company=request.session['ms']).order_by('-receipt_number')
		total = 0
		discount = 0
		total_net = 0

		if user_bills:
			for bill in user_bills:
				total +=bill.total_paid
				discount += bill.discount
				total_net += bill.total_net
		else:
			total = 0
			discount = 0
			total_net = 0
		msc_context['anonymous'] = True
		msc_context['user_bills'] = user_bills
		msc_context['total'] = total
		msc_context['discount'] = discount
		msc_context['total_net'] = total_net
		msc_context['setting'] = MS_Settings.objects.get(company=request.session['ms'])

		return render(request, template, msc_context)
	else:
		messages.error(request, "Login as Admin Please !!!")
		return HttpResponseRedirect('/managment/welcome/')


def get_msc_customers_world_sale(request):
	if check_all_sessions(request) is not False:
		template = "managment/mscustomers/customers_chart.html"
		msc_context = {}
		return render(request, template, msc_context)


def customer_ms_send_mail(request, user_id):
	if request.method == "POST":
		email = request.POST.get('email','')
		subject = request.POST.get('subject','')
		message = request.POST.get('message','')

		send_mail(subject, 
			message, 
			settings.EMAIL_HOST_USER, 
			[email],
			html_message=message, 
			fail_silently=True)

		return HttpResponse("Email Message Sent Successfully !!!")
	else:
		if check_all_sessions(request):
			template = "managment/mscustomers/send_email.html"
			msc_context = {}
			msc_context.update(csrf(request))
			msc_context['user'] = get_object_or_404(User, pk=user_id)

			return render(request, template, msc_context)


#DATA INVENT


def get_data_managment_ms(request):
	if check_all_sessions(request) is not False:
		template = "managment/ms_data.html"
		company_name = request.session['company_name']
		company = Company.objects.get(name_dotted = company_name)
		product_form = ProductForm()
		com_id = request.session['pk']
		categories = Categories.objects.filter(company=company.pk)
		ms_session = MS_CompanyAdministrator.objects.get(pk=request.session['ms'])
		licence_session = MS_LicenceKey.objects.get(company=ms_session.pk)

		msdt_context = {}
		msdt_context.update(csrf(request))
		msdt_context['company'] = company
		msdt_context['session_company'] = company_name
		msdt_context['categories'] = categories
		msdt_context['product_form'] = product_form
		msdt_context['post_form'] = PostForm()
		msdt_context['ms_session'] = ms_session
		msdt_context['licence_session'] = licence_session
		msdt_context['admin_session'] = admin_session(request)

		return render(request, template, msdt_context)
	else:
		messages.error(request, "Login as Admin Please !!!")
		return HttpResponseRedirect('/managment/welcome/')


def get_msdt_trades_all(request):
	if check_all_sessions(request) is not False:
		template = "managment/msdata/trades_all.html"
		msdt_context = {}
		msdt_context.update(csrf(request))
		msdt_context['session_company'] = request.session['company_name']
		msdt_context['ms_company'] = MS_CompanyAdministrator.objects.get(pk=request.session['ms'])
		msdt_context['trades_products'] = ProductTrade.objects.filter(product__company=request.session['pk']).values('product').annotate(customers=Count('product'))
		msdt_context['products'] = Products.items.filter(company=request.session['pk'])
		msdt_context['agreed_trades'] = TradeAgreements.objects.filter(trade__product__company=request.session['pk']).count()
		msdt_context['setting'] = MS_Settings.objects.get(company=request.session['ms'])

		return render(request, template, msdt_context)
	else:
		messages.error(request, "Login as Admin Please !!!")
		return HttpResponseRedirect('/managment/welcome/')


def get_msdt_users_trades(request, product_id):
	if check_all_sessions(request) is not False:
		template = "managment/msdata/trades_users.html"
		msdt_context = {}
		msdt_context["product"] = get_object_or_404(Products, pk=product_id)
		msdt_context["trades"] = ProductTrade.objects.filter(product=product_id).order_by('-started_date')
		return render(request, template, msdt_context)
	else:
		messages.error(request, "Login as Admin Please !!!")
		return HttpResponseRedirect("/managment/welcome/")


@csrf_exempt
def agree_msdt_user_trade(request, trade_id):
	if check_all_sessions(request) is not False:
		if request.method == "POST":
			trade = get_object_or_404(ProductTrade, pk=trade_id)
			quantity = request.POST.get('quantity', '')
			price = request.POST.get('price','')
			status = "Not Finished"
			product = MS_Products.objects.filter(product=trade.product.pk)

			if product:
				if trade.status == "succeeded":
					agreed_date = datetime.now().date()
					trade_fail = datetime.now().date() + timedelta(days=7)
					agreement = TradeAgreements(
							trade=ProductTrade.objects.get(pk=trade_id),
							price=price,
							quantity=quantity,
							status=status,
							is_finished=False,
							agreement_date=agreed_date,
							finished_date=trade_fail
						)
					agreement.save()
					return HttpResponse("ok")
				else:
					return HttpResponse("You need to succeed the trade First !!!")
			else:
				return HttpResponse("The Product is not in managment system !!!")
	else:
		return HttpResponse("Login First as Admin !!!")


def get_msdt_agreed_trades(request):
	if check_all_sessions(request) is not False:
		template = "managment/msdata/trades_agreed.html"
		msdt_context = {}
		msdt_context['trades'] = TradeAgreements.objects.filter(trade__product__company=request.session['pk']).order_by('finished_date')
		msdt_context['setting'] = MS_Settings.objects.get(company=request.session['ms'])
		return render_to_response(template, msdt_context)
	else:
		messages.error(request, "Login as Admin Please !!!")
		return HttpResponseRedirect("/managment/welcome/")


def calculate_deadline_time(finished_date):
	deadline =  finished_date - datetime.now().date()
	today = datetime.now().date() - datetime.now().date()
	if deadline >= today:
		return deadline
	else:
		return "TRADE IS EXPIRED. UPDATE IT TO EXTEND TIME"


def get_msdt_single_agreed_trade(request, trade_id):
	if check_all_sessions(request) is not False:
		template = "managment/msdata/trade_agreed.html"
		msdt_context = {}
		trade = get_object_or_404(TradeAgreements, pk=trade_id)
		msdt_context.update(csrf(request))
		msdt_context['trade'] = trade
		msdt_context['deadline_days'] = calculate_deadline_time(trade.finished_date)
		msdt_context['setting'] = MS_Settings.objects.get(company=request.session['ms'])

		return render_to_response(template, msdt_context)
		
	elif 'username' in request.session:
		template = "managment/msdata/trade_agreed.html"
		msdt_context = {}
		trade = get_object_or_404(TradeAgreements, pk=trade_id)
		msdt_context.update(csrf(request))
		msdt_context['trade'] = trade
		msdt_context['deadline_days'] = calculate_deadline_time(trade.finished_date)
		msdt_context['session_user'] = request.session['user']

		return render_to_response(template, msdt_context)
	else:
		messages.error(request, "Login as Admin Please !!!")
		return HttpResponseRedirect("/managment/welcome/")


def update_msdt_single_agreed_trade(request, trade_id):
	if check_all_sessions(request) is not False:
		if request.method == "POST":
			quantity = request.POST.get('quantity','')
			price = request.POST.get('price','')
			days = request.POST.get('days','')
			trade = get_object_or_404(TradeAgreements, pk=trade_id)
			finished_date = trade.finished_date + timedelta(days=int(days))

			if int(days) in range(0,8):
				trade.quantity = quantity
				trade.price = price
				trade.finished_date = finished_date
				trade.save()
				return HttpResponse("ok")
			else:
				return HttpResponse("Days cannot be negative and cannot exceed 7 !!!")
	else:
		return HttpResponse("You have to log in as an Admin !!!")


@csrf_exempt
def add_msdt_trade_to_cart(request, trade_id):
	if check_all_sessions(request) is not False:
		if request.method == "POST":
			if 'bill' in request.session:
				bill_id = request.session['bill']
				trade = TradeAgreements.objects.get(pk=trade_id)
				check_item = MS_ReceiptDetails.objects.filter(receipt=bill_id, product__product__pk=trade.trade.product.pk)
				bill = MS_Receipts.objects.get(pk=bill_id)
				product = MS_Products.objects.get(product=trade.trade.product.pk)
				today = datetime.now().date()
				expary_date = trade.finished_date

				if trade.is_finished == True:
					return HttpResponse("This trade is finished. You must reactuvate it to use it !!!")
				else:
					if bill.user:
						if bill.user.pk == trade.trade.user.pk:
							if check_item:
								
								return HttpResponse("The product is already in the cart. Delete it and add this trade product !!!")
								
							else:

								if expary_date > today:

									if product.stock > trade.quantity:

										receipt_item = MS_ReceiptDetails(
												receipt=MS_Receipts.objects.get(pk=bill_id),
												product=MS_Products.objects.get(pk=product.pk),
												quantity=trade.quantity,
												item_price=float(trade.price) / int(trade.quantity),
												total=trade.price,
												is_trade=True,
												trade=TradeAgreements.objects.get(pk=trade_id),
												saved_date=datetime.now().date()
											)
										receipt_item.save()

										decrease_items(request, trade.quantity, product.pk)

										trade.status = "Finished"
										trade.is_finished = True
										trade.save()

										return HttpResponse("ok")

									else:

										return HttpResponse("Quantity is higher than Stock !!!")
								else:

									trade.status = "Expired"
									trade.save()

									return HttpResponse("The trade is expired. Update it first")
						else:
							return HttpResponse("The user is not the owner of the trade !!!")
					else:
						return HttpResponse("For Only Users not Anonimous !!!")
			else:
				return HttpResponse("No Session Bill")
	else:
		return HttpResponse("Log in as an Admin")


@csrf_exempt
def reactivate_msdt_agreed_trade(request, trade_id):
	if check_all_sessions(request) is not False:
		if request.method == "POST":
			trade = get_object_or_404(TradeAgreements, pk=trade_id)
			if trade.is_finished == True:
				trade.status = "Not Finished"
				trade.is_finished = False
				trade.agreement_date = datetime.now().date()
				trade.finished_date = datetime.now().date() + timedelta(days=7)
				trade.save()
				return HttpResponse("ok")
			else:
				return HttpResponse("You cant reactivate trade that aint finished !!!")
	else:
		return HttpResponse("Login as an admin, please !!!")


def get_msdt_product_interess(request):
	if check_all_sessions(request) is not False:
		template = "managment/msdata/interess.html"
		msdt_context = {}

		msdt_context.update(csrf(request))
		msdt_context["products"] = Products.items.filter(company=request.session["pk"]).order_by("-posted_date")
		return render_to_response(template, msdt_context)
	else:
		messages.error(request, "Login as Admin Please !!!")
		return HttpResponseRedirect('/managment/welcome/')


def get_msdt_single_product_interessers(request, product_id):
	if check_all_sessions(request) is not False:
		template = "managment/msdata/interessers.html"
		product = Products.items.get(pk=product_id)
		interesses = ProductInteress.objects.filter(product=product_id).order_by('user__full_name')
		likes = ProductMention.objects.filter(product=product_id, mention='like').order_by('user__full_name')
		dislikes = ProductMention.objects.filter(product=product_id, mention='dislike').order_by('user__full_name')
		comments = ProductComments.objects.filter(product=product_id).order_by('-comment_date')

		msdt_context = {}
		msdt_context.update(csrf(request))
		msdt_context['product'] = product
		msdt_context['interesses'] = interesses
		msdt_context['likes'] = likes
		msdt_context['dislikes'] = dislikes
		msdt_context['comments'] = comments
		
		return render_to_response(template, msdt_context)
	else:
		messages.error(request, "Login as Admin Please !!!")
		return HttpResponseRedirect('/managment/welcome/')


#MS TELLER

def get_teller_managment_ms(request):
	if check_all_sessions(request) is not False:
		template = "managment/ms_teller.html"
		company_name = request.session['company_name']
		company = Company.objects.get(name_dotted = company_name)
		product_form = ProductForm()
		com_id = request.session['pk']
		categories = Categories.objects.filter(company=company.pk)
		ms_session = MS_CompanyAdministrator.objects.get(pk=request.session['ms'])
		licence_session = MS_LicenceKey.objects.get(company=ms_session.pk)

		mstl_context = {}
		mstl_context.update(csrf(request))
		mstl_context['company'] = company
		mstl_context['session_company'] = company_name
		mstl_context['categories'] = categories
		mstl_context['product_form'] = product_form
		mstl_context['post_form'] = PostForm()
		mstl_context['ms_session'] = ms_session
		mstl_context['licence_session'] = licence_session
		mstl_context['admin_session'] = admin_session(request)

		return render(request, template, mstl_context)
	else:
		messages.error(request, "Login as Admin Please !!!")
		return HttpResponseRedirect('/managment/welcome/')


def get_company_tellers_all(request):
	if check_all_sessions(request) is not False:
		template = "managment/msteller/tellers.html"
		tellers = MS_CompanyTeller.objects.filter(company=request.session['ms']).order_by('-full_name')
		
		mstl_context = {}
		mstl_context.update(csrf(request))
		mstl_context['tellers'] = tellers

		return render(request, template, mstl_context)
	else:
		messages.error(request, "Login as Admin Please !!!")
		return HttpResponseRedirect('/managment/welcome/')


class AddTeller(TemplateView):

	template = "managment/msteller/add_teller.html"

	def get(self, request):
		if check_all_sessions(request) is not False:
			mstl_context = {}
			mstl_context.update(csrf(request))
			mstl_context['session_ms'] = request.session['ms']
			mstl_context['teller_form'] = MS_TellerForm()

			return render(request, self.template, mstl_context) 
		else:
			messages.error(request, "Login as Admin Please !!!")
			return HttpResponseRedirect('/managment/welcome/')


	def post(self, request):
		if check_all_sessions(request) is not None:
			if request.method == "POST":
				digits = ''.join(string.digits)
				password = ''.join(random.choice(digits) for _ in range(8))

				_admin = request.POST.get('is_admin', '')

				teller = MS_TellerForm(request.POST, request.FILES, instance=MS_CompanyTeller(
						company=MS_CompanyAdministrator.objects.get(pk=request.session['ms']),
						password=password,
						is_admin=True if _admin is "on" else False,
						registration_date=datetime.now()
					))

				teller.save()

				return HttpResponse("Tailler Saved Successfully !!! Password: %s" % password)
			else:
				pass
		else:
			return HttpResponse("<p class=''xl-error'>PLEASE, LOGIN</p>")


def login_teller(request):
	if 'ms' in request.session:
		if request.method == "POST":
			username = request.POST.get('teller_username', '')
			password = request.POST.get('teller_password', '')

			teller = MS_CompanyTeller.objects.filter(company=request.session['ms'], username=username, password=password).first()

			if teller:

				request.session['teller'] = teller.pk

				messages.success(request, "Teller has logged in Successfully !!!")
				return HttpResponseRedirect('/managment/hms_c/')
			else:
				messages.error(request, "Teller Not Found !!!")
				return HttpResponseRedirect('/managment/hms_c/')
		else:
			pass
	else:
		messages.error(request, "Login Managment System !!!")
		return HttpResponseRedirect('/managment/welcome/')


def logout_teller(request):
	if check_sm_ms_sessions(request) is not None:
		if 'teller' in request.session:
			try:
				del request.session['teller']
			except KeyError:
				pass
		if 'admin' in request.session:
			try:
				del request.session['admin']
			except KeyError:
				pass
	messages.success(request, "Teller has logged Out Successfully !!!")
	return HttpResponseRedirect('/managment/hms_c/')


def get_company_single_teller(request, teller_id):
	if check_all_sessions(request) is not False:
		template = "managment/msteller/teller.html"
		teller = get_object_or_404(MS_CompanyTeller, pk=teller_id)

		if teller.company.pk == request.session['ms']:
			mstl_context = {}
			mstl_context.update(csrf(request))
			mstl_context['teller'] = teller
			mstl_context['customers_detail'] = MS_Receipts.objects.filter(company=request.session['ms'], teller=teller.pk).order_by('-receipt_number')
			mstl_context['setting']= MS_Settings.objects.get(company=request.session['ms'])
			
			return render(request, template, mstl_context)
		else:
			return HttpResponse("<p class='xl-error'>THIS TELLER DOESNT BELONG TO YOU</p>")
	else:
		messages.error(request, "Login as Admin Please !!!")
		return HttpResponseRedirect('/managment/welcome/')


def get_admin_update_teller(request, teller_id):
	if check_all_sessions(request) is not None:
		template = "managment/msteller/admin_update_teller.html"
		teller = get_object_or_404(MS_CompanyTeller, pk=teller_id)
		mstl_context = {}
		mstl_context.update(csrf(request))
		mstl_context['session_ms'] = request.session['ms']
		mstl_context['teller'] = teller
		mstl_context['teller_form'] = MS_AdminUpdateTeller(instance=MS_CompanyTeller.objects.get(pk=teller_id))
		return render(request, template, mstl_context)
	else:
		messages.error(request, "Login as Admin Please !!!")
		return HttpResponseRedirect('/managment/welcome/')


def admin_save_update_teller(request, teller_id):
	if check_all_sessions(request) is not None:
		if request.method == "POST":
			teller_form = MS_AdminUpdateTeller(request.POST, request.FILES)
			teller = MS_CompanyTeller.objects.get(pk=teller_id)

			if teller.company.pk == request.session['ms']:

				if teller_form.is_valid():

					teller.full_name = teller_form.cleaned_data['full_name']
					teller.email = teller_form.cleaned_data['email']
					teller.address = teller_form.cleaned_data['address']
					teller.phone_number = teller_form.cleaned_data['phone_number']

					teller.save()

					return HttpResponse("ok")
				else:
					return HttpResponse("Error: %s" % teller_form.errors)
			else:
				return HttpResponse("<p class='xl-error'>THIS TELLER DOESNT BELONG TO YOU</p>")

		else:
			pass
	else:
		messages.error(request, "Login as Admin Please !!!")
		return HttpResponseRedirect('/managment/welcome/')


@csrf_exempt
def admin_make_teller_admin(request, teller_id):
	if check_all_sessions(request) is not None:
		if request.method == "POST":
			teller = MS_CompanyTeller.objects.get(pk=teller_id)

			if teller.company.pk == request.session['ms']:
				if teller.is_admin == True:
					teller.is_admin = False
					teller.save()
					return HttpResponse("Teller admin set to False !!!")
				else:
					teller.is_admin = True
					teller.save()
					return HttpResponse("Teller admin set to True !!!")
			else:
				return HttpResponse("THIS TELLER DOESNT BELONG TO YOU!!!")
		else:
			pass
	else:
		return HttpResponse("Only For Company Admins")


def load_teller_profile(request, teller_id):
	if check_sm_ms_sessions(request) is not None and 'teller' in request.session:
		template = "managment/msteller/teller_profile.html"
		teller = MS_CompanyTeller.objects.get(pk=teller_id)

		if teller.pk == request.session['teller']:
			
			mstl_context = {}
			mstl_context.update(csrf(request))
			mstl_context['teller'] = teller
			mstl_context['session_teller'] = True

			return render(request, template, mstl_context)
		else:
			return HttpResponse("TRYING TO REACH SOMEONE ELSE'S ACCOUNT !!!")
	else:
		return HttpResponse("TRY TO LOGIN  AS TELLER")


def update_teller_username(request):
	if 'teller' in request.session:
		teller = MS_CompanyTeller.objects.get(pk=request.session['teller'])
		if request.method == 'POST':
			username = request.POST.get('new_username', '')
			password = request.POST.get('password', '')

			if username != "" and password == "":

				if teller.password == password:
					teller.username = username
					teller.save()

					return HttpResponse("ok")
				else:
					return HttpResponse("Incorrect Password !!!")
			else:
				return HttpResponse("Fill Up All Fields Please !!!")
		else:
			return HttpResponse("BAD REQUEST")
	else:
		raise KeyError


def update_teller_password(request):
	if 'teller' in request.session:
		teller = MS_CompanyTeller.objects.get(pk=request.session['teller'])
		
		if request.method == 'POST':
			
			old_password = request.POST.get('current_password', '')
			new_password = request.POST.get('new_password', '')
			conf_password = request.POST.get('conf_password', '')

			if teller.password == old_password:
				
				if new_password == conf_password:
					
					teller.password = new_password
					teller.save()

					return HttpResponse("ok")
				else:
					return HttpResponse("New Passwords didnt match !!!")
			else:
				return HttpResponse("Old Password Incorrect !!!")
		else:
			return HttpResponse("BAD REQUEST")
	else:
		raise KeyError


#MS E COMMERCE


def get_ecommerce_managment_ms(request):
	if check_all_sessions(request):
		template = "managment/ms_ecommerce.html"
		company_name = request.session['company_name']
		company = Company.objects.get(name_dotted = company_name)
		product_form = ProductForm()
		com_id = request.session['pk']
		categories = Categories.objects.filter(company=company.pk)
		ms_session = MS_CompanyAdministrator.objects.get(pk=request.session['ms'])
		licence_session = MS_LicenceKey.objects.get(company=ms_session.pk)

		msec_context = {}
		msec_context.update(csrf(request))
		msec_context['company'] = company
		msec_context['session_company'] = company_name
		msec_context['categories'] = categories
		msec_context['product_form'] = product_form
		msec_context['post_form'] = PostForm()
		msec_context['ms_session'] = ms_session
		msec_context['licence_session'] = licence_session
		msec_context['admin_session'] = admin_session(request)

		return render(request, template, msec_context)
	else:
		messages.error(request, "Login as Admin Please !!!")
		return HttpResponseRedirect('/managment/welcome/')


def get_msec_customers(request):
	if check_all_sessions(request):
		template = "managment/msecommerce/customers_list.html"
		msec_context = {}
		msec_context.update(csrf(request))
		msec_context["customers"] = EC_MarketAccess.objects.filter(company=request.session['ms'])
		return render(request, template, msec_context)
	else:
		return HttpResponse("MS and Admin Sessions Required")


def change_user_market_access_status(request, market):
	if check_all_sessions(request):
		status = request.GET.get('status')
		market = EC_MarketAccess.objects.get(pk=market)
		statuses = ["vip", "disallowed", "blocked"]

		if status in statuses:
			market.status = status
			market.save()
			return HttpResponse("ok")

		else:
			return HttpResponse("Unknown Market Access Status")
	else:
		return HttpResponse("MS and Admin Sessions Required")


def get_msec_customer_carts(request, market):
	if check_all_sessions(request):
		template = "managment/msecommerce/customer_carts.html"
		msec_context = {}
		msec_context.update(csrf(request))
		market = EC_MarketAccess.objects.get(pk=market)
		msec_context['market'] = market
		msec_context['carts'] = EC_ShoppingCart.objects.filter(market=market.pk).order_by('-saved_date')
		return render(request, template, msec_context)
	else:
		return HttpResponse("MS and Admin Sessions Required")


def get_msec_customer_single_cart(request, cart):
	if check_all_sessions(request):
		template = "managment/msecommerce/cart_details.html"
		msec_context = {}
		msec_context.update(csrf(request))

		cart = EC_ShoppingCart.objects.get(pk=cart)
		items = EC_ShoppingCartItems.objects.filter(cart=cart.pk).order_by('-saved_date')
		msec_context['items'] = items
		msec_context['total'] = cart.get_cart_total()
		msec_context['cart'] = cart
		msec_context['currency'] = cart.market.company.get_currency()
		msec_context['company'] = MS_CompanyAdministrator.objects.get(pk=request.session['ms'])

		return render(request, template, msec_context)
	else:
		return HttpResponse("MS and Admin Sessions Required")


def accept_or_decline_order(request, cart):
	if check_all_sessions(request):
		status = request.GET.get('status')
		statuses = ["accepted", "suspended"]
		cart = EC_ShoppingCart.objects.get(pk=cart)
		if status in statuses:
			cart.status = status
			cart.save()
			return HttpResponse("ok")
		else:
			return HttpResponse("Unknown Status")
	else:
		return HttpResponse("MS and Admin Sessions Required")


def add_shopping_cart_to_ms(request, cart):
	if check_all_sessions(request):
		cart = get_object_or_404(EC_ShoppingCart, pk=cart)
		
		if cart.market.company.pk == request.session['ms']:

			last_bill_id = MS_Receipts.objects.filter(company=request.session['ms']).order_by('receipt_number').last()

			if last_bill_id:
				bill_number = last_bill_id.receipt_number + 1
			else:
				bill_number = 1

			check_bill = MS_Receipts.objects.filter(company=request.session['ms'], receipt_number=bill_number)
			
			if check_bill is None:
				
				ms_receipt = MS_Receipts(
						company=MS_CompanyAdministrator.objects.get(pk=request.session['ms']),
						user=User.objects.get(pk=user_id),
						teller=MS_CompanyTeller.objects.get(pk=request.session['teller']) if 'teller' in request.session else None,
						receipt_number=bill_number,
						status="created",
						saved_date_timezone=today_now,
						saved_date=datetime.now().date()
					)
				ms_receipt.save()

				items = EC_ShoppingCartItems.objects.filter(cart=cart.pk)

				for item in items:

					receipt_item = MS_ReceiptDetails(
						receipt=MS_Receipts.objects.get(pk=ms_receipt.pk),
						product=MS_Products.objects.get(pk=item.product.pk),
						quantity=item.quantity,
						item_price=item.item_price,
						total=item.total,
						saved_date=datetime.now().date()
					)
					decrease_items(request, int(item.quantity), item.product.pk)
					receipt_item.save()

				
				ms_receipt.status="success"
				ms_receipt.discount=0
				ms_receipt.total_paid=cart.total_paid
				ms_receipt.other_charges=cart.others_chargers
				ms_receipt.total_net=cart.total_net
				ms_receipt.paid_by="ec_%s" % cart.payment_mode
				ms_receipt.saved_date=datetime.now().date()
				ms_receipt.save()

				send_bill_email(request, ms_receipt.pk)

				return HttpResponse("Cart Added To MS !!!")
			else:
				return HttpResponse("Try Again !!!")
		else:
			return HttpResponse("Not Owner")
	else:
		return HttpResponse("MS and Admin Sessions Required")


#MS SETTINGS


def get_settings_managment_ms(request):
	if check_all_sessions(request) is not False:
		template = "managment/ms_settings.html"
		company_name = request.session['company_name']
		company = Company.objects.get(name_dotted = company_name)
		product_form = ProductForm()
		com_id = request.session['pk']
		categories = Categories.objects.filter(company=company.pk)
		ms_session = MS_CompanyAdministrator.objects.get(pk=request.session['ms'])
		licence_session = MS_LicenceKey.objects.get(company=ms_session.pk)

		msst_context = {}
		msst_context.update(csrf(request))
		msst_context['company'] = company
		msst_context['session_company'] = company_name
		msst_context['categories'] = categories
		msst_context['product_form'] = product_form
		msst_context['post_form'] = PostForm()
		msst_context['ms_session'] = ms_session
		msst_context['licence_session'] = licence_session
		msst_context['admin_session'] = admin_session(request)

		return render(request, template, msst_context)
	else:
		messages.error(request, "Login as Admin Please !!!")
		return HttpResponseRedirect('/managment/welcome/')


#General Settings


def get_msst_general_settings(request):
	if check_all_sessions(request) is not False:
		template = "managment/mssettings/general_set.html"
		msst_context = {}
		msst_context.update(csrf(request))
		ms_settings = MS_Settings.objects.get(company=request.session['ms'])
		msst_context['settings'] = ms_settings

		return render(request, template, msst_context)
	else:
		return HttpResponse("MS and Admin Sessions Required")


def check_ms_password(request, password):
	ms_admin = MS_CompanyAdministrator.objects.get(pk=request.session['ms'])
	if ms_admin.password == password:
		return "success"
	else:
		return None


class ReduceProductTrade(TemplateView):

	template = "managment/mssettings/g_reduce_prod.html"

	def get(self, request):
		if check_all_sessions(request) is not False:
			msst_context = {}
			text = "If you choose <b>True</b>, that means that the quantity that you've agreed for the trade will be  "
			text +=	"diducted to the stock after you've agreed but if you choose <b>False</b>, the quantity will be deducted "
			text +=	"to the stock when the customer will come to finalize the trade (buy)"
			ms_settings = MS_Settings.objects.get(company=request.session['ms'])
			msst_context.update(csrf(request))
			msst_context['text'] = text
			msst_context['setting'] = ms_settings
			return render_to_response(self.template, msst_context)
		else:
			return HttpResponse("MS and Admin Sessions Required")


	def post(self, request):
		if 'admin' in request.session:
			if request.method == 'POST':
				setting = request.POST.get('setting','')
				password = request.POST.get('password','')

				if check_ms_password(request, password) is not None:
					ms_settings = MS_Settings.objects.get(company=request.session['ms'])
					ms_settings.reduce_after_trade_agreed = setting
					ms_settings.save()
					return HttpResponse('ok')
				else:
					return HttpResponse("MS Password is Incorrect !!!")


class AllowUserSucceed(TemplateView):

	template = "managment/mssettings/g_allow_user.html"

	def get(self, request):
		if check_all_sessions(request) is not False:
			msst_context = {}
			text = "If set on <b>True</b>, users will be allowed to succeed trade, means that they can accept trade "
			text += " by themselves but this is not highly recommanded for company's self managment, by default, only companies "
			text += "are able to succeed trades"
			ms_settings = MS_Settings.objects.get(company=request.session['ms'])
			msst_context.update(csrf(request))
			msst_context['text'] = text
			msst_context['setting'] = ms_settings
			return render_to_response(self.template, msst_context)
		else:
			return HttpResponse("MS and Admin Sessions Required")


	def post(self, request):
		if 'admin' in request.session:
			if request.method == 'POST':
				setting = request.POST.get('setting','')
				password = request.POST.get('password','')

				if check_ms_password(request, password) is not None:
					ms_settings = MS_Settings.objects.get(company=request.session['ms'])
					ms_settings.allow_user_to_succeed = setting
					ms_settings.save()
					return HttpResponse('ok')
				else:
					return HttpResponse("MS Password is Incorrect !!!")


class PrintBill(TemplateView):

	template = "managment/mssettings/g_print_bill.html"

	def get(self, request):
		if check_all_sessions(request) is not False:
			msst_context = {}
			text = "If set on <b>True</b>, after a customer has finished his shopping and the cashier has received the money, "
			text += " the bill will be printed. But you can still decide to print or not but the receipt will always "
			text += " be sent to the customer's email address if provided"
			ms_settings = MS_Settings.objects.get(company=request.session['ms'])
			msst_context.update(csrf(request))
			msst_context['text'] = text
			msst_context['setting'] = ms_settings
			return render_to_response(self.template, msst_context)
		else:
			return HttpResponse("MS and Admin Sessions Required")

	def post(self, request):
		if 'admin' in request.session:
			if request.method == 'POST':
				setting = request.POST.get('setting','')
				password = request.POST.get('password','')

				if check_ms_password(request, password) is not None:
					ms_settings = MS_Settings.objects.get(company=request.session['ms'])
					ms_settings.print_bill = setting
					ms_settings.save()
					return HttpResponse('ok')
				else:
					return HttpResponse("MS Password is Incorrect !!!")



class Currency(TemplateView):

	template = "managment/mssettings/g_currency.html"

	def get(self, request):
		if check_all_sessions(request) is not False:
			msst_context = {}
			text = "This is the currency that you will be using in all managment system. Once set, it cannot be changed "
			text += "unless if you come to our offices or reset your managment system. It is highly recommanded to check the "
			text += "currency before you submit it. The default one will be USD"
			ms_settings = MS_Settings.objects.get(company=request.session['ms'])
			msst_context.update(csrf(request))
			msst_context['text'] = text
			msst_context['setting'] = ms_settings
			msst_context['currencies'] = CURRENCIES
			return render_to_response(self.template, msst_context)
		else:
			return HttpResponse("MS and Admin Sessions Required")


	def post(self, request):
		if 'admin' in request.session:
			if request.method == 'POST':
				setting = request.POST.get('setting','')
				password = request.POST.get('password','')

				if check_ms_password(request, password) is not None:
					ms_settings = MS_Settings.objects.get(company=request.session['ms'])
					if ms_settings.is_currency_changed == True:
						return HttpResponse("You cannot change the currency twice !!!")
					else:
						ms_settings.currency = setting
						ms_settings.is_currency_changed = True
						ms_settings.save()
						return HttpResponse('ok')
				else:
					return HttpResponse("MS Password is Incorrect !!!")



class Internationalize(TemplateView):

	template = "managment/mssettings/g_internat.html"

	def get(self, request):
		if check_all_sessions(request) is not False:
			msst_context = {}
			text = "If this is set on <b>True</b>, your products can be viewed internationaly and the price can be compared" 
			text += " in difference currency and compared to other similar product. This is not really recommanded to avoid "
			text += "useless and negative critics"
			ms_settings = MS_Settings.objects.get(company=request.session['ms'])
			msst_context.update(csrf(request))
			msst_context['text'] = text
			msst_context['setting'] = ms_settings
			return render_to_response(self.template, msst_context)
		else:
			return HttpResponse("MS and Admin Sessions Required")


	def post(self, request):
		if 'admin' in request.session:
			if request.method == 'POST':
				setting = request.POST.get('setting','')
				password = request.POST.get('password','')

				if check_ms_password(request, password) is not None:
					ms_settings = MS_Settings.objects.get(company=request.session['ms'])
					ms_settings.internationalize = setting
					ms_settings.save()
					return HttpResponse('ok')
				else:
					return HttpResponse("MS Password is Incorrect !!!")


class FreeAccessMarket(TemplateView):

	template = "managment/mssettings/g_free_access.html"

	def get(self, request):
		if check_all_sessions(request) is not False:
			msst_context = {}
			text = "If set on <b>True</b>, the user (customer) can access your market without your permission at anytime. "
			text += "This is not really recommanded because of keeping company or store's privacies if there are products "
			text += "that can only be accessible to the phisical store (not web)"
			ms_settings = MS_Settings.objects.get(company=request.session['ms'])
			msst_context.update(csrf(request))
			msst_context['text'] = text
			msst_context['setting'] = ms_settings
			return render_to_response(self.template, msst_context)
		else:
			return HttpResponse("MS and Admin Sessions Required")


	def post(self, request):
		if 'admin' in request.session:
			if request.method == 'POST':
				setting = request.POST.get('setting','')
				password = request.POST.get('password','')

				if check_ms_password(request, password) is not None:
					ms_settings = MS_Settings.objects.get(company=request.session['ms'])
					ms_settings.access_market = setting
					ms_settings.save()
					return HttpResponse('ok')
				else:
					return HttpResponse("MS Password is Incorrect !!!")


class TimeAccessMarket(TemplateView):

	template = "managment/mssettings/g_time_access.html"

	def get(self, request):
		if check_all_sessions(request) is not False:
			msst_context = {}
			text = "This is the maximum time a user can access your market. The defaut is set to 30 minutes"
			ms_settings = MS_Settings.objects.get(company=request.session['ms'])
			msst_context.update(csrf(request))
			msst_context['text'] = text
			msst_context['setting'] = ms_settings
			return render_to_response(self.template, msst_context)
		else:
			return HttpResponse("MS and Admin Sessions Required")


	def post(self, request):
		if 'admin' in request.session:
			if request.method == 'POST':
				setting = request.POST.get('setting','')
				password = request.POST.get('password','')

				if check_ms_password(request, password) is not None:
					ms_settings = MS_Settings.objects.get(company=request.session['ms'])
					if int(setting) > 0:
						if ms_settings.access_market == False:
							ms_settings.time_market_access = setting
							ms_settings.save()
							return HttpResponse('ok')
						else:
							return HttpResponse("Allow Free Access Market must be False")
					else:
						return HttpResponse("Time must be greater than 0")
				else:
					return HttpResponse("MS Password is Incorrect !!!")


def get_country_airline(countries, count):
	for country in countries:
		if country["country"] == count:
			return country
	return None


class AddMobileMoneyNumber(TemplateView):

	template =  "managment/mssettings/g_mobile.html"

	def get(self, request):
		if check_all_sessions(request) is not False:
			msst_context = {}
			text = "This is the maximum time a user can access your market. The defaut is set to 30 minutes"
			ms_settings = MS_Settings.objects.get(company=request.session['ms'])
			company = Company.objects.get(pk=request.session['pk'])
			msst_context.update(csrf(request))
			msst_context['text'] = text
			msst_context['setting'] = ms_settings
			msst_context['numbers'] = MS_CompanyMobile.objects.filter(company=request.session['ms'])
			msst_context['airlines'] = get_country_airline(settings.MOBILE_MONEY_AIRLINES, company.country)
			return render_to_response(self.template, msst_context)
		else:
			return HttpResponse("MS and Admin Sessions Required")


	def is_number(self, s):
	    try:
	        int(s)
	        return True
	    except ValueError:
	        pass
	 
	    try:
	        import unicodedata
	        unicodedata.numeric(s)
	        return True
	    except (TypeError, ValueError):
	        pass
	 
		return False


	def post(self, request):
		if check_all_sessions(request):
			if request.method  == "POST":
				number = request.POST.get('number', '')
				airline = request.POST.get('airline', '')
				password = request.POST.get('password', '')

				number = ''.join( c for c in number if  c not in ' -' )

				if number[1:].isdigit():

					if check_ms_password(request, password) is not None:

						mobile_number = MS_CompanyMobile(
								company=MS_CompanyAdministrator.objects.get(pk=request.session['ms']),
								airline=airline,
								number=number
							)
						mobile_number.save()

						return HttpResponse('ok')
					else:
						return HttpResponse("Wrong MS Password !!!")
				else:
					return HttpResponse("Enter a Valid Phone Number")
			else:
				return HttpResponse("Bad Request")
		else:
			return HttpResponse("MS and Admin Sessions Required")

	
	def remove(self, request, number):
		if check_all_sessions(request):
			number = MS_CompanyMobile.objects.get(pk=number)
			if number.company.pk == request.session['ms']:
				number.delete()
				return HttpResponse("ok")
			else:
				return HttpResponse("You are not the Owner")
		else:
			return HttpResponse("MS and Admin Sessions Required")

	
	def update(self, request, number):
		if check_all_sessions(request):
			pass
		else:
			return HttpResponse("MS and Admin Sessions Required")


class CommentProduct(TemplateView):

	template = "managment/mssettings/g_comment_prod.html"

	def get(self, request):
		if check_all_sessions(request) is not False:
			msst_context = {}
			text = "Add Mobile Money Number that you can use to get payment from customers in MS or EC"
			ms_settings = MS_Settings.objects.get(company=request.session['ms'])
			msst_context.update(csrf(request))
			msst_context['text'] = text
			msst_context['setting'] = ms_settings
			return render_to_response(self.template, msst_context)
		else:
			return HttpResponse("MS and Admin Sessions Required")


	def post(self, request):
		if 'admin' in request.session:
			if request.method == 'POST':
				setting = request.POST.get('setting','')
				password = request.POST.get('password','')

				if check_ms_password(request, password) is not None:
					ms_settings = MS_Settings.objects.get(company=request.session['ms'])
					ms_settings.comment_product = setting
					ms_settings.save()
					return HttpResponse('ok')
				else:
					return HttpResponse("MS Password is Incorrect !!!")
			else:
				return HttpResponse("Bad Request")
		else:
			return HttpResponse("MS and Admin Sessions Required")


#Security Settings


def get_msst_security_settings(request):
	if check_all_sessions(request) is not False:
		template = "managment/mssettings/security_set.html"
		msst_context = {}
		msst_context.update(csrf(request))
		ms_settings = MS_Settings.objects.get(company=request.session['ms'])
		msst_context['settings'] = ms_settings

		return render(request, template, msst_context)
	else:
		return HttpResponse("MS and Admin Sessions Required")


class ModifySMPassword(TemplateView):

	template = "managment/mssettings/s_sm_password.html"

	def get(self, request):
		if check_all_sessions(request) is not False:
			msst_context = {}
			msst_context.update(csrf(request))

			return render(request, self.template, msst_context)
		else:
			return HttpResponse("MS and Admin Sessions Required")


	def post(self, request):
		if check_all_sessions(request) is not False:
			if request.method == 'POST':
				old_password = request.POST.get('old_password', '')
				new_password = request.POST.get('new_password', '')
				new_password_c = request.POST.get('new_password_c','')
				company = Company.objects.get(pk=request.session['pk'])

				if company.password == old_password:
					if new_password  == new_password_c:
						if new_password != old_password:
							company.password = new_password
							company.save()
							return HttpResponse("ok")
						else:
							return HttpResponse("New and Old Passwords cannot be the same !!!")
					else:
						return HttpResponse("New Passwords didnt match !!!")
				else:
					return HttpResponse("Current Password Incorrect !!!")
			else:
				return HttpResponse("Bad Request")
		else:
			return HttpResponse('Login as Admin Please !!!')


class ModifyMSPassword(TemplateView):

	template = "managment/mssettings/s_ms_password.html"

	def get(self, request):
		if check_all_sessions(request) is not False:
			msst_context = {}
			msst_context.update(csrf(request))

			return render(request, self.template, msst_context)
		else:
			return HttpResponse("MS and Admin Sessions Required")


	def post(self, request):
		if check_all_sessions(request) is not False:
			if request.method == 'POST':
				old_password = request.POST.get('old_password', '')
				new_password = request.POST.get('new_password', '')
				new_password_c = request.POST.get('new_password_c','')
				
				if check_ms_password(request, old_password) is not None:
					if new_password  == new_password_c:
						if new_password != old_password:
							ms_company = MS_CompanyAdministrator.objects.get(pk=request.session['ms'])
							ms_company.password = new_password
							ms_company.save()
							return HttpResponse("ok")
						else:
							return HttpResponse("New and Old Passwords cannot be the same !!!")
					else:
						return HttpResponse("New Passwords didnt match !!!")
				else:
					return HttpResponse("Current Password Incorrect !!!")
			else:
				return HttpResponse("Bad Request")
		else:
			return HttpResponse('Login as Admin Please !!!')


class AlwaysAdmin(TemplateView):

	template = "managment/mssettings/s_admin.html"

	def get(self, request):
		if check_all_sessions(request) is not False:
			msst_context = {}
			text = "If set on <b>True</b>, evry logged in will be considered as an administrator but this is not really recommanded since"
			text += "not everyone can do anything in a company or a store"
			ms_settings = MS_Settings.objects.get(company=request.session['ms'])
			msst_context.update(csrf(request))
			msst_context['text'] = text
			msst_context['setting'] = ms_settings
			return render_to_response(self.template, msst_context)
		else:
			return HttpResponse("MS and Admin Sessions Required")


	def post(self, request):
		if check_all_sessions(request):
			if request.method == 'POST':
				setting = request.POST.get('setting','')
				password = request.POST.get('password','')

				if check_ms_password(request, password) is not None:
					ms_settings = MS_Settings.objects.get(company=request.session['ms'])
					ms_settings.always_admin = setting
					ms_settings.save()
					return HttpResponse('ok')
				else:
					return HttpResponse("MS Password is Incorrect !!!")


class LicenceKey(TemplateView):

	template = "managment/mssettings/licence_key.html"

	def get(self, request):
		if 'company_name' in request.session and 'admin' in request.session:
			mslk_context = {}
			mslk_context.update(csrf(request))
			mslk_context['ms_company'] = get_object_or_404(MS_CompanyAdministrator, pk=request.session['ms'])
			mslk_context['licence'] = MS_LicenceKey.objects.get(company=request.session['ms'])
			mslk_context['remaining'] = check_ms_licence_key(request)
			return render(request, self.template, mslk_context)
		else:
			return HttpResponse("MS and Admin Sessions Required")