from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django_countries.widgets import CountrySelectWidget
from django_countries.fields import LazyTypedChoiceField
from datetime import datetime
from django import forms
from models import *
from django.utils import timezone

UGANDA = 'USH'
CONGO = 'FRC'
EUROPE = 'EURO'
USA = 'USD'
CHINA = 'YUAN'
ENGLAND = 'GBP'
UAE = 'AED'

CURRENCIES = (
		(USA, 'United State Dollars'),
		(UGANDA, 'Uganda Shilling'),
		(CONGO, 'Congolese Franc'),
		(EUROPE, 'Euro'),
		(CHINA, 'China Yuan'),
		(ENGLAND, 'British Pound'),
		(UAE, 'Arab Emairate United Dirham')
	)

CATEGORIES = (
		(1,''),
		(2,''),
		(3,''),
		(4,''),
		(5,''),
		(6,''),
		(7,''),
		(8,'')
	)

#CATEGORIES = [(i,i) for i in range(1000000000)]

#For Company

class CompanyCreateForm(UserCreationForm):

	def __init__(self, *args, **kargs):
		super(CompanyCreateForm, self).__init__(*args, **kargs)
		del self.fields['username']

		class Meta:
			model = Company
			fields = ("email",)


class CompanyChangeForm(UserChangeForm):
	
	def __init__(self, *arg, **kargs):
		super(CompanyChangeForm, self).__init__(*arg, **kargs)
		del self.fields['username']

		class Meta:
			model = Company


class CompanyForm(forms.ModelForm):
	name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Company Name'}))
	email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Enter Email Address'}))
	town = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter Town'}))
	phone_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter Phone Number', 'type':'tel'}))
	password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Enter Password'}))
	conf_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Confirm Password'}))
	name_dotted = forms.CharField(widget=forms.HiddenInput())

	class Meta:
		model = Company
		fields = ('name', 'email', 'country', 'town', 'phone_number', 'password', 'name_dotted',)
		widgets = {'country': CountrySelectWidget()}


class CompanyProfileImage(forms.ModelForm):
	profile_image = forms.ImageField(widget=forms.FileInput(attrs={'accept':'image/*'}))

	class Meta:
		model = Company
		fields = ('profile_image',)


class CompanyCoverImage(forms.ModelForm):
	cover_image = forms.ImageField(widget=forms.FileInput(attrs={'accept':'image/*'}))

	class Meta:
		model = Company
		fields = ('cover_image',)


class UpdateCompanyForm(forms.ModelForm):
	name = forms.CharField(widget=forms.TextInput())
	phone_number = forms.CharField(widget=forms.TextInput(attrs={'type':'tel'}))
	motto = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter Company Motto'}))
	description = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Enter Company Description'}))

	def __init__(self, *args, **kwargs):
		super(UpdateCompanyForm, self).__init__(*args, **kwargs)
		self.fields['phone_number'].required = False
		self.fields['motto'].required = False
		self.fields['description'].required = False

	class Meta:
		model = Company
		fields = ('name', 'phone_number', 'motto', 'description',)


class CategoryForm(forms.ModelForm):
	name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter Category Name'}))
	description = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Category Description', 'max-length':'150'}))
	created_date = forms.DateTimeField(widget=forms.HiddenInput(), initial=timezone.now())

	class Meta:
		model = Categories
		fields = ('name', 'description', 'created_date',) 


class ProductForm(forms.ModelForm):
	product_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter Product Name'}))
	category = forms.ChoiceField(widget=forms.Select, choices=CATEGORIES)
	image = forms.ImageField(widget=forms.FileInput(attrs={'style':'display:none', 'accept':'image/*'}))
	price = forms.CharField(widget=forms.NumberInput(attrs={'placeholder':'Enter Product Price', 'min':'0'}))
	currency = forms.ChoiceField(widget=forms.Select, choices=CURRENCIES)
	product_description = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Enter Product Description'}))

	class Meta:
		model = Products
		fields = ('product_name', 'category', 'image', 'price', 'currency', 'product_description',)


