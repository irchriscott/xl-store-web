from django.conf.urls import url, include
from xlstore_managment import views
from xlstore_managment.views import MS_Welcome
from xlstore_managment.views import MS_SignUp
from xlstore_managment.views import AddFreshProduct
from xlstore_managment.views import AddFromProduct
from xlstore_managment.views import ReduceProductTrade, AllowUserSucceed, PrintBill, Currency, ModifySMPassword
from xlstore_managment.views import Internationalize, FreeAccessMarket, TimeAccessMarket, CommentProduct, AlwaysAdmin
from xlstore_managment.views import ModifyMSPassword, LicenceKey, AddTeller, AddMobileMoneyNumber

mobile = AddMobileMoneyNumber()

urlpatterns = [
	
	#SIGN UP MS

    url(r'^welcome/$', MS_Welcome.as_view(), name='managment_welcome'),
    url(r'^signup/$', MS_SignUp.as_view(), name='managment_signup'),
    url(r'^thanks/$', views.get_thanks_page, name='managment_thanks'),

    #SETTINGS, AND LOGS MS

    url(r'^ms_else/admin/activate/$', views.activate_ms_admin, name='managment_activate_admin'),
    url(r'^ms_else/admin/desactivate/$', views.desactivate_ms_admin, name='managment_desactivate_admin'),
    url(r'^ms_else/admin/logout/$', views.logout_ms, name='managment_logout'),

    #PRODUCTS MS

    url(r'^pms_c/$', views.get_products_managment_system, name='managment_products'),
    url(r'^pms_c/add_pms_c/$', AddFreshProduct.as_view(), name='managment_add_product'),
    url(r'^pms_c/add_fp_pms_c/$', AddFromProduct.as_view(), name='managment_add_from_product'),
    url(r'^pms_c/all/$', views.get_all_ms_products, name='managment_products_all'),
    url(r'^pms_c/categ/(?P<category_id>\d+)/$', views.get_product_categories, name='managment_products_category'),
    url(r'^pms_c/update/(?P<product_id>\d+)/$', views.update_ms_product, name='managment_products_update'),
    url(r'^pms_c/t_itbp/$', views.is_to_be_posted_toggle, name='managment_tooge_posted'),

    #HOME MS

	url(r'^hms_c/$', views.get_home_managment_system, name='managment_home'),
	url(r'^hms_c/cart/$', views.get_all_ms_cart_products, name='managment_products_cart'),
    url(r'^hms_c/cart/filter/$', views.filter_ms_cart_product, name='managment_products_filter'),
    url(r'^hms_c/bill/lcb/$', views.get_next_bill, name='managment_load_bill'),
    url(r'^hms_c/bill/create/$', views.create_this_bill, name='managment_create_bill'),
    url(r'^hms_c/bill/sob_u/$', views.load_users_for_bill, name='managment_search_user'),
    url(r'^hms_c/bill/add_i/$', views.add_items_to_bill, name='managment_add_item_to_bill'),
    url(r'^hms_c/bill/update_i/$', views.update_bill_item, name='managment_update_item_bill'),
    url(r'^hms_c/bill/remove_i/$', views.remove_bill_item, name='managment_remove_item_bill'),
    url(r'^hms_c/bill/finish/$', views.finish_current_bill, name='managment_finish_bill'),

    #BILLS MS

    url(r'^bms_c/$', views.get_all_ms_bills, name='managment_get_bills'),
    url(r'^bms_c/today/$', views.get_today_bills, name='managment_get_today_bills'),
    url(r'^bms_c/date/b_date=(?P<bill_date>[^/]+)$', views.load_bill_by_date, name='managment_get_date_bills'),
    url(r'^bms_c/date/month=(?P<month>[^/]+)&year=(?P<year>[^/]+)$', views.load_bill_by_month_year, name='managment_get_month_bills'),
    url(r'^bms_c/bill/(?P<bill_id>\d+)/$', views.load_bill_single_bill, name='managment_get_single_bill'),
    url(r'^bms_c/bill/search/$', views.get_searched_bill, name='managment_search_bill'),

    #MANAGMENT MS

    url(r'^mms_c/$', views.get_inventory_managment_system, name='managment_managment'),
    url(r'^mms_c/p/$', views.get_product_managment_ms, name='managment_msp'),
    url(r'^mms_c/p/all/$', views.get_msp_all_products, name='managment_msp_all'),
    url(r'^mms_c/p/item=(?P<product_id>\d+)&month=(?P<month>\d+)&year=(?P<year>\d+)$', views.get_msp_single_product, name='managment_msp_single'),
    url(r'^mms_c/p/item=(?P<product_id>\d+)&month=(?P<month>\d+)&year=(?P<year>\d+)/edit/$', views.get_ms_single_product_edit, name='managment_msp_single_edit'),
    url(r'^mms_c/p/item=(?P<product_id>\d+)&month=(?P<month>\d+)&year=(?P<year>\d+)/chart/$', views.get_msp_single_product_charts, name='managment_msp_single_charts'),
    url(r'^mms_c/d/$', views.get_daily_managment_ms, name='managment_msd'),
    url(r'^mms_c/d/date=(?P<date>[^/]+)$', views.get_daily_managment_ms_day, name='managment_msd_single'),
    url(r'^mms_c/d/month=(?P<month>[^/]+)&year=(?P<year>[^/]+)$', views.get_monthly_managment_ms_day, name='managment_msd_month'),
    url(r'^mms_c/d/date=(?P<date>[^/]+)/chart/$', views.get_daily_managment_ms_day_chart, name='managment_msd_single_chart'),
    url(r'^mms_c/d/month=(?P<month>[^/]+)&year=(?P<year>[^/]+)/chart/$', views.get_monthly_managment_ms_day_chart, name='managment_msd_month_chart'),
    
    #CUSTOMERS MS

    url(r'^mms_c/c/$', views.get_customers_managment_ms, name='managment_msc'),
    url(r'^mms_c/c/all/$', views.get_msc_all_customers, name='managment_msc_all'),
    url(r'^mms_c/c/chart/$', views.get_msc_customers_world_sale, name='managment_msc_chart'),
    url(r'^mms_c/c/(?P<user_id>\d+)/$', views.get_msc_single_customers, name='managment_msc_single'),
    url(r'^mms_c/c/mail/(?P<user_id>\d+)/$', views.customer_ms_send_mail, name='managment_msc_send_mail'),
    url(r'^mms_c/c/anonymous/$', views.get_msc_anonymous_customers, name='managment_msc_anonymous'),


    #MS DATA

    url(r'^mms_c/dt/$', views.get_data_managment_ms, name='managment_msdt'),
    url(r'^mms_c/dt/trades/$', views.get_msdt_trades_all, name='managment_msdt_trades'),
    url(r'^mms_c/dt/trades/agreed/$', views.get_msdt_agreed_trades, name='managment_msdt_agreed_trades'),
    url(r'^mms_c/dt/trades/agreed/(?P<trade_id>\d+)/$', views.get_msdt_single_agreed_trade, name='managment_msdt_single_agreed_trade'),
    url(r'^mms_c/dt/trades/agreed/(?P<trade_id>\d+)/update/$', views.update_msdt_single_agreed_trade, name='managment_msdt_update_agreed_trade'),
    url(r'^mms_c/dt/trades/agreed/(?P<trade_id>\d+)/add_to_cart/$', views.add_msdt_trade_to_cart, name='managment_msdt_add_to_cart_trade'),
    url(r'^mms_c/dt/trades/agreed/(?P<trade_id>\d+)/reactivate/$', views.reactivate_msdt_agreed_trade, name='managment_msdt_reactivate_trade'),
    url(r'^mms_c/dt/trades/(?P<product_id>\d+)/$', views.get_msdt_users_trades, name='managment_msdt_users_trades'),
    url(r'^mms_c/dt/trades/(?P<trade_id>\d+)/agree/$', views.agree_msdt_user_trade, name='managment_msdt_agree_trade'),
    url(r'^mms_c/dt/interess/$', views.get_msdt_product_interess, name='managment_msdt_interess'),
    url(r'^mms_c/dt/interess/(?P<product_id>\d+)/interessers/$', views.get_msdt_single_product_interessers, name='managment_msdt_interessers'),

    #MS TELLER

    url(r'mms_c/tl/$', views.get_teller_managment_ms, name='managment_mstl'),
    url(r'mms_c/tl/all/$', views.get_company_tellers_all, name='managment_mstl_all'),
    url(r'mms_c/tl/add/$', AddTeller.as_view(), name='managment_mstl_add'),
    url(r'mms_c/tl/login/$', views.login_teller, name='managment_mstl_login'),
    url(r'mms_c/tl/logout/$', views.logout_teller, name='managment_mstl_logout'),
    url(r'mms_c/tl/teller/id=(?P<teller_id>\d+)$', views.get_company_single_teller, name='managment_mstl_single_teller'),
    url(r'mms_c/tl/teller/id=(?P<teller_id>\d+)/profile/$', views.load_teller_profile, name='managment_mstl_teller_profile'),
    url(r'mms_c/tl/teller/edit/username/$', views.update_teller_username, name='managment_mstl_update_username'),
    url(r'mms_c/tl/teller/edit/password/$', views.update_teller_password, name='managment_mstl_update_password'),
    url(r'mms_c/tl/teller/id=(?P<teller_id>\d+)/update/$', views.get_admin_update_teller, name='admin_update_teller_temp'),
    url(r'mms_c/tl/teller/id=(?P<teller_id>\d+)/save/$', views.admin_save_update_teller, name='admin_update_teller'),
    url(r'mms_c/tl/teller/id=(?P<teller_id>\d+)/admin/update/$', views.admin_make_teller_admin, name='admin_update_teller_admin'),

    #MS ECOMMERCE

    url(r'^mms_c/ec/$', views.get_ecommerce_managment_ms, name='managment_msec'),
    url(r'^mms_c/ec/customers/$', views.get_msec_customers, name='managment_msec_customers'),
    url(r'^mms_c/ec/customer/(?P<market>\d+)/$', views.get_msec_customer_carts, name='managment_msec_customer'),
    url(r'^mms_c/ec/customer/(?P<market>\d+)/status/change/$', views.change_user_market_access_status, name='market_change_status'),
    url(r'^mms_c/ec/customer/(?P<cart>\d+)/load/$', views.get_msec_customer_single_cart, name='managment_msec_customer_cart'),
    url(r'^mms_c/ec/customer/(?P<cart>\d+)/accept_or_decline/$', views.accept_or_decline_order, name='managment_msec_accept_or_decline_cart'),
    url(r'^mms_c/ec/customer/(?P<cart>\d+)/ms/add/$', views.add_shopping_cart_to_ms, name='add_cart_to_ms'),


    #MS SETTINGS

    url(r'^mms_c/st/$', views.get_settings_managment_ms, name='managment_msst'),
    url(r'^mms_c/st/genset/$', views.get_msst_general_settings, name='managment_msst_general_set'),
    url(r'^mms_c/st/rpt/$', ReduceProductTrade.as_view(), name='managment_msst_rpt'),
    url(r'^mms_c/st/aus/$', AllowUserSucceed.as_view(), name='managment_msst_aus'),
    url(r'^mms_c/st/apb/$', PrintBill.as_view(), name='managment_msst_apb'),
    url(r'^mms_c/st/cur/$', Currency.as_view(), name='managment_msst_cur'),
    url(r'^mms_c/st/inter_p/$', Internationalize.as_view(), name='managment_msst_inter_p'),
    url(r'^mms_c/st/fam/$', FreeAccessMarket.as_view(), name='managment_msst_fam'),
    url(r'^mms_c/st/tam/$', TimeAccessMarket.as_view(), name='managment_msst_tam'),
    url(r'^mms_c/st/mobile/add/$', AddMobileMoneyNumber.as_view(), name='managment_msst_mm_add'),
    url(r'^mms_c/st/mobile/(?P<number>\d+)/remove/$', mobile.remove, name='managment_msst_mm_delete'),
    url(r'^mms_c/st/com_prod/$', CommentProduct.as_view(), name='managment_msst_com_prod'),
    url(r'^mms_c/st/secset/$', views.get_msst_security_settings, name='managment_msst_security_set'),
    url(r'^mms_c/st/admin/$', AlwaysAdmin.as_view(), name='managment_msst_admin'),
    url(r'^mms_c/st/sm_p/$', ModifySMPassword.as_view(), name='managment_msst_sm_p'),
    url(r'^mms_c/st/ms_p/$', ModifyMSPassword.as_view(), name='managment_msst_ms_p'),
    url(r'^mms_c/st/lk/$', LicenceKey.as_view(), name='managment_msst_lk'),
]