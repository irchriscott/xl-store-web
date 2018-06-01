# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, render_to_response, get_object_or_404
from django.core import serializers
from django.http import HttpResponse
from xlstore.models import * 
from xlstore.views import *
from django.utils import timezone
from xlstore.backends import UserAuth
from django.views.decorators.csrf import csrf_exempt
import datetime
import json

# Create your views here.


#FOR USER


def check_user_username(request, username):
	try:
		user_username = User.objects.get(user_name=username)
		return username
	except User.DoesNotExist:
		return None


def check_user_email(request, email):
	try:
		user_email = User.objects.get(email=email)
		return email
	except User.DoesNotExist:
		return None


def check_company_email(request, email):
	try:
		company_email = Company.objects.get(email=email)
		return email
	except Company.DoesNotExist:
		return None

def return_response(params):
	response = HttpResponse(params, content_type="application/json")
	response['Access-Control-Allow-Origin'] = "*"
	response['Access-Control-Allow-Headers'] = "origin, x-requested-with, content-type"
	response['Access-Control-Allow-Methods'] = "PUT, GET, POST, DELETE, OPTIONS"
	return response


def api_get_countries(request):
	response = render(request, "countries.json", {}, content_type="application/json")

	response['Access-Control-Allow-Origin'] = "*"
	response['Access-Control-Allow-Headers'] = "origin, x-requested-with, content-type"
	response['Access-Control-Allow-Methods'] = "PUT, GET, POST, DELETE, OPTIONS"
	
	return response


@csrf_exempt
def api_user_login(request):
	if request.method == "POST":
		login_data = json.loads(request.body)
		auth = UserAuth()
		email = login_data["email"]
		password = login_data["password"]

		user = auth.authenticate_user(email=email, password=password)

		if user is not None:
			username = user.user_name

			request.session['user'] = user.pk
			request.session['username'] = user.user_name

			return return_response(json.dumps(user.get_user_json(request.session['user']), default=str))
		else:

			return return_response("401")
	else:
		error = {
			"Error":"Expecting POST REQUEST METHOD",
			"Fields": "email, password",
			"Format":"JSON"
		}
		return return_response(json.dumps(error, indent=4))


@csrf_exempt
def api_user_logout(request):
	if request.method == "POST":
		try:
			del request.session['user']
			del request.session['username']

			return return_response("Logged Out !!!")

		except KeyError:

			return return_response("Error Logout !!!")
	else:
		response = HttpResponse("Error Session !!!", content_type="application/json")
		response['Access-Control-Allow-Origin'] = "*"
		return response


@csrf_exempt
def api_user_register(request):
	if request.method == "POST":
		user_data = json.loads(request.body)
		user_name = user_data["user_name"]
		email = user_data["email"]
		password = user_data["password"]
		conf_password = user_data["conf_password"]

		if user_name != "" and user_data["full_name"] != "" and email != "" and password != "" and conf_password != "" and user_data["town"] != "":

			if check_user_username(request, user_name) is not None:
				return return_response("Username Is Already Taken !!!")

			elif check_user_email(request, email) is not None or check_company_email(request, email) is not None:
				return return_response("Email Is Already Taken !!!")

			else:

				if password == conf_password:
					
					new_user = User(
							full_name=user_data["full_name"],
							user_name=user_name,
							email=email,
							gender=user_data["gender"],
							country=user_data["country"],
							town=user_data["town"],
							password=password
						)
					new_user.save()

					return return_response("ok")
				else:
					return return_response("Passwords Did Not Match !!!")
		else:
			return return_response("Fill All The Fields, Please !!!")
	else:
		error = {
			"Error":"Expecting POST REQUEST METHOD",
			"Fields": "User Fields",
			"Format":"JSON"
		}
		return return_response(json.dumps(error, indent=4))


def api_get_user_data(request, token):
	user = User.objects.get(pk=token)
	return return_response(json.dumps(user.get_user_json(user.pk), default=str))


def api_get_user_followers(request, token):
	user = User.objects.get(pk=token)
	followers = [follower.following.get_user_json(follower.following.pk) for follower in user.get_followers()]
	return return_response(json.dumps(followers, indent=4, default=str))


def api_get_user_followings(request, token):
	user = User.objects.get(pk=token)
	followings = [following.follower_user.get_user_json(following.follower_user.pk) for following in user.get_following()]
	return return_response(json.dumps(followings, indent=4, default=str))


def api_get_user_companies(request, token):
	user = User.objects.get(pk=token)
	companies = [company.company.get_company_json() for company in user.get_companies()]
	return return_response(json.dumps(companies, indent=4, default=str))


def api_get_user_interess(request, token):
	user = User.objects.get(pk=token)
	interesses = [interess.product.get_product_json() for interess in user.get_interess()]
	return return_response(json.dumps(interesses, indent=4, default=str))

#FOR POSTS

def api_get_user_posts(request, token):
	user = User.objects.get(pk=token)
	posts = Posts.objects.filter(poster=user.pk).order_by('-posted_date')

	posts = [post.get_post_json() for post in posts]
	posts = json.dumps(posts, indent=4, sort_keys=True, default=str)

	return return_response(posts)


