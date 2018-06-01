# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from pip._vendor.requests import Response
from django.views.generic import TemplateView
from xlstore.models import *
from xlstore_managment.models import *
from xlstore_ecommerce.models import *
from xlstore.backends import email_check
from xlstore_managment.views import check_all_sessions, check_ms_password
from datetime import datetime, timedelta, date
import string
import random
import pytz


utc = pytz.UTC
today_now = datetime.now().replace(tzinfo=utc)

# Create your views here.

def save_user_ecommerce_settings(admin_id):
	ecommerce_settings = EC_CompanySettings(
			company=MS_CompanyAdministrator.objects.get(pk=admin_id)
		)
	ecommerce_settings.save()


def user_request_access_market(request):
	if 'username' in request.session:
		if request.method == "POST":
			allowed_chars = ''.join((string.lowercase, string.uppercase, string.digits))
			key = ''.join(random.choice(allowed_chars) for _ in range(8))
			company = request.POST.get('company', '')
			user = request.session['user']
			ms_company = MS_CompanyAdministrator.objects.get(company=company)

			if ms_company is not None:
				check_access_market = EC_MarketAccess.objects.filter(company=ms_company.pk, user=user).first()
				
				if check_access_market is None:
					market = EC_MarketAccess(
							user=User.objects.get(pk=user),
							company=MS_CompanyAdministrator.objects.get(pk=ms_company.pk),
							key=key,
							status="disallowed",
							key_date=today_now
						)
					market.save()
					return HttpResponse("ok")
				else:
					return HttpResponse("ok")
			else:
				return HttpResponse("Company is Not Registered in MS !!!")
		else:
			return HttpResponse("Error Method")
	else:
		return HttpResponse("Login As Admin Please !!!")


def check_user_access_market_user(request, user, company):
	if user is not "" and company is not "":
		ms_company = MS_CompanyAdministrator.objects.get(company=company)
		check_access_market = EC_MarketAccess.objects.filter(company=ms_company.pk, user=user).first()
		
		if check_access_market is not None:
			return HttpResponse(json.dumps(check_access_market.get_access_market_json(), default=str))
		else:
			return HttpResponse("Error")
	else:
		return HttpResponse("Error")


def company_allow_user_access_market(request, key):
	if check_all_sessions(request):
		market_access = EC_MarketAccess.objects.get(key=key)
		settings = MS_Settings.objects.get(company=request.session['ms'])
		status = request.GET.get('status')
		if market_access is not None and market_access.company.pk == request.session['ms']:
			if market_access.status == "vip":
				return HttpResponse(json.dumps(market_access.get_access_market_json(), default=str))
			elif market_access.status == "bloked":
				return HttpResponse("bloked")
			else:
				if status == "allow":
					market_access.status = "allowed"
					if settings.access_market == True:
						market_access.access_time = settings.time_market_access
						market_access.time_from = datetime.now()
						market_access.time_to = datetime.now() + timedelta(minutes=int(settings.time_market_access))
						market_access.save()
						return HttpResponse(json.dumps(market_access.get_access_market_json(), default=str))
					else:
						market_access.save()
						return HttpResponse(json.dumps(market_access.get_access_market_json(), default=str))
				elif status == "vip":
					market_access.status = "vip"
					market_access.save()
					return HttpResponse(json.dumps(market_access.get_access_market_json(), default=str))
				else:
					return HttpResponse("missing status")
		else:
			return HttpResponse("error")
	else:
		return HttpResponse("session")


def company_disallow_market_access(request, key):
	market_access = get_object_or_404(EC_MarketAccess, key=key)
	if market_access.status == "allowed" or market_access.status == "disallowed":
		market_access.status == "disallowed"
		market_access.access_time = None
		market_access.from_time = None
		market_access.to_time = None
		market_access.save()
		return HttpResponse("disallowed")
	else:
		return HttpResponse("Cant disallow acccess for access is %s" % market_access.status)


def load_and_await_market(request, company):
	if 'username' in request.session:
		template = "ecommerce/market.html"
		company = Company.objects.get(pk=company)
		ms_market = {}
		ms_market["session_user"] = request.session['username']
		ms_market["company"] = company
		ms_market["user"] = User.objects.get(pk=request.session['user'])

		return render(request, template, ms_market)
	else:
		return HttpResponse("USER SESSION REQUIRED")


def error_access_market(request):
	return HttpResponse("<p class='xl-error'>Cant Access Market, Access Blocked</p>")