class EditProduct(forms.ModelForm):
	product_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter Product Name', 'id':'id_product_name_edit'}))
	price = forms.CharField(widget=forms.NumberInput(attrs={'placeholder':'Enter Product Price', 'min':'0', 'id':'id_price_edit'}))
	currency = forms.ChoiceField(widget=forms.Select(attrs={'id':'id_currency_edit'}), choices=CURRENCIES,)
	product_description = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Enter Product Description', 'id':'id_description_edit'}))

	class Meta:
		model = Products
		fields = ('product_name', 'price', 'currency', 'product_description',)


class ProductPicturesUpload(forms.ModelForm):
	image = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True, 'accept': 'image/*', 'id':'id_product_images_upload'}))

	class Meta:
		model = ProductPictures
		fields = ('image',)


class AdvertismentsForm(forms.ModelForm):
	video = forms.FileField(widget=forms.ClearableFileInput(attrs={'accept':'video/*'}))
	advertisment_text = forms.CharField(widget=forms.Textarea())
	posted_date = forms.DateTimeField(widget=forms.HiddenInput(), initial=timezone.now())

	class Meta:
		model = Advertisments
		fields = ('video', 'advertisment_text', 'posted_date',)


class ProductCommentForm(forms.ModelForm):
	comment = forms.CharField(widget=forms.Textarea())

	class Meta:
		model = ProductComments
		fields = ('comment',)


#For User


class UserForm(forms.ModelForm):
	full_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Full Name'}))
	user_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter User Name'}))
	email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Enter Email Address'}))
	town = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Town'}))
	gender = forms.ChoiceField(widget=forms.Select, choices=GENDER_CHOICES)
	password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password'}))
	conf_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))

	class Meta:
		model = User
		fields = ('full_name', 'user_name', 'email', 'country', 'town', 'gender', 'password',)
		widgets = {'country': CountrySelectWidget()}


class UserProfileImage(forms.ModelForm):
	profile_image = forms.ImageField(widget=forms.FileInput(attrs={'accept':'image/*'}))

	class Meta:
		model = User
		fields = ('profile_image',)


class UserCoverImage(forms.ModelForm):
	cover_image = forms.ImageField(widget=forms.FileInput(attrs={'accept':'image/*'}))

	class Meta:
		model = User
		fields = ('cover_image',)


class UpdateUserProfile(forms.ModelForm):
	full_name = forms.CharField(widget=forms.TextInput())
	town = forms.CharField(widget=forms.TextInput(attrs={}))
	phone_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter Phone Number', 'type':'tel'}))
	biography = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Tell Us About You'}))

	def __init__(self, *args, **kwargs):
		super(UpdateUserProfile, self).__init__(*args, **kwargs)
		self.fields['phone_number'].required = False
		self.fields['biography'].required = False

	class Meta:
		model = User
		fields = ('full_name', 'country', 'town', 'phone_number', 'biography',)
		widgets = {'country': CountrySelectWidget()}


class PostForm(forms.ModelForm):
	post_file = forms.FileField(widget=forms.ClearableFileInput(attrs={'accept':'image/*, video/*', 'required': False}))
	post_text = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Enter Post Text'}))
	file_type = forms.CharField(widget=forms.HiddenInput())

	def __init__(self, *args, **kwargs):
		super(PostForm, self).__init__(*args, **kwargs)
		self.fields['post_file'].required = False
		self.fields['file_type'].required = False

	class Meta:
		model = Posts
		fields = ('post_text', 'post_file', 'file_type',)


class EditPost(forms.ModelForm):
	post_text = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Enter Post Text', 'id':'id_post_text_edit'}))

	class Meta:
		model = Posts
		fields = ('post_text',)


class PostReplyForm(forms.ModelForm):
	reply_text = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Enter Your Reply', 'rows':'0', 'cols':'0'}))
	reply_image = forms.ImageField(widget=forms.ClearableFileInput(attrs={'accept':'image/*'}), required=False)

	def __init__(self, *args, **kwargs):
		super(PostReplyForm, self).__init__(*args, **kwargs)
		self.fields['reply_image'].required = False

	class Meta:
		model = PostReplies
		fields = ('reply_text', 'reply_image',)

		


