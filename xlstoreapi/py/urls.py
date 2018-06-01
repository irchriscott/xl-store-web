from django.conf.urls import url, include
from xlstoreapi import views

urlpatterns = [	
		
	url(r'^countries/$', views.api_get_countries, name='api_countries'),

	#USER API URLs

	url(r'^signup/$', views.api_user_register, name='api_register'),
	url(r'^login/$', views.api_user_login, name='api_auth'),
	url(r'^logout/$', views.api_user_logout, name='api_logout'),
	url(r'^user/(?P<token>\d+)/$', views.api_get_user_data, name='api_user_data'),
	url(r'^user/(?P<token>\d+)/posts/', views.api_get_user_posts, name='api_user_posts'),
	url(r'^user/(?P<token>\d+)/followers/', views.api_get_user_followers, name='api_user_followers'),
	url(r'^user/(?P<token>\d+)/following/', views.api_get_user_followings, name='api_user_followings'),
	url(r'^user/(?P<token>\d+)/companies/', views.api_get_user_companies, name='api_user_companies'),
	url(r'^user/(?P<token>\d+)/interess/', views.api_get_user_interess, name='api_user_interess'),

	#POSTS API URLs

	url(r'^posts/replies/(?P<post>\d+)/$', views.api_get_post_replies, name='api_post_replies'),
	url(r'^posts/replies/(?P<post>\d+)/add/$', views.api_add_reply, name='api_add_reply'),
	url(r'^posts/replies/(?P<reply>\d+)/edit/$', views.api_edit_reply, name='api_edit_reply'),
	url(r'^posts/replies/(?P<reply>\d+)/delete/$', views.api_delete_reply, name='api_delete_reply'),
	url(r'^posts/mention/(?P<post>\d+)/$', views.api_mention_post, name='api_mention_post'),

	#COMPANY API URLs

	url(r'^company/(?P<company>\d+)/$', views.api_get_company_data, name='api_company_data'),
	url(r'^company/(?P<company>\d+)/products/$', views.api_get_company_products, name='api_products_company'),
	url(r'^company/(?P<company>\d+)/posts/$', views.api_get_company_posts, name='api_posts_company'),

	#PRODUCTS API URLs

	url(r'^products/$', views.api_get_all_products, name='api_products_all'),
	url(r'^products/all/$', views.api_get_all_products, name='api_products_all'),
	url(r'^products/product/(?P<product>\d+)/$', views.api_get_single_product, name='api_single_product'),
	url(r'^products/comments/(?P<product>\d+)/$', views.api_get_product_comments, name='api_product_comments'),
	url(r'^products/comments/(?P<product>\d+)/add/$', views.api_add_comment, name='api_add_comment'),
	url(r'^products/comments/(?P<comment>\d+)/edit/$', views.api_edit_comment, name='api_edit_comment'),
	url(r'^products/comments/(?P<comment>\d+)/delete/$', views.api_delete_comment, name='api_delete_comment'),
	url(r'^products/mention/(?P<product>\d+)/$', views.api_mention_product, name='api_mention_product'),
	url(r'^products/interess/(?P<product>\d+)/$', views.api_interess_product, name='api_interess_product'),
	
]