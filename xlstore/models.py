# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from datetime import datetime
from time import strftime
from django.utils import timezone
from time import *
from django_countries.fields import CountryField
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
import json


#UnixTimeStamp

MALE = 'Male'
FEMALE = 'Female'
OTHER = 'Other'

GENDER_CHOICES = (
	(MALE, 'Male'),
	(FEMALE, 'Female'),
	(OTHER, 'Other'),
)


class UnixTimestampField(models.DateTimeField):
    
    def __init__(self, null=False, blank=False, **kwargs):
        super(UnixTimestampField, self).__init__(**kwargs)
        self.blank, self.isnull = blank, null
        self.null = True 

    def db_type(self, connection):
        typ=['TIMESTAMP']
        if self.isnull:
            typ += ['NULL']
        if self.auto_created:
            typ += ['default CURRENT_TIMESTAMP']
        return ' '.join(typ)

    def to_python(self, value):
        if isinstance(value, int):
            return datetime.fromtimestamp(value)
        else:
            return models.DateTimeField.to_python(self, value)

    def get_db_prep_value(self, value, connection, prepared=False):
        if value==None:
            return None
        return strftime('%Y-%m-%d %H:%M:%S',value.timetuple())

#Files storage function

def get_company_profile_img(instance, filename):
	return "company_profile/%s_%s" % (str(time()).replace('.','_'), filename)

def get_company_cover_img(instance, filename):
	return "company_cover/%s_%s" % (str(time()).replace('.','_'), filename)

def get_user_profile_img(instance, filename):
	return "user_profile/%s_%s" % (str(time()).replace('.','_'), filename)

def get_user_cover_img(instance, filename):
	return "user_cover/%s_%s" % (str(time()).replace('.','_'), filename)


#Models Managers


class GeneralQuerySet(models.QuerySet):

	def is_deleted(self):
		return self.filter(is_deleted=True)


class ProductAdminQuerySet(models.QuerySet):

	def my_products(self):
		return self.exclude(is_deleted=True)


class GeneralManager(models.Manager):

	def get_queryset(self):
		return super(GeneralManager, self).get_queryset().exclude(is_deleted=True)


class NotificationsManager(models.Manager):

	def get_queryset(self):
		return super(NotificationsManager, self).get_queryset().exclude(is_read=True)


class GeneralProductManager(models.Manager):

	def get_queryset(self):
		return super(GeneralProductManager, self).get_queryset().exclude(is_to_be_posted=False)


class ProductAdminManager(models.Manager):

	def get_queryset(self):
		return ProductAdminQuerySet(self.model, using=self._db)


#Models


class CompanyCategories(models.Model):
	name = models.CharField(max_length=250)
	image = models.ImageField(upload_to='admin/categories/')
	description = models.TextField()

	def __unicode__(self):
		return self.name

	def __str__(self):
		return self.name

	def get_sum_category_users(self):
		users = UserCategories.objects.filter(category=self.pk).count()
		return users

	def get_category_users(self):
		users = UserCategories.objects.filter(category=self.pk)
		return users

	def get_category_users_list(self):
		users = [user.user.pk for user in UserCategories.objects.filter(category=self.pk)]
		return users

	def get_sum_category_companies(self):
		companies = Company.objects.filter(category=self.pk).count()
		return companies

	def get_category_companies(self):
		companies = Company.objects.filter(category=self.pk)
		return companies


