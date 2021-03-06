from django import forms 
from django.core.validators import RegexValidator
import math

POSITION_CHOICES=[
("long", "long"),
("short", "short")
]

KIND_CHOICES=[
("call", "call"), 
("put", "put")
]

MODEL_CHOICES=[
("BlackScholes", "BlackScholes"),
("BinomialTree", "BinomialTree")
]

EXER_CHOICES=[
("european", "european"),
("american", "american")
]

STEPS_CHOICES=[
(10,"10"),
(25,"25"),
(50,"50")
]

alpha = RegexValidator(r'^[a-z A-Z]*$', 'Only letters are allowed.')

class StrategyForm(forms.Form):
	S0 = forms.FloatField(min_value=1, max_value=1000)
	sigma = forms.FloatField(min_value=0.1, max_value=100, required=True)
	q = forms.FloatField(min_value=0, max_value=100, required=True)
	r = forms.FloatField(min_value=0, max_value=100)

	# Clean percentages from user form to decimals for use in pricing models
	def clean_data(self): 
		self.cleaned_data = super().clean()
		self.cleaned_data['sigma'] = self.cleaned_data['sigma']/100
		self.cleaned_data['q'] = self.cleaned_data['q']/100
		self.cleaned_data['r'] = self.cleaned_data['r']/100

class LegsForm(forms.Form): 
	position = forms.ChoiceField(choices=POSITION_CHOICES)
	kind = forms.ChoiceField(choices=KIND_CHOICES)
	K = forms.FloatField(min_value=1, max_value=1000)
	T = forms.FloatField(min_value=.01, max_value=20)

	# Convert time to expiration to years for pricing models
	# def clean(self): 
	# 	self.cleaned_data = super().clean()
	# 	self.cleaned_data['T'] = self.cleaned_data['T']/365

class StockForm(forms.Form): 
	longqty = forms.IntegerField(min_value=0, max_value=100)
	shortqty = forms.IntegerField(min_value=0, max_value=100)

class PriceModelForm(forms.Form): 
	model = forms.ChoiceField(choices=MODEL_CHOICES)
	exer_type = forms.ChoiceField(choices=EXER_CHOICES, required=False)
	steps = forms.ChoiceField(choices=STEPS_CHOICES, required=False)

	def clean(self):
		self.cleaned_data = super().clean()
		model = self.cleaned_data.get("model")
		if model == "BlackScholes":
			self.cleaned_data['exer_type']=None
			self.cleaned_data['steps']=None
		elif model == "BinomialTree":
			self.cleaned_data['steps'] = int(self.cleaned_data['steps'])

class VolForm(forms.Form): 
	ticker = forms.CharField(min_length=1, validators=[alpha])
	days = forms.IntegerField(min_value=7)

class RangeForm(forms.Form): 
	range_start = forms.FloatField(min_value=0, max_value=999)
	range_end = forms.FloatField(min_value=1, max_value=1000)

	def clean_data(self): 
		self.cleaned_data = super().clean()
		range_start = self.cleaned_data.get('range_start')
		range_end = self.cleaned_data.get('range_end')
		if range_start >= range_end: 
			message = "Invalid Range"
			self._errors['range_end'] = self.error_class([message])
		self.cleaned_data['range_start'] = math.floor(range_start)
		self.cleaned_data['range_end'] = math.ceil(range_end)























