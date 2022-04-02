from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from settings.models import Report
from django.utils import translation

from django.db.models.signals import post_save
from allauth.account.signals import user_logged_in
from django.dispatch import receiver

@receiver(post_save, sender=User)
def populateReportModel(instance, sender, **kwargs):
	if sender is User:
		if kwargs["created"]:

			Report.objects.create(report_overdue=True, report_recurring=True, report_missing=True, report_monthly=True, foruser_id=instance.id)
			UserProfile.objects.create(bio=None, image=None, user_id=instance.id)



@receiver(user_logged_in, dispatch_uid="unique")
def user_logged_in_(request, user, **kwargs):
    getlanguage = UserProfile.objects.filter(user_id=request.user.id).values_list('language', flat=True)[0]
    translation.activate(getlanguage)
    request.session[translation.LANGUAGE_SESSION_KEY] = getlanguage
    print(getlanguage)


@login_required
def logout(request):
	if request.user.is_authenticated:
		auth.logout(request)
		return redirect('dashboard')

@login_required
def deleteAccount(request):

	if request.user.is_authenticated:
		user = User.objects.get(pk=request.user.id)
		user.delete()
		auth.logout(request)
		return redirect('dashboard')

	return render(request, '/dashboard')


	