class Company(models.Model):
	name = models.CharField(max_length=250)
	name_dotted = models.CharField(max_length=250, blank=True, null=True, unique=True)
	email = models.EmailField(max_length=254, blank=False, unique=True)
	password = models.CharField(max_length=20)
	profile_image = models.ImageField(upload_to=get_company_profile_img, null = True, blank = True)
	cover_image = models.ImageField(upload_to=get_company_cover_img, null = True, blank = True)
	phone_number = models.CharField(max_length=20, null = True)
	country = CountryField(null = True)
	town = models.CharField(max_length=250, null = True)
	category = models.ForeignKey(CompanyCategories, null = True, blank = True)
	motto = models.TextField(null = True)
	description = models.TextField(null = True)
	is_authenticated = models.BooleanField(default=False)
	has_seen_tutorial = models.BooleanField(default=False)
	registration_date = models.DateTimeField(blank=True, default=datetime.now)

	def __unicode__(self):
		return self.name

	def __str__(self):
		return self.name

	def email_company(self, subject, message, from_email=None):
		send_mail(subject, from_email, [self.email])

	def get_absolute_url(self):
		return "/company/%s/" % urlquote(self.name_dotted)

	def get_full_name(self):
		full_name = '%s' % (self.name)
		return full_name.strip()

	def get_sum_products(self):
		sum_product = Products.objects.filter(company=self.pk).count()
		return sum_product

	def get_sum_categories(self):
		sum_categories = Categories.objects.filter(company=self.pk).count()
		return sum_categories

	def get_categories(self):
		categories = Categories.objects.filter(company=self.pk)
		return categories

	def get_sum_advertisments(self):
		sum_advertisment = Advertisments.objects.filter(company=self.pk).count()
		return sum_advertisment

	def get_sum_followers(self):
		sum_followers = Followers.objects.filter(company=self.pk).count()
		return sum_followers

	def get_sum_posts(self):
		sum_posts = Posts.objects.filter(company=self.pk).count()
		return sum_posts

	def get_profile_image(self):
		if self.profile_image:
			return self.profile_image
		else:
			return "default/default_company.jpg"

	def get_followers(self):
		followers = Followers.objects.filter(company=self.pk)
		return followers

	def get_sum_notification(self):
		sum_notification = CompanyNotifications.objects.filter(concern=self.pk).count()
		return sum_notification

	def get_notifications(self):
		notifications = CompanyNotifications.objects.filter(concern=self.pk).order_by('-posted_date')
		return notifications

	def get_sum_trades(self):
		sum_trades = ProductTrade.objects.filter(product__company=self.pk).count()
		return sum_trades

	def get_trades(self):
		trades = ProductTrade.objects.filter(product__company=self.pk)
		return trades

	def get_sum_replies(self):
		replies = PostReplies.objects.filter(company=self.pk).count()
		return replies

	def get_sum_comments(self):
		comments = ProductComments.objects.filter(company=self.pk).count()
		return comments

	def get_sum_interess(self):
		interess = ProductInteress.objects.filter(product__company=self.pk).count()
		return interess

	def get_ms_products(self):
		products = MS_Products.objects.filter(product__company=self.pk).count()
		return products

	def get_company_addresses(self):
		address = Address.objects.filter(company=self.pk)
		return address

	def get_company_json(self):
		return {
					"id":self.pk,
					"name": self.name,
					"name_dotted": self.name_dotted,
					"email": self.email,
					"profile_image": self.get_profile_image(),
					"cover_image": self.cover_image,
					"phone_number": self.phone_number,
					"country": self.country.name,
					"town": self.town,
					"address": [address.get_address_json() for address in self.get_company_addresses()],
					"category": self.category.name,
					"motto": self.motto,
					"description": self.description,
					"registration_date": self.registration_date,
					"url":reverse('comp_profile', kwargs={'company_name': self.name_dotted}),
					"followers": self.get_sum_followers(),
					"categories": self.get_sum_categories(),
					"posts": self.get_sum_posts(),
					"products": self.get_sum_products(),
					"advertisments": self.get_sum_advertisments()
				}

	def get_company_tag_json(self):
		return {"name":self.name, "username":self.name_dotted, "image":"http://127.0.0.1:8000/media/"+str(self.get_profile_image())}