@csrf_exempt
def api_mention_post(request, post):
	if request.method == "POST":
		mention_data = json.loads(request.body)

		post_obj = Posts.objects.get(pk=post)
		mention = mention_data["mention"]
		user = mention_data["user"]

		check_mention = PostMention.objects.filter(post=post, mentioner=user)

		if check_mention:
			for this_mention in check_mention:
				mention_post = PostMention.objects.get(pk=this_mention.pk)
				mention_post.mention = mention
				mention_post.mention_date = timezone.now()
				mention_post.save()
			
			return return_response("Post %sd !!!" % mention)

		else:
			mention_post = PostMention(
					post=Posts.objects.get(pk=post),
					mentioner=User.objects.get(pk=user),
					mention=mention,
					mention_date=timezone.now()
				)
			mention_post.save()
			if post_obj.poster_type == 'user':
				saveUserNotificationFromUser(
						request,
						User.objects.get(pk=user),
						User.objects.get(pk=post_obj.poster.pk),
						post_obj.pk,
						mention
					)
			elif post_obj.poster_type == 'company':
				saveCompanyNotificationFromUser(
						request,
						User.objects.get(pk=user),
						Company.objects.get(pk=post_obj.company.pk),
						post_obj.pk,
						mention
					)
		return return_response("Post %sd !!!" % mention)


def api_get_post_replies(request, post):
	replies = PostReplies.objects.filter(post=post).order_by('-reply_date')

	replies = [reply.get_reply_json() for reply in replies]
	replies = json.dumps(replies, indent=4, sort_keys=True, default=str)

	return return_response(replies)


@csrf_exempt
def api_add_reply(request, post):
	if request.method == "POST":

		reply_data = json.loads(request.body)
		post_obj = Posts.objects.get(pk=post)
		user = reply_data["user"]
		reply = reply_data["reply"]

		reply_obj = PostReplies(
			post=Posts.objects.get(pk=post),
			replyer_user=User.objects.get(pk=user),
			reply_type='user',
			reply_text=reply,
			reply_date=timezone.now()
			)
		reply_obj.save()

		print reply_data

		if post_obj.poster_type == 'user':

			saveUserNotificationFromUser(
				request,
				User.objects.get(pk=user),
				User.objects.get(pk=post_obj.poster.pk),
				post_obj.pk,
				"reply"
			)
			return return_response("Reply Added !!!")

		elif post_obj.poster_type == 'company':
			saveCompanyNotificationFromUser(
				request,
				User.objects.get(pk=user),
				Company.objects.get(pk=post_obj.company.pk),
				post_obj.pk,
				"reply"
			)
			return return_response("Reply Added !!!")
	else:
		error = {
			"Error":"Expecting POST REQUEST METHOD",
			"Fields": "Reply Fields",
			"Format":"JSON"
		}
		return return_response(json.dumps(error, indent=4))


@csrf_exempt
def api_edit_reply(request, reply):
	if request.method == "POST":
		reply_data = json.loads(request.body)
		user = reply_data["user"]
		reply_text = reply_data["reply"]

		reply_obj = PostReplies.objects.get(pk=reply)

		if reply_obj.replyer_user.pk == int(user):

			reply_obj.reply_text = reply_text
			reply_obj.save()

			return return_response("Reply Edited !!!")

		else:
			return return_response("You are not the owner !!!")
	else:
		error = {
			"Error":"Expecting POST REQUEST METHOD",
			"Fields": "reply(text), user",
			"Format":"JSON"
		}
		return return_response(json.dumps(error, indent=4))

@csrf_exempt
def api_delete_reply(request, reply):
	if request.method == "POST":
		reply_data = json.loads(request.body)
		user = reply_data["user"]

		reply_obj = PostReplies.objects.get(pk=reply)

		if reply_obj.replyer_user.pk == int(user):

			reply_obj.delete()

			return return_response("Reply Deleted !!!")
		else:
			return return_response("You are not the owner !!!")
	else:
		error = {
			"Error":"Expecting POST REQUEST METHOD",
			"Fields": "user, reply(reply_id)",
			"Format":"JSON"
		}
		return return_response(json.dumps(error, indent=4))

#FOR PRODUCTS

def api_get_company_data(request, company):
	company = Company.objects.get(pk=company)
	return return_response(json.dumps(company.get_company_json(), default=str))


def api_get_company_posts(request, company):
	posts = Posts.objects.filter(company=company).order_by('-posted_date')
	posts = [post.get_post_json() for post in posts]
	posts = json.dumps(posts, indent=4, sort_keys=True, default=str)

	return return_response(posts)


def api_get_all_products(request):
	products = [product.get_product_json() for product in Products.objects.all().order_by('-posted_date')]
	products = json.dumps(products, indent=4, sort_keys=True, default=str)
	return return_response(products)


def api_get_company_products(request, company):
	company = get_object_or_404(Company, pk=company)
	if company:
		products = [product.get_product_json() for product in Products.objects.filter(company=company).order_by('-posted_date')]
		products = json.dumps(products, indent=4, sort_keys=True, default=str)
		return return_response(products)
	else:
		return return_response("404")