def start_new_or_get_last_shopping(request, user):
	if 'username' in request.session:
		key = request.GET.get("key")
		user = User.objects.get(pk=user)
		market_access = EC_MarketAccess.objects.get(key=key)

		if user.pk == request.session['user'] and market_access.user.pk == user.pk:
			
			template = "ecommerce/start.html"
			market_context = {}
			last_shopping = EC_ShoppingCart.objects.filter(market=market_access.pk).last()

			statuses = ["created", "finished", "accepted"]
			
			if last_shopping is not None and last_shopping.status in statuses:
				
				last_shopping_items = EC_ShoppingCartItems.objects.filter(cart=last_shopping.pk)
				
				total = 0
				if last_shopping_items is not None:
					for item in last_shopping_items:
						total += item.total

				market_context["status"] = last_shopping.status
				market_context["shopping"] = last_shopping
				market_context["items"] = last_shopping_items
				market_context["total"] = total
				market_context["currency"] = market_access.company.get_currency()
			else:
				market_context["status"] = last_shopping.status if last_shopping is not None else None

			market_context["user"] = user
			market_context["session_user"] = request.session["user"]
			market_context["company"] = Company.objects.get(pk=market_access.company.company.pk)
			market_context["market"] = market_access
			market_context["none"] = 0

			return render(request, template, market_context)
		else:
			return HttpResponse("Session and Owner Didnt Match")
	else:
		return HttpResponse("User Session Required")


def load_market_products(request, key, cart=None):
	if 'username' in request.session:
		template = "ecommerce/market_products.html"
		option = request.GET.get('last_option')

		check_access = EC_MarketAccess.objects.get(key=key)
		company = Company.objects.get(pk=check_access.company.company.pk)
		products = MS_Products.objects.filter(product__company=company.pk)

		ms_market = {}
		ms_market.update(csrf(request))

		last_shopping = EC_ShoppingCart.objects.filter(market=check_access.pk, status="accepted")

		if last_shopping is not None:

			if option == "create":

				shopping_cart = EC_ShoppingCart(
						market=EC_MarketAccess.objects.get(pk=check_access.pk),
						status="created",
						saved_date=today_now
					)
				shopping_cart.save()
				ms_market["shopping_cart"] = shopping_cart
				ms_market["status"] = shopping_cart.status

			elif option == "continue":
				shopping_cart = EC_ShoppingCart.objects.get(pk=cart)
				shopping_cart.status = "created"
				shopping_cart.save()
				ms_market["shopping_cart"] = shopping_cart
				ms_market["status"] = shopping_cart.status

			elif option == "suspend":

				last_shopping_cart = EC_ShoppingCart.objects.get(pk=cart)
				last_shopping_cart.status = "suspended"
				last_shopping_cart.save()
				shopping_cart = EC_ShoppingCart(
						market=EC_MarketAccess.objects.get(pk=check_access.pk),
						status="created",
						saved_date=today_now
					)
				shopping_cart.save()

				ms_market["shopping_cart"] = shopping_cart
				ms_market["status"] = shopping_cart.status

			elif option == "abbort":

				shopping_cart = EC_ShoppingCart.objects.get(pk=cart)
				shopping_cart_items = EC_ShoppingCartItems.objects.filter(cart=shopping_cart.pk)
				if shopping_cart_items is not None:
					for item in shopping_cart_items:
						item.delete()

				shopping_cart.status = "created"
				shopping_cart.saved_date = today_now
				shopping_cart.save()

				ms_market["shopping_cart"] = shopping_cart
				ms_market["status"] = shopping_cart.status

			else:
				shopping_cart = EC_ShoppingCart(
						market=EC_MarketAccess.objects.get(pk=check_access.pk),
						status="created",
						saved_date=today_now
					)
				shopping_cart.save()
				ms_market["shopping_cart"] = shopping_cart
				ms_market["status"] = shopping_cart.status


			ms_market["session_user"] = request.session['username']
			ms_market["company"] = company
			ms_market["products"] = products
			ms_market["currency"] = check_access.company.get_currency()
			ms_market["market"] = check_access
			ms_market["user"] = User.objects.get(pk=check_access.user.pk)

			return render(request, template, ms_market)
		else:
			return HttpResponse("<p class='xl-error'>Cant Create, Contunue or Suspend a cart when you have one which is accepted</p>")
	else:
		return HttpResponse("USER SESSION REQUIRED")