class User(models.Model):
	full_name = models.CharField(max_length=250, null=True, blank=False)
	user_name = models.CharField(max_length=250, unique=True)
	email = models.EmailField(max_length=254, blank=False, unique=True)
	profile_image = models.ImageField(upload_to=get_user_profile_img, null = True, blank = True)
	cover_image = models.ImageField(upload_to=get_user_cover_img, null = True, blank = True)
	gender = models.CharField(choices=GENDER_CHOICES, max_length=10, default=MALE)
	country = CountryField(null = True)
	town = models.TextField(null = True)
	phone_number = models.TextField(null = True)
	password = models.CharField(max_length=100, blank=True, null=True)
	biography = models.TextField(blank=True, null=True)
	show_secret_details = models.BooleanField(default=True)
	is_authenticated = models.BooleanField(default=False)
	has_seen_tutorial = models.BooleanField(default=False)
	registration_date = models.DateTimeField(blank=True, default=datetime.now)

	def __unicode__(self):
		return self.user_name

	def email_user(self, subject, message, from_email=None):
		send_mail(subject, from_email, [self.email])

	def get_absolute_url(self):
		return "/user/%s/" % urlquote(self.user_name)

	def get_full_name(self):
		full_name = '%s' % (self.full_name)
		return full_name.strip()

	def get_sum_posts(self):
		sum_posts = Posts.objects.filter(user=self.pk).count()
		return sum_posts

	def get_sum_following(self):
		sum_following = UserFollow.objects.filter(follower_user=self.pk).count()
		return sum_following

	def get_sum_followers(self):
		sum_followers = UserFollow.objects.filter(following=self.pk).count()
		return sum_followers

	def get_sum_companies(self):
		sum_companies = Followers.objects.filter(user=self.pk).count()
		return sum_companies

	def get_companies(self):
		companies = Followers.objects.filter(user=self.pk)
		return companies

	def get_sum_interess(self):
		sum_interess = ProductInteress.objects.filter(user=self.pk).count()
		return sum_interess

	def get_followers(self):
		followers = UserFollow.objects.filter(following=self.pk)
		return followers

	def get_following(self):
		following = UserFollow.objects.filter(follower_user=self.pk)
		return following

	def get_sum_notification(self):
		notifications = UserNotifications.objects.filter(concern=self.pk).count()
		return notifications

	def get_notifications(self):
		notifications = UserNotifications.objects.filter(concern=self.pk).order_by('-posted_date')
		return notifications

	def get_sum_likes(self):
		likes = ProductMention.objects.filter(user=self.pk, mention='like').count()
		return likes

	def get_sum_dislikes(self):
		dislikes = ProductMention.objects.filter(user=self.pk, mention='dislike').count()
		return dislikes

	def get_sum_comments(self):
		comments = ProductComments.objects.filter(user=self.pk).count()
		return comments

	def get_interess(self):
		interess = ProductInteress.objects.filter(user=self.pk).order_by('-interess_date')
		return interess

	def get_sum_replies(self):
		replies = PostReplies.objects.filter(user=self.pk).count()
		return replies

	def get_sum_trades(self):
		sum_trades = ProductTrade.objects.filter(user=self.pk).count()
		return sum_trades

	def get_trades(self):
		trades = ProductTrade.objects.filter(user=self.pk)
		return trades

	def get_profile_image(self):
		if self.profile_image:
			return self.profile_image
		else:
			return "default/default_user.jpg"

	def get_company_categories(self):
		categories = UserCategories.objects.filter(user=self.pk)
		return categories

	def get_company_categories_list(self):
		categories = [category.category.pk for category in UserCategories.objects.filter(user=self.pk)]
		return categories

	def get_sum_categories(self):
		categories = UserCategories.objects.filter(user=self.pk).count()
		return categories

	def get_user_address(self):
		address = Address.objects.filter(user=self.pk).first()
		return address.get_address_json() if address is not None else None
		
	def get_user_json(self, token):
		return {
					"token": token,
					"name": self.full_name,
					"username": self.user_name,
					"email": self.email,
					"profile_image": self.get_profile_image(),
					"cover_image": self.cover_image,
					"gender": self.gender,
					"country": self.country.name,
					"town": self.town,
					"phone_number": self.phone_number,
					"address": self.get_user_address(),
					"registration_date": self.registration_date,
					"url": reverse('user_profile', kwargs={'user_name': self.user_name}),
					"posts": self.get_sum_posts(),
					"following": self.get_sum_following(),
					"followers": self.get_sum_followers(),
					"companies": self.get_sum_companies(),
					"interess": self.get_sum_interess(),
					"replies": self.get_sum_replies(),
					"comments": self.get_sum_comments(),
					"trades": self.get_sum_trades(),
					"likes": self.get_sum_likes(),
					"dislikes": self.get_sum_dislikes()
				}

	def get_user_tag_json(self):
		return {"name":self.full_name, "username":self.user_name, "image":"http://127.0.0.1:8000/media/"+str(self.get_profile_image())}


class Categories(models.Model):
	name = models.CharField(max_length=100)
	company = models.ForeignKey(Company)
	description = models.TextField(null=True, blank=True)
	created_date = models.DateTimeField(blank=True, default=datetime.now)

	def __unicode__(self):
		return self.name

	def get_sum_products(self):
		products = Products.objects.filter(category=self.pk).count()
		return products


class Followers(models.Model):
	user = models.ForeignKey(User)
	company = models.ForeignKey(Company)
	follow_date = models.DateTimeField(default=datetime.now, blank=True, null=True)

	def __unicode__(self):
		return self.user.user_name


class UserFollow(models.Model):
	following = models.ForeignKey(User, related_name="followed_user")
	follower_user = models.ForeignKey(User, related_name="follower_user")
	follow_date = models.DateTimeField(auto_created=True)

	def __unicode__(self):
		return self.pk


