from django.db import models
from bills.models import Bill
from billtypes.models import BillType
from django import forms

class newBillForm(forms.ModelForm):
	month= forms.DateField(input_formats=['%B %Y'], widget=forms.DateInput(attrs={'class':'datepicker-here', 'data-language':'en', 'data-position':'right top', 'data-min-view':'months','data-view':'months', 'data-date-format':'MM yyyy'}))
	due_date = forms.DateField(input_formats=['%d %B %Y'], widget= forms.DateInput(attrs={'class':'datepicker-here', 'data-language':'en', 'data-position':'right top', 'data-date-format':'dd MM yyyy'}))

	class Meta:
		model = Bill
		fields = ("month", "amount", "due_date", "note", "recurring")

		def __init__(self, *args, **kwargs):
			super(newBillForm, self).__init__(*args, **kwargs)
			self.fields['template'].required = True

class updateBillForm(forms.ModelForm):
	month= forms.DateField(input_formats=['%B %Y'], widget=forms.DateInput(format='%B %Y', attrs={'class':'datepicker-here', 'data-language':'en', 'data-position':'right top', 'data-min-view':'months','data-view':'months', 'data-date-format':'MM yyyy'}))
	due_date = forms.DateField(input_formats=['%d %B %Y'], widget= forms.DateInput(format='%d %B %Y',attrs={'class':'datepicker-here', 'data-language':'en', 'data-position':'right top', 'data-date-format':'dd MM yyyy'}))

	class Meta:
		model = Bill
		fields = ("month", "amount", "due_date", "note", "recurring")

		def __init__(self, *args, **kwargs):
			super(updateBillForm, self).__init__(*args, **kwargs)
			self.fields['template'].required = True