def load_shopping_cart(request, cart):
	if 'username' in request.session:
		data_type = request.GET.get('type')
		cart_context = {}
		cart_context.update(csrf(request))
		shopping_cart = EC_ShoppingCart.objects.get(pk=cart)
		company = Company.objects.get(pk=shopping_cart.market.company.company.pk)

		if request.session["user"] == shopping_cart.market.user.pk:
			items = EC_ShoppingCartItems.objects.filter(cart=shopping_cart.pk)
			quantity = 0
			total = 0

			if items is not None:
				for item in items:
					quantity += item.quantity
					total += item.total

			cart_context["shopping_cart"] = shopping_cart
			cart_context["status"] = shopping_cart.status
			cart_context["items"] = items
			cart_context["quantity"] = quantity
			cart_context["total"] = total
			cart_context["currency"] = shopping_cart.market.company.get_currency()
			cart_context["company"] = company
			cart_context["user"] = User.objects.get(pk=shopping_cart.market.user.pk)
			cart_context["market"] = EC_MarketAccess.objects.get(pk=shopping_cart.market.pk)

			if data_type == "data":
				template = "ecommerce/shopping_cart.html"
				return render(request, template, cart_context)
			else:
				template = "ecommerce/shopping_cart_items.html"
				return render(request, template, cart_context)

		else:
			return HttpResponse("USER NOT THE OWNER OF THE CART")
	else:
		return HttpResponse("USER SESSION REQUIRED")


def load_shopping_cart_json(request, cart):
	cart = EC_ShoppingCart.objects.get(pk=cart)
	if 'username' in request.session:
		if cart.market.user.pk == request.session['user']:
			return HttpResponse(json.dumps(cart.get_shopping_cart_json(), default=str))
		else:
			return HttpResponse("Not Owner")
	elif check_all_sessions(request):
		if cart.market.company.pk == request.session['ms']:
			return HttpResponse(json.dumps(cart.get_shopping_cart_json(), default=str))
		else:
			return HttpResponse("Not Owner")
	else:
		return HttpResponse("User or Company Session Required")


def load_shopping_cart_company(request, cart):
	if check_all_sessions(request):
		
		cart = EC_ShoppingCart.objects.get(pk=cart)
		cart_context = {}
		template = "ecommerce/company_cart_items.html"

		if cart.market.company.pk == request.session['ms']:
			items = EC_ShoppingCartItems.objects.filter(cart=cart.pk)
			quantity = 0
			total = 0

			if items is not None:
				for item in items:
					quantity += item.quantity
					total += item.total

			cart_context["cart"] = cart
			cart_context["items"] = items
			cart_context["quantity"] = quantity
			cart_context["total"] = total
			cart_context["currency"] = cart.market.company.get_currency()
			cart_context["user"] = User.objects.get(pk=cart.market.user.pk)
			cart_context["market"] = EC_MarketAccess.objects.get(pk=cart.market.pk)

			return render(request, template, cart_context)
		else:
			return HttpResponse("Not Owner")
	else:
		return HttpResponse("MS and Admin Required")


def add_item_to_shopping_cart(request, cart):
	if 'username' in request.session:
		if request.method == "POST":

			shopping_cart =  EC_ShoppingCart.objects.get(pk=cart)
			quantity = request.POST.get('quantity', '')
			product = request.POST.get('product', '')
			product = MS_Products.objects.get(pk=product)

			if shopping_cart.status is "created":

				if int(quantity) > 0 and int(quantity) <= product.stock:

					total = int(quantity) * product.product.price
					check_product = EC_ShoppingCartItems.objects.filter(cart=shopping_cart.pk, product=product.pk).last()
					
					if check_product is not None:

						count = check_product.quantity + int(quantity)
						total_count = check_product.total + total
						check_product.quantity = count
						check_product.total = total_count
						check_product.save()

						return HttpResponse("saved")
					else:

						shopping_cart_items = EC_ShoppingCartItems(
								cart=EC_ShoppingCart.objects.get(pk=shopping_cart.pk),
								product=MS_Products.objects.get(pk=product.pk),
								quantity=int(quantity),
								item_price=product.product.price,
								total=total,
								saved_date=today_now
							)
						shopping_cart_items.save()

						return HttpResponse("saved")
				else:
					return HttpResponse("Quantiy must not be 0 or geater than Stock")
			else:
				return HttpResponse("Cannot Perform Action. Status: %s" % shopping_cart.status )
		else:
			return HttpResponse("Error Method")
	else:
		return HttpResponse("User Session Required")