class UserCategories(models.Model):
	user = models.ForeignKey(User)
	category = models.ForeignKey(CompanyCategories)
	follow_date = models.DateTimeField(auto_created=True)

	def __unicode__(self):
		return self.category.name

	def __str__(self):
		return self.category.name


class Address(models.Model):
	company = models.ForeignKey(Company, null=True, blank=True)
	user = models.ForeignKey(User, null=True, blank=True)
	address = models.CharField(max_length=255)
	latitude = models.DecimalField(max_digits=20, decimal_places=10)
	longitude = models.DecimalField(max_digits=20, decimal_places=10)
	added_date = models.DateTimeField(auto_created=True)

	def __unicode__(self):
		return self.address

	def __str__(self):
		return self.address

	def get_address_json(self):
		return {"address": self.address, "latitude": self.latitude, "longitude": self.longitude}


class UserNotifications(models.Model):
	user = models.ForeignKey(User, blank=True, null=True)
	company = models.ForeignKey(Company, blank=True, null=True)
	notification_maker = models.CharField(max_length=100, default='user')
	concern = models.ForeignKey(User, related_name='notification_user')
	notification_id = models.IntegerField()
	about = models.CharField(max_length=200)
	is_read = models.BooleanField(default=False)
	posted_date = models.DateTimeField(auto_created=True)

	objects = NotificationsManager()

	def __unicode__(self):
		return self.pk


class CompanyNotifications(models.Model):
	user = models.ForeignKey(User, blank=True, null=True)
	concern = models.ForeignKey(Company)
	notification_id = models.IntegerField()
	about = models.CharField(max_length=200)
	is_read = models.BooleanField(default=False)
	posted_date = models.DateTimeField(auto_created=True)

	objects = NotificationsManager()

	def __unicode__(self):
		return self.pk


#PRODUCTS


class Products(models.Model):
	company = models.ForeignKey(Company)
	product_name = models.CharField(max_length=250)
	category = models.IntegerField(null=True, blank=True)
	image = models.ImageField(upload_to='products/%Y/%m/%d/', blank=False, null=False)
	price = models.DecimalField(max_digits=18, decimal_places=2)
	currency = models.TextField()
	product_description = models.TextField(null=True, blank=True)
	is_deleted = models.BooleanField(default=False)
	is_to_be_posted = models.BooleanField(default=True)
	posted_date = models.DateTimeField(auto_created=True, default=datetime.now)

	objects = GeneralManager()
	objects = GeneralProductManager()
	items = ProductAdminManager()

	def __unicode__(self):
		return self.product_name

	def get_category(self):
		category = Categories.objects.get(pk=self.category)
		return category.name

	def get_sum_likes(self):
		sum_likes = ProductMention.objects.filter(product=self.pk, mention='like').count()
		return sum_likes

	def get_sum_dislikes(self):
		sum_dislike = ProductMention.objects.filter(product=self.pk, mention='dislike').count()
		return sum_dislike

	def get_sum_comments(self):
		sum_comments = ProductComments.objects.filter(product=self.pk).count()
		return sum_comments

	def get_sum_interess(self):
		sum_interess = ProductInteress.objects.filter(product=self.pk).count()
		return sum_interess

	def get_interess(self):
		interests = [ interess.user.pk for interess in ProductInteress.objects.filter(product=self.pk)  ]
		return interests

	def get_absolute_url(self):
		return None

	def check_mention_like(self):
		mentions = [mention.user.pk for mention in ProductMention.objects.filter(product=self.pk, mention="like")]
		return mentions

	def check_mention_dislike(self):
		mentions = [mention.user.pk for mention in ProductMention.objects.filter(product=self.pk, mention="dislike")]
		return mentions

	def check_managment_product(self):
		msp = MS_Products.objects.get(product=self.pk)
		return msp

	def get_more_image(self):
		more_images = ProductPictures.objects.filter(product=self.pk)
		return more_images

	def get_advertisment(self):
		advertisment = Advertisments.objects.filter(product=self.pk)[:1]
		return advertisment

	def get_product_json(self):
		category = Categories.objects.get(pk=self.category)
		company = Company.objects.get(pk=self.company.pk)
		return {
					"id": self.pk,
					"company":self.company.get_company_json(),
					"product_name":self.product_name,
					"group":{"id":company.category.pk, "name":company.category.name},
					"category": {"name":category.name, "id":category.pk},
					"image":self.image,
					"price":self.price,
					"currency":self.currency,
					"product_description":self.product_description,
					"posted_date":self.posted_date,
					"url": reverse('single_product', kwargs={'company_name': self.company.name_dotted, 'product_id': self.pk}),
					"likes":self.get_sum_likes(),
					"dislikes":self.get_sum_dislikes(),
					"comments":self.get_sum_comments(),
					"interess":self.get_sum_interess(),
					"album":[img.get_image_json() for img in self.get_more_image()],
					"advertisment": [adverst.get_adverst_json() for adverst in self.get_advertisment()]
				}

	def get_product_tag_json(self):
		return {"name":self.product_name, "username":str(self.pk), "image":"http://127.0.0.1:8000/media/"+str(self.image), "is_product":True, "company": self.company.name}


