from xlstore_managment.models import *
from xlstore_managment.helpers import intword, intcomma
from xlstore.models import Company, Address
from django.core.mail import send_mail
from django.conf import settings


class MS_CompanyAuthentication(object):

	def ms_authenticate(self, company=None, username=None, password=None):
		
		try:
			ms_administrator = MS_CompanyAdministrator.objects.get(company=company)

			if ms_administrator.username == username and ms_administrator.password == password:
				return ms_administrator

		except MS_CompanyAdministrator.DoesNotExist:
			return None


def get_bill_to_send(request, bill):
	receipt = MS_Receipts.objects.get(pk=bill)
	currency = receipt.company.get_currency()
	address = Address.objects.filter(company=receipt.company.company.pk).first()

	receipt_content = ''
	receipt_content += '<div style="width:calc(100% - 100px) !important; margin:auto; background:#eee; border:2px solid #00c6d7; padding:15px; font-family: Avenir,Avenir Next,Helvetica Neue,Segoe UI,Helvetica,Arial,sans-serif !important;">'
	receipt_content += '<div class="xl-ms-receipt-content">'
	receipt_content += '<div>'
	receipt_content += '<h2>%s</h2>' % receipt.company.company.name
	receipt_content += '<p style="margin-top:-12px !important;"><strong>Email : </strong>%s</p>' % receipt.company.company.email
	receipt_content += '<p style="margin-top:-12px !important;"><strong>Address : </strong>%s</p>' % address.address if address is not None else "Null"
	receipt_content += '<p style="margin-top:-12px !important;"><strong>Phone Number : </strong>%s</p>' % receipt.company.company.phone_number
	receipt_content += '</div>'
	receipt_content += '<h3 style="padding-bottom: 10px; border-bottom: 1px solid #bbb; font-size: 18px; text-align: center;">Receipt No %s</h3>' % receipt.receipt_number
	receipt_content += '<div style="border-bottom: 1px solid #bbb !important; padding: 0 7px; margin-bottom: 10px; margin-top:-10px !important;">'
	receipt_content += '<div style="float: left; border-radius: 4px; margin-right: 10px; width: 50px; height: 50px; background:#333;">'
	receipt_content += '<img style="width: 50px; height: 50px; border-radius: 4px;" src="%s" />' % "http://127.0.0.1:8000/media" + receipt.user.get_profile_image() if receipt.user is not None else "http://127.0.0.1:8000/static/images/default_user.jpg" 
	receipt_content += '</div>'
	receipt_content += '<div class="user-details">'
	receipt_content += '<br/>'
	receipt_content += '<div style="float:left;"><p style="font-weight: bold; white-space: normal; margin-top:-14px !important;">%s <span class="username">@%s</span></p>' % (receipt.user.full_name if receipt.user else receipt.username, receipt.user.user_name if receipt.user else "")
	receipt_content += '<p style="margin-top:-10px !important;"><strong>Email : </strong>%s</p></div>' % receipt.user.email if receipt.user else receipt.email
	receipt_content += '<div style="float:right; margin-top:-55px !important;"><p><b>Teller : </b> %s</p></div>' % get_receipt_teller(request)
	receipt_content += '</div>'
	receipt_content += '</div>'

	receipt_content += '<div style="width: 100%; white-space: normal; overflow: hidden;">'
	receipt_content += '<table style="width: 100%; font-size: 13px; border-collapse: collapse; border-spacing: 0;">'
	receipt_content += '<thead>'
	receipt_content += '<tr style="text-align:center; text-transform: uppercase; font-size:14px; ">'
	receipt_content += '<th style="padding-bottom: 7px; border-bottom: 2px solid #333;">Code</th>'
	receipt_content += '<th style="padding-bottom: 7px; border-bottom: 2px solid #333;">Name</th>'
	receipt_content += '<th style="padding-bottom: 7px; border-bottom: 2px solid #333;">Price</th>'
	receipt_content += '<th style="padding-bottom: 7px; border-bottom: 2px solid #333;">Quantity</th>'
	receipt_content += '<th style="padding-bottom: 7px; border-bottom: 2px solid #333;">Total</th>'
	receipt_content += '</tr>'
	receipt_content += '</thead>'
	receipt_content += get_receipt_items(request, receipt.pk, currency)
	receipt_content += '</table>'
	receipt_content += '</div>'
	receipt_content += '<div style="margin-top:10px !important;">'
	receipt_content += '<h4><strong>Total : </strong>%s %s</h4>' % (intcomma(receipt.total_paid), currency)
	receipt_content += '<h4 style="margin-top:-15px !important;"><strong>Other Charges : </strong>%s %s</h4>' % (intcomma(receipt.other_charges), currency)
	receipt_content += '<h2 style="margin-top:-10px !important;"><strong>Total Net : </strong>%s %s</h2>' % (intcomma(receipt.total_net), currency)
	receipt_content += '<p style="float:right; margin-top:-40px !important;"><strong>Date : </strong>%s</p>' % receipt.saved_date
	receipt_content += '<h5 style="text-align:center;">Thank You For Coming, See U Next Time !!!</h5>'
	receipt_content += '</div>'
	receipt_content += '</div>'
	receipt_content += '</div>'

	return receipt_content


def get_receipt_items(request, bill, currency):
	products = MS_ReceiptDetails.objects.filter(receipt=bill)
	content = "<tbody>"
	
	if products is not None:
		for product in products:
			content += '<tr style="cursor: default;">'
			content += '<td style="border-bottom: 1px solid #bbb; text-align: center; padding: 8px 0; font-size: 15px;">%s</td>' % product.product.product_code
			content += '<td style="border-bottom: 1px solid #bbb; text-align: center; padding: 8px 0; font-size: 15px;">%s</td>' % product.product.product.product_name
			content += '<td style="border-bottom: 1px solid #bbb; text-align: center; padding: 8px 0; font-size: 15px;">%s %s</td>' % (intcomma(product.item_price), currency)
			content += '<td style="border-bottom: 1px solid #bbb; text-align: center; padding: 8px 0; font-size: 15px;">%s</td>' % product.quantity
			content += '<td style="border-bottom: 1px solid #bbb; text-align: center; padding: 8px 0; font-size: 15px;">%s %s</td>' % (intcomma(product.total), currency)
			content += '</tr>'

	content += '</tbody>'
	return content



def get_receipt_teller(request):
	if 'teller' in request.session:
		teller = MS_CompanyTeller.objects.get(pk=request.session['teller'])
		return teller.full_name
	else:
		return "Admin"


def send_bill_email(request, receipt):
	receipt = MS_Receipts.objects.get(pk=receipt)
	if receipt.user is not None or receipt.email is not None:
		
		subject = "Xl-Store - Purchase Status from %s" % receipt.company.company.name
		message = "THIS IS A RECEIPT FROM %s" % receipt.company.company.name
		html_message = "<div style='background:lightgray;'Hi %s ! <br/><br/> <div style='text-align: center; font-size: 20px;'>Xl-Store and %s is thanking you for being our customer today.<br/><br/> Here is what you bought:</div> <br/><br/> %s <br/><br/><div style='text-align: center; font-size: 18px;'>We will be pleased to have you next time.<br/><br/> <strong>Xl-Store managment</strong></div></div>" % (receipt.user.full_name if receipt.user else receipt.username, receipt.company.company.name, get_bill_to_send(request, receipt.pk))
		
		send_mail(subject, 
			message, 
			settings.EMAIL_HOST_USER, 
			[receipt.user.email if receipt.user is not None else receipt.email], 
			html_message=html_message,
			fail_silently=True)

		return True
	else:
		return False