def remove_item_to_shopping_cart(request, item):
	if 'username' in request.session:
		item = EC_ShoppingCartItems.objects.get(pk=item)
		cart = EC_ShoppingCart.objects.get(pk=item.cart.pk)
		if cart.status is "created":
			if item.cart.market.user.pk == request.session['user']:
				item.delete()
				return HttpResponse("removed")
			else:
				return HttpResponse("User Not The Owner")
		else:
			return HttpResponse("Cannot Perform Action. Status: %s" % cart.status )
	else:
		return HttpResponse("Session User Required")


def update_item_to_shopping_cart(request, item):
	if 'username' in request.session:
		if request.method == "POST":
			
			item = EC_ShoppingCartItems.objects.get(pk=item)
			quantity = request.POST.get('quantity', '')
			product = MS_Products.objects.get(pk=item.product.pk)
			total = int(quantity) * product.product.price
			cart = EC_ShoppingCart.objects.get(pk=item.cart.pk)

			if cart.status is "created":

				if int(quantity) > 0:

					if item.cart.market.user.pk == request.session['user']:
						item.quantity = quantity
						item.total = total
						item.save()
						return HttpResponse("updated")
					else:
						return HttpResponse("User Not The Owner")
				else:
					return HttpResponse("Quantiy Must Be Greater Than 0")
			else:
				return HttpResponse("Cannot Perform Action. Status: %s" % cart.status )
		else:
			return HttpResponse("Bad Request")
	else:
		return HttpResponse("Session User Required")


@csrf_exempt
def place_payment_cart(request, cart):
	
	if 'username' in request.session:
		
		if request.method == "POST":
			
			cart = get_object_or_404(EC_ShoppingCart, pk=cart)
			charges = request.POST.get('other_charges', '')
			delivery = request.POST.get('delivery', '')
			payment_mode = request.POST.get('payment_mode', '')

			if cart.status is "accepted":
			
				if cart.market.user.pk == request.session['user']:
					
					cart.status = "paid"
					cart.total_net = cart.get_cart_total() 
					cart.others_chargers = int(charges)
					cart.total_paid = cart.get_cart_total() + int(charges)
					cart.payment_mode = payment_mode
					cart.delivery = True if delivery == "true" else False
					cart.save()

					return HttpResponse("paid")
				else:
					return HttpResponse("User Not The Owner")
			else:
				return HttpResponse("Cannot Perform Action. Status: %s" % cart.status )
		else:
			return HttpResponse("Bad Request")
	else:
		return HttpResponse("Session User Required")


def finish_shopping_cart(request, cart):
	if 'username' in request.session:
		cart = get_object_or_404(EC_ShoppingCart, pk=cart)
		if cart.get_sum_items_cart() > 0:
			cart.status = "finished"
			cart.save()
			return HttpResponse("ok")
		else:
			return HttpResponse("Cart Is Empty !!!")
	else:
		return HttpResponse("User Session Required")


def load_single_cart_gen(request, cart):
	if 'username' in request.session:
		cart = get_object_or_404(EC_ShoppingCart, pk=cart)
		
		if cart.market.user.pk == request.session['user']:
			template = "ecommerce/user_cart.html"
			cart_context = {}
			cart_context.update(csrf(request))
			cart_context['market'] = EC_MarketAccess.objects.get(pk=cart.market.pk)
			cart_context['cart'] = cart
			cart_context['session_user'] = request.session['user']

			return render(request, template, cart_context)
		else:
			return HttpResponse("Not Owner")
	else:
		return HttpResponse("User Session Required")


#Company E-Commerse Settings


def load_company_ecommerse_settings(request):
	if check_all_sessions(request):
		template = "managment/mssettings/ecommerce_set.html"
		company = MS_CompanyAdministrator.objects.get(pk=request.session['ms'])
		ecommerce_set = EC_CompanySettings.objects.filter(company=company.pk).first()
		
		ecommerce_context = {}

		if ecommerce_set is not None:
			ecommerce_context["settings"] = ecommerce_set
		else:
			ecommerce_set = EC_CompanySettings(
					company=MS_CompanyAdministrator.objects.get(company=company.pk)
				) 
			ecommerce_set.save()
			ecommerce_context["settings"] = ecommerce_set

		return render(request, template, ecommerce_context)
	else:
		return HttpResponse("Session Company & Admin Required")