class ProductPictures(models.Model):
	product = models.ForeignKey(Products)
	image = models.ImageField(upload_to='products/%Y/%m/%d/', blank=False, null=False)
	uploaded_date = models.DateTimeField(auto_created=True, default=datetime.now)

	def __unicode__(self):
		return self.product

	def get_image_json(self):
		return{"source": self.image}


class Advertisments(models.Model):
	company = models.ForeignKey(Company)
	product = models.ForeignKey(Products)
	video = models.FileField(upload_to='advertisments/%Y/%m/%d/', blank=False, null=False)
	advertisment_text = models.TextField()
	posted_date = models.DateTimeField(auto_created=True, default=datetime.now)

	def __unicode__(self):
		return self.product

	def get_adverst_json(self):
		return {"source": self.video, "text":self.advertisment_text, "posted_date":self.posted_date}


class ProductComments(models.Model):
	product = models.ForeignKey(Products)
	company = models.ForeignKey(Company, blank=True, null=True)
	user = models.ForeignKey(User, blank=True, null=True)
	commenter = models.CharField(max_length=200)
	comment = models.TextField()
	comment_date = models.DateTimeField(auto_created=True, default=datetime.now)

	def __unicode__(self):
		return self.product

	def get_comment_json(self):
		if self.company:
			company = Company.objects.get(pk=self.company.pk) 
			return {
				"id":self.pk,
				"is_company":True,
				"company":self.company.get_company_json(),
				"commenter":self.commenter,
				"comment":self.comment,
				"comment_date":self.comment_date
			}
		else:
			return {
				"id":self.pk,
				"is_user":True,
				"user":self.user.get_user_json(self.user.pk),
				"commenter":self.commenter,
				"comment":self.comment,
				"comment_date":self.comment_date
			}


class ProductMention(models.Model):
	product = models.ForeignKey(Products)
	user = models.ForeignKey(User)
	mention = models.TextField()
	mention_date = models.DateTimeField(auto_created=True, default=datetime.now)

	def __unicode__(self):
		return self.product


class ProductInteress(models.Model):
	product = models.ForeignKey(Products)
	user = models.ForeignKey(User)
	interess_date = models.DateTimeField(auto_created=True, default=datetime.now)

	def __unicode__(self):

		return self.product


#POSTS


class Posts(models.Model):
	user = models.ForeignKey(User, blank=True, null=True)
	company = models.ForeignKey(Company, blank=True, null=True)
	poster_type = models.CharField(max_length=30, default='user')
	post_text = models.TextField()
	post_file = models.FileField(upload_to='posts/%Y/%m/%d/', blank=True, null=True)
	file_type = models.CharField(max_length=200, null=True, blank=True)
	is_deleted = models.BooleanField(default=False)
	posted_date = models.DateTimeField(auto_created=True, default=datetime.now)

	objects = GeneralManager()

	def __unicode__(self):
		return self.user

	def get_sum_likes(self):
		sum_likes = PostMention.objects.filter(post=self.pk, mention='like').count()
		return sum_likes

	def get_sum_dislikes(self):
		sum_dislike = PostMention.objects.filter(post=self.pk, mention='dislike').count()
		return sum_dislike

	def get_sum_replies(self):
		sum_replies = PostReplies.objects.filter(post=self.pk).count()
		return sum_replies

	def check_mention_like(self, request):
		mentions = [mention.user.pk for mention in PostMention.objects.filter(post=self.pk, mention="like")]
		return mentions

	def check_mention_dislike(self, request):
		mentions = [mention.user.pk for mention in PostMention.objects.filter(post=self.pk, mention="dislike")]
		return mentions

	def get_post_json(self):
		if self.user:
			return {
						"id": self.pk,
						"user": self.user.get_user_json(self.user.pk),
						"poster_type": self.poster_type,
						"is_user": True,
						"text": self.post_text,
						"post_file": self.post_file,
						"file_type": self.file_type,
						"posted_date": self.posted_date,
						"likes": self.get_sum_likes(),
						"dislikes": self.get_sum_dislikes(),
						"replies": self.get_sum_replies()
					}
		elif self.company:
			return {
						"id": self.pk,
						"company": self.company.get_company_json(),
						"poster_type": self.poster_type,
						"is_company": True,
						"text": self.post_text,
						"post_file": self.post_file,
						"file_type": self.file_type,
						"posted_date": self.posted_date,
						"likes": self.get_sum_likes(),
						"dislikes": self.get_sum_dislikes(),
						"replies": self.get_sum_replies()
					}



		

