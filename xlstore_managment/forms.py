from datetime import datetime, timedelta
from django import forms
from models import MS_LicenceKey, MS_LicenceKeyActivations, MS_CompanyTeller
from xlstore.forms import CURRENCIES
from django.core.exceptions import ValidationError


STATUS = (
		('activated', 'Activated'),
		('desactivated', 'Desactivated'),
		('paused', 'Paused')
	)


today = datetime.now().date()
expary_date = datetime.now().date() + timedelta(days=30)


class MS_LicenceKeyForm(forms.ModelForm):
	licence_key = forms.CharField(widget=forms.TextInput(attrs={'style':'width:40%'}))
	status = forms.ChoiceField(widget=forms.Select(attrs={'style':'width:40%'}), choices=STATUS)
	expary_date = forms.DateField(widget=forms.DateInput(attrs={'style':'width:40%', 'class':'vDateField', 'value':expary_date}))
	ammount = forms.CharField(widget=forms.NumberInput(attrs={'min':'1', 'style':'width:40%'}))
	currency = forms.ChoiceField(widget=forms.Select(attrs={'style':'width:40%'}), choices=CURRENCIES)

	def __init__(self, *args, **kwargs):
		super(MS_LicenceKeyForm, self).__init__(*args, **kwargs)
		self.fields['company'].disabled = True
		self.fields['licence_key'].disabled = True
		self.fields['status'].required = False
		self.fields['activated_date'].disabled = True
		self.fields['activated_date'].value = datetime.now().date()
		self.fields['expary_date'].value = datetime.now().date() + timedelta(days=30)

	class Meta:
		fields = ('company', 'licence_key', 'status', 'ammount', 'currency', 'activated_date', 'expary_date',)
		model = MS_LicenceKey


class MS_TellerForm(forms.ModelForm):
	full_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter Teller Full Name'}))
	username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter Teller Username'}))
	email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder':'Enter Teller Email'}))
	address = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter Teller Address'}))
	phone_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter Teller Phone Number', 'type':'tel'}))
	teller_image = forms.ImageField(widget=forms.FileInput(attrs={'required':'required', 'accept':'images/*'}))

	class Meta:
		fields = ('teller_image','full_name', 'username', 'email', 'address', 'phone_number',)
		model = MS_CompanyTeller


class MS_AdminUpdateTeller(forms.ModelForm):
	full_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter Teller Full Name'}))
	email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder':'Enter Teller Email'}))
	address = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter Teller Address'}))
	phone_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter Teller Phone Number', 'type':'tel'}))

	class Meta:
		fields = ('full_name', 'email', 'address', 'phone_number',)
		model = MS_CompanyTeller