class UseEcommerceService(TemplateView):

	template = "managment/mssettings/e_use_ecommerce.html"

	def get(self, request):
		if check_all_sessions(request):
			ecommerce_context = {}
			ecommerce_context.update(csrf(request))
			text = "If set to <b>False</b>, users and your customers cannot be able to buy online nor access your macket "
			text +="but if set to <b>True</b>, your customers can be able to order online."
			ecommerce_set = EC_CompanySettings.objects.get(company=request.session['ms'])

			ecommerce_context["setting"] = ecommerce_set
			ecommerce_context["text"] = text

			return render_to_response(self.template, ecommerce_context)
		else:
			return HttpResponse("MS and Admin Sessions Required")

	@csrf_exempt
	def post(self, request):
		if check_all_sessions(request):
			if request.method == "POST":
				setting = request.POST.get('setting', '')
				password = request.POST.get('password', '')
				ecommerce_set = EC_CompanySettings.objects.get(company=request.session['ms'])
				if check_ms_password(request, password) is not None:
					ecommerce_set.use_ecommerce = setting
					ecommerce_set.save()
					return HttpResponse("ok")
				else:
					return HttpResponse("Wrong MS Password !!!")
			else:
				return HttpResponse("Bad Request")
		else:
			return HttpResponse("MS and Admin Sessions Required")


class UsePayPal(TemplateView):

	template = "managment/mssettings/e_paypal.html"

	def get(self, request):
		if check_all_sessions(request):
			ecommerce_context = {}
			ecommerce_context.update(csrf(request))
			text = "Set it to <b>True</b> then add your paypal email or other so that "
			text +="you may receive your poayment on paypal."

			ecommerce_set = EC_CompanySettings.objects.get(company=request.session['ms'])

			ecommerce_context["setting"] = ecommerce_set
			ecommerce_context["text"] = text

			return render_to_response(self.template, ecommerce_context)
		else:
			return HttpResponse("MS and Admin Sessions Required")

	@csrf_exempt
	def post(self, request):
		if check_all_sessions(request):
			if request.method == "POST":
				setting = request.POST.get('setting', '')
				password = request.POST.get('password', '')
				ecommerce_set = EC_CompanySettings.objects.get(company=request.session['ms'])
				if check_ms_password(request, password) is not None:
					ecommerce_set.use_paypal = setting
					ecommerce_set.save()
					return HttpResponse('ok')
				else:
					return HttpResponse("Wrong MS Password !!!")
			else:
				return HttpResponse("Bad Request")
		else:
			return HttpResponse("MS and Admin Sessions Required")

	@csrf_exempt
	def add_paypal_account(self, request):
		if check_all_sessions(request):
			if request.method == "POST":
				account = request.POST.get('account', '')
				password = request.POST.get('password', '')
				ecommerce_set = EC_CompanySettings.objects.get(company=request.session['ms'])
				if email_check(account) is not False:
					if ecommerce_set.use_paypal is True:
						ecommerce_set.paypal = account
						ecommerce_set.save()
						return HttpResponse('ok')
					else:
						return HttpResponse("Set Use E-Comerce PayPal To True !!!")
				else:
					return HttpResponse("Enter A Right Email !!!")
			else:
				return HttpResponse("Bad Request")
		else:
			return HttpResponse("MS and Admin Sessions Required")


class UseMobileMoney(TemplateView):

	template = "managment/mssettings/e_mobile.html"

	def get(self, request):
		if check_all_sessions(request):
			ecommerce_context = {}
			ecommerce_context.update(csrf(request))

			text = "If set to <b>True</b>, you will be able to receive the payment "
			text += " through mobile money. You must add numbers in MS Settings"

			ecommerce_set = EC_CompanySettings.objects.get(company=request.session['ms'])

			ecommerce_context["setting"] = ecommerce_set
			ecommerce_context["text"] = text

			return render_to_response(self.template, ecommerce_context)
		else:
			return HttpResponse("MS and Admin Sessions Required")

	def post(self, request):
		if check_all_sessions(request):
			if request.method == "POST":
				setting = request.POST.get('setting', '')
				password = request.POST.get('password', '')
				ecommerce_set = EC_CompanySettings.objects.get(company=request.session['ms'])
				if check_ms_password(request, password) is not None:
					ecommerce_set.mobile = setting
					ecommerce_set.save()
					return HttpResponse('ok')
				else:
					return HttpResponse("Wrong MS Password !!!")
			else:
				return HttpResponse("Bad Request")
		else:
			return HttpResponse("MS and Admin Sessions Required")