class PostReplies(models.Model):
	post = models.ForeignKey(Posts)
	user = models.ForeignKey(User, blank=True, null=True)
	company = models.ForeignKey(Company, blank=True, null=True)
	reply_type = models.TextField(default='user')
	reply_image = models.ImageField(upload_to='posts_reply/%Y/%m/%d/', blank=True, null=True)
	reply_text = models.TextField()
	reply_date = models.DateTimeField(auto_created=True, default=datetime.now)

	def __unicode__(self):
		return self.post

	def get_reply_json(self):
		if self.company:
			return {
						"id": self.pk,
						"is_company": True,
						"company": self.company.get_company_json(),
						"type": self.reply_type,
						"image": self.reply_image,
						"reply": self.reply_text,
						"date": self.reply_date
					}
		else:
			return {
						"id": self.pk,
						"is_user": True,
						"user": self.user.get_user_json(self.user.pk),
						"type": self.reply_type,
						"image": self.reply_image,
						"reply": self.reply_text,
						"date": self.reply_date
					}


class PostMention(models.Model):
	post = models.ForeignKey(Posts)
	user = models.ForeignKey(User)
	mention = models.TextField()
	mention_date = models.DateTimeField(auto_created=True, default=datetime.now)

	def __unicode__(self):
		return self.post


#Trade messages


class ProductTrade(models.Model):
	user = models.ForeignKey(User)
	product = models.ForeignKey(Products)
	status = models.CharField(max_length=50)
	started_date = models.DateTimeField(auto_created=True)
	end_date = models.DateTimeField(auto_created=True, null=True, blank=True)

	def __unicode__(self):
		return self.pk

	def __str__(self):
		return self.pk

	def get_sum_trade_messages(self):
		messages = ProductTradeMessages.objects.filter(trade=self.pk, is_read=False).count()
		return messages

	def check_trade_agreement(self):
		trade_agreement = TradeAgreements.objects.get(trade=self.pk)
		return trade_agreement


class ProductTradeMessages(models.Model):
	trade = models.ForeignKey(ProductTrade)
	sender = models.CharField(max_length=50)
	receiver = models.CharField(max_length=50)
	text_message = models.TextField(blank=True, null=True)
	image_message = models.ImageField(upload_to='trades/%Y/%m/%d/', null=True, blank=True)
	address = models.TextField(blank=True, null=True)
	longitude = models.CharField(max_length=18, blank=True, null=True)
	latitude = models.CharField(max_length=18, blank=True, null=True)
	is_read = models.BooleanField(default=False)
	is_deleted_by = models.CharField(default='none', max_length=40)
	date_time = models.DateTimeField(auto_created=True)

	def __unicode__(self):
		return self.trade


class TradeAgreements(models.Model):
	trade = models.OneToOneField(ProductTrade)
	price = models.DecimalField(max_digits=18, decimal_places=2)
	quantity = models.IntegerField()
	status = models.CharField(max_length=100)
	is_finished = models.BooleanField(default=False)
	agreement_date = models.DateField(auto_created=True)
	finished_date = models.DateField(auto_created=True, null=True, blank=True)

	def __unicode__(self):
		return self.trade


#FOR MANAGMENT SYSTEM INTEGRATED


class MS_Products(models.Model):
	product = models.OneToOneField(Products)
	price = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
	stock = models.IntegerField()
	product_code = models.CharField(max_length=255)
	place_number = models.CharField(max_length=255, null=True, blank=True)
	last_entry_stock = models.DateTimeField(auto_created=True)

	def __unicode__(self):
		return self.product

	def check_managment_product(self):
		msp = Products.items.filter(pk=self.product)
		return msp