def api_get_single_product(request, product):
	product = get_object_or_404(Products, pk=product)
	if product:
		product = json.dumps(product.get_product_json(),  default=str)
		return return_response(product)
	else:
		return return_response("404")


def api_get_product_comments(request, product):
	comments = [comment.get_comment_json() for comment in ProductComments.objects.filter(product=product).order_by('comment_date')]
	comments = json.dumps(comments, indent=4, sort_keys=True, default=str)
	return return_response(comments)


@csrf_exempt
def api_add_comment(request, product):
	if request.method == "POST":
		comment_data = json.loads(request.body)
		
		comment = comment_data["comment"]
		user = comment_data["user"]
		product = comment_data["product"]

		product_obj = Products.objects.get(pk=product)

		comment_obj = ProductComments(
				product = product_obj,
				commenter_user = User.objects.get(pk=user),
				commenter = "user",
				comment = comment,
				comment_date = timezone.now()
			)
		comment_obj.save()

		saveCompanyNotificationFromUser(
				request,
				User.objects.get(pk=user),
				Company.objects.get(pk=product_obj.company.pk),
				product_obj.pk,
				'comment'
			)

		return return_response("Comment Added !!!")
	else:
		error = {
			"Error":"Expecting POST REQUEST METHOD",
			"Fields": "Comment Fields",
			"Format":"JSON"
		}
		return return_response(json.dumps(error, indent=4))


@csrf_exempt
def api_edit_comment(request, comment):
	if request.method == "POST":
		comment_data = json.loads(request.body)

		user = comment_data["user"]
		comment_text = comment_data["comment"]

		comment_obj = ProductComments.objects.get(pk=comment)

		if comment_obj.commenter_user.pk == int(user):

			comment_obj.comment = comment_text
			comment_obj.save()

			return return_response("Comment Edited !!!")
		else:
			return return_response("You Are Not Owner !!!")
	else:
		error = {
			"Error":"Expecting POST REQUEST METHOD",
			"Fields": "user, comment(text)",
			"Format":"JSON"
		}
		return return_response(json.dumps(error, indent=4))


@csrf_exempt
def api_delete_comment(request, comment):
	if request.method == "POST":
		comment_data = json.loads(request.body)

		user = comment_data["user"]
		comment = comment_data["comment"]

		comment_obj = ProductComments.objects.get(pk=comment)

		if comment_obj.commenter_user.pk == int(user):

			comment_obj.delete()

			return return_response("Comment Deleted !!!")

		else:
			return return_response("You Are Not Owner !!!")
	else:
		error = {
			"Error":"Expecting POST REQUEST METHOD",
			"Fields": "user, comment(id)",
			"Format":"JSON"
		}
		return return_response(json.dumps(error, indent=4))


@csrf_exempt
def api_mention_product(request, product):
	if request.method == "POST":
		mention_data = json.loads(request.body)
		
		user = mention_data["user"]
		product = mention_data["product"]
		mention = mention_data["mention"]

		product_obj = Products.objects.get(pk=product)

		check_mention = ProductMention.objects.filter(mentioner=user, product=product)

		if check_mention :

			for this_mention in check_mention:
				mention_product = ProductMention.objects.get(pk=this_mention.pk)
				mention_product.mention = mention
				mention_product.mention_date = timezone.now()
				mention_product.save()

			return return_response("Product %sd !!!" % mention)
		else:

			mention_product = ProductMention(
					product=Products.objects.get(pk=product),
					mentioner=User.objects.get(pk=user),
					mention=mention,
					mention_date=timezone.now()
				)
			mention_product.save()
			saveCompanyNotificationFromUser(
					request,
					User.objects.get(pk=user),
					Company.objects.get(pk=product_obj.company.pk),
					product_obj.pk,
					'%s_product' % mention
				)

			return return_response("Product %sd !!!" % mention)
	else:
		error = {
			"Error":"Expecting POST REQUEST METHOD",
			"Fields": "user, product, mention",
			"Format":"JSON"
		}
		return return_response(json.dumps(error, indent=4))


@csrf_exempt
def api_interess_product(request, product):
	if request.method == "POST":
		interess_data = json.loads(request.body)
		
		user = interess_data["user"]
		product = interess_data["product"]

		check_interess = ProductInteress.objects.filter(interesser=user, product=product)
		product_obj = Products.objects.get(pk=product)

		if check_interess :

			return return_response("Already Interessed !!!")
		else:

			interess = ProductInteress(
					interesser=User.objects.get(pk=user),
					product=Products.objects.get(pk=product),
					interess_date=timezone.now()
				)
			interess.save()
			saveCompanyNotificationFromUser(
					request,
					User.objects.get(pk=user),
					Company.objects.get(pk=product_obj.company.pk),
					product_obj.pk,
					'interess'
				)
			
			return return_response("Product Interessed !!!")
	else:
		error = {
			"Error":"Expecting POST REQUEST METHOD",
			"Fields": "user, product",
			"Format":"JSON"
		}
		return return_response(json.dumps(error, indent=4))

