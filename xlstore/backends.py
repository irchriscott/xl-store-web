from models import Company, User, Products
import re

class CompanyAuth(object):
	def authenticate_company(self, email=None, password=None):
		try:
			#company = Company.objects.extra(where=["email='%s' OR phone_number = '%s'", "password = '%s'"], params=[log_email, log_email, log_password])
			company = Company.objects.get(email=email)
			if company.password == password:
				return company
		except Company.DoesNotExist:
			return None

	def get_company(self, company_id):
		try:
			company = Company.objects.get(pk=company_id)
			if company.is_activated:
				return company
			return None
		except Company.DoesNotExist:
			return None

class UserAuth(object):
	def authenticate_user(self, email=None, password=None):
		try:
			user = User.objects.get(email=email)
			if user.password == password:
				return user
		except User.DoesNotExist:
			return None

	def check_email(self, email=None):
		try:
			#company = Company.objects.extra(where=["email='%s' OR phone_number = '%s'", "password = '%s'"], params=[log_email, log_email, log_password])
			company = Company.objects.get(email=email)
			return company
		except Company.DoesNotExist:
			return None


def email_check(mail):
    if re.match("^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$", mail) is not None:
    	return True
    else:
    	return False


class Helpers(object):

	char_strings = ['~', '!', '%', '^', '&', '*', '(', ')', '+', '?', '<', '>', '|', ',', '.', '/', '[', ']', '{', '}', '=']

	def get_post_tags_user(self, sentence):

		for char in self.char_strings:
			text = sentence.replace(char, '')

		words = text.split()
		tagged_users = []
		tagged_companies = []
		tagged_products = []

		for word in words:
			if word[0] == "@":
				if self.check_company_exists(word[1:]) is not None:
					tagged_companies.append({'pk':self.check_company_exists(word[1:]), 'company':word[1:]})
				elif self.check_user_exists(word[1:]) is not None:
					tagged_users.append({'pk':self.check_user_exists(word[1:]), 'username':word[1:]})

				if self.check_product_exists(word[1:]) is not None:
					product = self.check_product_exists(word[1:])
					tagged_products.append({'pk':product.pk, 'prod':product.product_name, 'company':product.company.name_dotted})

		return {'users': tagged_users, 'companies': tagged_companies, 'products': tagged_products}


	def check_user_exists(self, username):
		try:
			user = User.objects.get(user_name = username)
			if user:
				return user.pk
		except User.DoesNotExist:
			return None


	def check_company_exists(self, company_name):
		try:
			company = Company.objects.get(name_dotted=company_name)
			if company:
				return company.pk
		except Company.DoesNotExist:
			return None


	def get_product_pk(self, product_tag):
		product = product_tag.split("__")
		if len(product) > 2:
			_first = product[0]
			_next = product[1]
			_end = product[2]

			try:
				_prod_id = int(_next)
				return _prod_id
			except ValueError:
				return None
		else:
			return None


	def check_product_exists(self, product_tag):
		_product_pk = self.get_product_pk(product_tag)

		if _product_pk is not None:
			try:
				_product = Products.items.get(pk=_product_pk)
				if _product:
					return _product
			except Products.DoesNotExist:
				return None
		else:
			return None


	def get_linked_post_text(self, sentence):
		_data = self.get_post_tags_user(sentence)
		_users = _data['users']
		_companies = _data['companies']
		_products = _data['products']

		_all_dic = {}

		for user in _users:
			_all_dic['@%s' % user['username']] = '<a href="/user/%s/" class="xl_mentioned_user" data-user="%s">@%s</a>' % (user['username'], user['pk'], user['username'])

		for company in _companies:
			_all_dic['@%s' % company['company']] = '<a href="/company/%s/" class="xl_mentioned_company" data-company="%s">@%s</a>' % (company['company'], company['pk'], company['company'])

		for product in _products:
			_name_prod = product['prod'].replace(' ','') + "__" + str(product['pk']) + "__"
			_all_dic['@%s' % _name_prod] = '<a href="/company/%s/products/%s/" class="xl_mentioned_product" data-product="%s">%s</a>' % (product['company'], product['pk'], product['pk'], product['prod'])

		_rep = dict((re.escape(k), v) for k, v in _all_dic.iteritems())

		pattern = re.compile("|".join(_rep.keys()))
		text = pattern.sub(lambda m: _rep[re.escape(m.group(0))], sentence)

		return {'text': text, 'users': _users, 'companies': _companies, 'products': _products}
