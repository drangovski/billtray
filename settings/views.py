from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.models import User
from billtypes.models import BillType
from bills.models import Bill
from users.models import UserProfile
from .models import Report
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.db.models import Q
from .forms import settingsPersonal, settingsSecurity, settingsLocalization, settingsReport, settingsImage
from allauth.account.views import PasswordChangeView 
from django.utils import translation

class PassChangeView(PasswordChangeView):

    @property
    def success_url(self):
        print ('start')
        return '/settings/'


@login_required
def settings(request):


	# Change Image
	userprofileid = UserProfile.objects.get(user_id=request.user.id)

	newForm = settingsImage(instance=userprofileid)

	if request.method == 'POST' and 'settingsImage' in request.POST:
		newForm = settingsImage(request.POST, request.FILES, instance=userprofileid)
		if newForm.is_valid():
			newForm.save()
			return redirect('{}?tab=personal'.format(reverse('settings')))
		else:
			return redirect('dashboard')
	else:
		newForm = settingsImage(instance=userprofileid)



	user = request.user

	# Personal Settings
	form = settingsPersonal(instance=user)

	if request.method == 'POST' and 'settingsPersonal' in request.POST:
		form = settingsPersonal(request.POST, instance=user)
		if form.is_valid():
			form.save()
			return redirect('{}?tab=personal'.format(reverse('settings')))
		else:
			return redirect('settings')

	else:
		form = settingsPersonal(instance=user)


	# Security Settings
	changePassForm = settingsSecurity()	
	if request.method == 'POST' and 'settingsSecurity' in request.POST:
		changePassForm = settingsSecurity(data=request.POST, user=request.user)
		if changePassForm.is_valid():
			changePassForm.save()
			update_session_auth_hash(request, changePassForm.user)
			return redirect('{}?tab=security'.format(reverse('settings')))
		else:
			return redirect('dashboard')

	else:
		changePassForm = settingsSecurity()

	# Localization Settings
	userprofile = UserProfile.objects.get(user_id=request.user.id)

	localizationForm = settingsLocalization(instance=userprofile)
	if request.method == 'POST' and 'settingsLocalization' in request.POST:
		localizationForm = settingsLocalization(data=request.POST, instance=userprofile)
		if localizationForm.is_valid():
			localizationForm = localizationForm.save(commit=False)
			user_language = localizationForm.language
			localizationForm.save()
			
			translation.activate(user_language)
			request.session[translation.LANGUAGE_SESSION_KEY] = user_language

			return redirect('{}?tab=localization'.format(reverse('settings')))
		else:
			return redirect('dashboard')
	else:
		localizationForm = settingsLocalization(instance=userprofile)


	# Report Settings
	getuser = Report.objects.get(foruser_id=request.user.id) 

	reportsForm = settingsReport(instance=getuser)

	if request.method == 'POST' and 'settingsReport' in request.POST:
		reportsForm = settingsReport(request.POST, instance=getuser)
		if reportsForm.is_valid():
			reportsForm.save()
			return redirect('{}?tab=notifications'.format(reverse('settings')))
		else:
			return redirect('dashboard')
	else:
		reportsForm = settingsReport(instance=getuser)


	

	context = {
		'form': form,
		'user': user,
		'changePassForm': changePassForm,
		'localizationForm': localizationForm,
		'reportsForm': reportsForm,
		'newForm': newForm,
		'getuser': getuser,
	}


	return render(request, 'management/settings.html', context)