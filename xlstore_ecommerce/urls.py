from django.conf.urls import url, include
from xlstore_ecommerce import views
from xlstore_ecommerce.views import UseEcommerceService, UsePayPal, UseMobileMoney

paypal = UsePayPal()

urlpatterns = [
	
	#E-Commerce URLs
	
	url(r'^mc/market/access/$', views.user_request_access_market, name='user_access_market'),
    url(r'^mc/market/(?P<company>\d+)/await/$', views.load_and_await_market, name='user_await_market'),
    url(r'^mc/market/(?P<company>\d+)/(?P<user>\d+)/status/load/$', views.check_user_access_market_user, name='check_user_access_market'),
    url(r'^mc/market/access/error/$', views.error_access_market, name='error_access_market'),
    url(r'^mc/market/company/access/(?P<key>[^/]+)/allow/$', views.company_allow_user_access_market, name='company_allow_access'),
    url(r'^mc/market/company/access/(?P<key>[^/]+)/disallow/$', views.company_disallow_market_access, name='company_disallow_access'),
    url(r'^mc/market/user/(?P<user>\d+)/start/$', views.start_new_or_get_last_shopping, name='ecommerce_user_start'),
    url(r'^mc/market/(?P<key>[^/]+)/products/(?P<cart>\d+)/load/$', views.load_market_products, name='load_market_products'),
    url(r'^mc/market/cart/(?P<cart>\d+)/load/$', views.load_shopping_cart, name='load_current_cart'),
    url(r'^mc/market/cart/(?P<cart>\d+)/single/load/$', views.load_single_cart_gen, name='load_single_cart'),
    url(r'^mc/market/cart/(?P<cart>\d+)/load/json/$', views.load_shopping_cart_json, name='load_current_cart_json'),
    url(r'^mc/market/cart/(?P<cart>\d+)/load/company/$', views.load_shopping_cart_company, name='load_current_cart_comp'),
    url(r'^mc/market/cart/(?P<cart>\d+)/finish/$', views.finish_shopping_cart, name='finish_shopping_cart'),
    url(r'^mc/market/cart/(?P<cart>\d+)/pay/$', views.place_payment_cart, name='pay_shopping_cart'),
    url(r'^mc/market/cart/(?P<cart>\d+)/product/add/$', views.add_item_to_shopping_cart, name='add_item_to_shopping_cart'),
    url(r'^mc/market/item/(?P<item>\d+)/remove/$', views.remove_item_to_shopping_cart, name='remove_item_to_shopping_cart'),
    url(r'^mc/market/item/(?P<item>\d+)/update/$', views.update_item_to_shopping_cart, name='update_item_to_shopping_cart'),

    #E-Commerce Settings

    url(r'^mc/company/settings/$', views.load_company_ecommerse_settings, name='load_ecommerce_settings'),
    url(r'^mc/company/settings/ecommerce/use/$', views.UseEcommerceService.as_view(), name='use_ecommerce_settings'),
    url(r'^mc/company/settings/paypal/use/$', UsePayPal.as_view(), name='use_paypal_settings'),
    url(r'^mc/company/settings/paypal/add/$', paypal.add_paypal_account, name='add_paypal_settings'),
    url(r'^mc/company/settings/mobile/use/$', UseMobileMoney.as_view(), name='use_mobile_settings'),
]