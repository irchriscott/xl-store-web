from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from xlstore import views
from xlstore.company import CompanyRegister
from xlstore.user import UserRegister
from xlstore.post import PostController
from xlstore.post_reply import PostReplyController
from xlstore.product import ProductController
from xlstore.product_comment import ProductCommentController
from xlstore.category import ProductCategoryController
from xlstore.trade import TradeController
from xlstore.user import UserController
from xlstore.company import CompanyController
from xlstore.advertisment import AdvertismentController
import urllib


post = PostController()
reply = PostReplyController()
product = ProductController()
comment = ProductCommentController()
category = ProductCategoryController()
trade = TradeController()
user = UserController()
company = CompanyController()
advert = AdvertismentController()


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^managment/', include('xlstore_managment.urls')),
    url(r'^ecommerce/', include('xlstore_ecommerce.urls')),
    #url(r'^api/', include('xlstoreapi.urls')),
    url(r'^home/$', product.get_home_page, name='home'),
    url(r'^$', product.get_home_page, name='home_simple'),
    url(r'^products/$', product.get_products_page, name='products'),
    url(r'^posts/$', post.get_posts_page, name='posts'),
    url(r'^advertisments/$', advert.get_advertisments_page, name='advertisments'),
    url(r'^search/$', views.search_products_comp_users, name='search'),
    url(r'^address/add/new/$', user.add_address, name='add_address'),
    url(r'^load/map/(?P<source>[^/]+)/(?P<any_id>\d+)/load/', views.load_geo_map, name='load_geo_map'),
    
    #User Login, Register, Auth and logout

    url(r'^user/signup/$', UserRegister.as_view(), name='regist_user'),
    url(r'^user/login/$', user.get_user_login_page, name='login_user'),
    url(r'^user/logout/$', user.get_user_logout_page, name='logout_user'),
    url(r'^user/invalid/$', user.get_user_invalid_page, name='invalid_user'),
    url(r'^user/auth/$', user.get_user_auth_page, name='auth_user'),
    url(r'^user/company/categories/$', user.load_company_categories_users, name='user_company_categories'),
    url(r'^user/company/categories/(?P<category>\d+)/$', user.load_company_category_users, name='user_company_category'),
    url(r'^user/company/bills_carts/$', user.get_user_bills_and_carts, name='user_company_bills_carts_all'),
    url(r'^user/company/bills_carts/(?P<company>\d+)/$', user.get_user_bills_and_carts_company, name='user_company_bills_carts_company'),

    #View User Profile and Other

    url(r'^user/(?P<user_name>[^/]+)/$', user.get_user_profile, name='user_profile'),
    url(r'^user/(?P<user_name>[^/]+)/posts/$', user.get_user_profile, name='user_posts'),
    url(r'^user/(?P<user_name>[^/]+)/following/$', user.get_user_following_page, name='user_following'),
    url(r'^user/(?P<user_name>[^/]+)/followers/$', user.get_user_followers_page, name='user_followers'),
    url(r'^user/(?P<user_name>[^/]+)/companies/$', user.get_user_companies_page, name='user_companies'),
    url(r'^user/(?P<user_name>[^/]+)/interess/$', user.get_user_interess_page, name='user_interess'),
    
    url(r'^user/update/user_cover_image/$', user.update_user_cover_image, name='user_cover_edit'),
 	url(r'^user/update/user_profile_image/$', user.update_user_profile_image, name='user_profile_image_edit'),
 	url(r'^user/update/user_profile/$', user.update_user_profile, name='user_profile_edit'),
 	
    url(r'^user/add/post/$', post.add_post, name='user_save_post'),
    url(r'^user/save/post/$', post.save_post, name='user_add_post'),
 	url(r'^user/posts/(?P<post_id>\d+)/$', post.get_single_post_ajax, name='single_post_ajax'),
 	url(r'^user/user/follow/$', user.user_follow_user, name='user_follow_user'),
 	
    url(r'^user/posts/(?P<post_id>\d+)/edit/$', post.get_edit_post, name='user_edit_post'),
 	url(r'^user/save/(?P<post_id>\d+)/edit/$', post.save_edit_post, name='user_edit_save_post'),
 	url(r'^user/posts/article/(?P<post_id>\d+)/delete/$', post.delete_post, name='user_delete_post'),
 	
    url(r'^user/products/like_dislike/$', product.user_like_dislike_product, name='user_like_dislike_product'),
 	url(r'^user/posts/like_dislike/$', post.user_like_dislike_post, name='user_like_dislike_post'),
 	
    url(r'^user/posts/reply/(?P<post_id>\d+)/$', reply.get_post_reply, name='user_post_reply'),
 	url(r'^user/save/reply/(?P<post_id>\d+)/$', reply.save_post_reply, name='user_save_post_reply'),
 	
    url(r'^user/posts/(?P<post_id>\d+)/replies/$', reply.load_post_replies, name='user_load_post_replies'),
 	url(r'^user/posts/replies/(?P<reply_id>\d+)/delete/$', reply.delete_post_reply, name='user_delete_post_reply'),
 	url(r'^user/posts/replies/(?P<reply_id>\d+)/edit/$', reply.edit_post_reply, name='user_edit_post_reply'),
 	url(r'^user/posts/replies/(?P<reply_id>\d+)/edit_page/$', reply.get_edit_post_reply, name='user_edit_page_reply'),

    #Company Login, Register, Auth and logout

    url(r'^company/signup/$', CompanyRegister.as_view(), name='regist_comp'),
    url(r'^company/login/$', company.get_comp_login_page, name='login_comp'),
    url(r'^company/logout/$', company.get_comp_logout_page, name='logout_comp'),
    url(r'^company/invalid/$', company.get_comp_invalid_page, name='invalid_comp'),
    url(r'^company/auth/$', company.get_comp_auth_page, name='auth_comp'),

    #View Company Profile

 	url(r'^company/(?P<company_name>[^/]+)/$', company.get_comp_profile, name='comp_profile'),
 	url(r'^company/(?P<company_name>[^/]+)/products/$', company.get_comp_profile, name='comp_profile_2'),
 	url(r'^company/(?P<company_name>[^/]+)/posts/$', company.get_comp_posts, name='comp_posts'),
 	url(r'^company/(?P<company_name>[^/]+)/profile/$', company.get_comp_about, name='comp_about'),
 	url(r'^company/(?P<company_name>[^/]+)/categories/$', company.get_comp_categories, name='comp_categories'),
 	url(r'^company/(?P<company_name>[^/]+)/followers/$', company.get_comp_followers, name='comp_followers'),
 	url(r'^company/(?P<company_name>[^/]+)/advertisments/$', company.get_comp_advertisments, name='comp_advertisments'),
 	
    url(r'^company/update/company_profile_image/$', company.update_comp_profile_image, name='comp_profile_image_edit'),
 	url(r'^company/update/company_cover_image/$', company.update_comp_cover_image, name='comp_cover_edit'),
 	url(r'^company/update/company_profile/$', company.update_company_profile, name='comp_profile_edit'),
    url(r'^company/add/category/$', category.get_category_template, name='comp_add_category'),
 	url(r'^company/save/category/$', category.save_category, name='comp_save_category'),
    url(r'^company/add/product/$', product.add_product, name='comp_add_product'),
 	url(r'^company/save/product/$', product.save_product, name='comp_save_product'),
 	
    url(r'^company/(?P<company_name>[^/]+)/products/(?P<product_id>\d+)/$', product.get_single_product, name='single_product'),
 	url(r'^company/products/(?P<product_id>\d+)/$', product.get_single_product_ajax, name='single_product_ajax'),
    url(r'^company/products/(?P<product_id>\d+)/advertisment/$', product.get_product_advertisment, name='get_product_advertisment'),
    
    url(r'^edit/products/(?P<product_id>\d+)/template/$', product.get_edit_product, name='get_edit_single_product'),
 	url(r'^edit/products/(?P<product_id>\d+)/$', product.edit_product, name='edit_single_product'),
    
    url(r'^upload/products/(?P<product_id>\d+)/template/$', product.get_upload_more_images, name='get_upload_product_images'),
 	url(r'^upload/products/(?P<product_id>\d+)/$', product.upload_more_images, name='upload_product_images'),

 	url(r'^company/(?P<company_name>[^/]+)/categories/(?P<category_id>\d+)/$', category.get_single_category, name='single_category'),
    url(r'^edit/categories/(?P<category_id>\d+)/$', category.edit_category, name='edit_single_category'),
 	url(r'^edit/categories/(?P<category_id>\d+)/template/$', category.get_edit_category_template, name='get_edit_single_category'),
    
    url(r'^save/advertisment/(?P<product_id>\d+)/template/$', product.get_advertise_product, name='get_advertise_product'),
 	url(r'^save/advertisment/(?P<product_id>\d+)/$', product.advertise_product, name='advertise_product'),
 	
    url(r'^company/user/follow/$', company.user_follow_company, name='user_follow_company'),
 	url(r'^company/user/interess/$', product.user_interess_product, name='user_interess_product'),
 	url(r'^company/product/add_comment/$', comment.product_add_comment, name='product_add_comment'),
 	url(r'^company/product/comments/(?P<product_id>\d+)/$', comment.product_load_comments_main, name='product_load_comment_main'),
 	url(r'^company/product/comments_else/item=(?P<product_id>\d+)/$', comment.product_load_comments_else, name='product_load_comment_else'),
 	url(r'^company/product/comments/(?P<comment_id>\d+)/edit_page/$', comment.get_edit_product_comment, name='product_comment_edit_page'),
 	url(r'^company/product/comments/(?P<comment_id>\d+)/edit/$', comment.edit_product_comment, name='product_comment_edit'),
 	url(r'^company/product/comments/(?P<comment_id>\d+)/delete/$', comment.delete_product_comment, name='product_comment_delete'),

 	#Product Trade

 	url(r'^company/product/trade/(?P<product_id>\d+)/start/$', trade.start_product_trade, name='start_product_trade'),
 	url(r'^user/trade/t/$', trade.get_user_trades, name='user_all_trades'),
 	url(r'^company/trade/t/$', trade.get_company_trades, name='company_all_trades'),
 	url(r'^user/trade/(?P<trade_id>\d+)/$', trade.get_user_single_trade, name='user_single_trade'),
 	url(r'^company/trade/(?P<trade_id>\d+)/$', trade.get_company_single_trade, name='company_single_trade'),
 	
    url(r'^trade/message/(?P<trade_id>\d+)/$', trade.load_trade_messages, name='trade_messages'),
 	url(r'^trade/message/save/(?P<trade_id>\d+)/text/$', trade.save_trade_message, name='save_trade_messages'),
    url(r'^trade/message/save/(?P<trade_id>\d+)/images/$', trade.save_trade_message_images, name='save_trade_messages_images'),
    url(r'^trade/message/save/(?P<trade_id>\d+)/location/$', trade.save_trade_message_location, name='save_trade_message_location'),
    url(r'^trade/message/save/(?P<trade_id>\d+)/status/$', trade.change_trade_status, name='change_trade_status'),
    
    url(r'^trade/products/company/main_trade=(?P<trade_id>\d+)/$', trade.get_trades_products_company, name='products_trades'),
    url(r'^trade/customers/(?P<product_id>\d+)/(?P<trade_id>\d+)/$', trade.get_trades_customers, name='products_customers'),
    url(r'^trade/companies/users/(?P<trade_id>\d+)/$', trade.get_trades_company_users, name='company_trades'),
    url(r'^trade/products/(?P<company_id>\d+)/(?P<trade_id>\d+)/$', trade.get_trades_products_users, name='company_products'),
    
    url(r'^trades/succeeded/company/$', trade.get_succeeded_company_trades, name='company_succeeded_trades'),
    url(r'^trades/succeeded/company/(?P<product_id>\d+)/$', trade.get_customers_succeeded_trade, name='customers_succeeded_trades'),
    url(r'^trades/failed/company/$', trade.get_failed_company_trades, name='company_failed_trades'),
    url(r'^trades/failed/company/(?P<product_id>\d+)/$', trade.get_customers_failed_trade, name='customers_failed_trades'),
    
    url(r'^trades/succeeded/user/$', trade.get_succeeded_user_trades, name='user_succeeded_trades'),
    url(r'^trades/succeeded/user/(?P<company_id>\d+)/$', trade.get_succeeded_products_trades, name='products_succeeded_trades'),
    url(r'^trades/failed/user/$', trade.get_failed_user_trades, name='user_failed_trades'),
    url(r'^trades/failed/user/(?P<company_id>\d+)/$', trade.get_failed_products_trades, name='products_failed_trades'),
    url(r'^trades/restart/user/(?P<trade_id>\d+)/$', trade.user_restart_trade, name='user_restart_trades'),


 	#APIs

 	url(r'^api/products/$', views.api_get_products, name='api_products'),
    url(r'^users/tags/all/$', views.api_get_users_tags, name='users_tags'),
    url(r'^api/search/users/all/$', views.api_search_get_all_users, name='search_users'),
    url(r'^api/search/companies/all/$', views.api_search_get_all_companies, name='search_companies'),
    url(r'^api/search/products/all/$', views.api_search_get_all_products, name='search_products'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)