from django.db import models
from django import forms
from django.contrib.auth.models import User
from users.models import UserProfile
from allauth.account.forms import ChangePasswordForm
from .models import Report

class settingsImage(forms.ModelForm):
	image = forms.ImageField(widget=forms.FileInput(attrs={'onchange': 'document.getElementById("settingsImage").click()'}))

	class Meta:
		model = UserProfile
		fields = ["image"]

class settingsPersonal(forms.ModelForm):

	class Meta:
		model = User
		fields = ("first_name", "last_name")


class settingsSecurity(ChangePasswordForm):

	oldpassword = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': ''}))
	password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': ''}))
	password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': ''}))

	def save(self, *args, **kwargs):
		super(settingsSecurity, self).save()

class settingsLocalization(forms.ModelForm):

	class Meta:
		model = UserProfile
		fields = ("currency", "language")

class settingsReport(forms.ModelForm):

	class Meta:
		model = Report
		fields = ("report_overdue", "report_recurring", "report_missing", "report_monthly")
		