from django.conf import settings
from django.db import models
from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect

from django.contrib.auth.models import User
from users.models import UserProfile
from settings.models import Report
from bills.models import Bill

from django.db.models import Q, Sum, Count
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags



def sendOverdueReport():
	today = datetime.now()

	users = User.objects.all()

	for user in users:
		report = user.foruser.values_list('report_overdue', flat=True)[0]

		if report == True:
			overdue_bills = Bill.objects.filter(Q(creator_id=user.id) & Q(due_date__lte=today) & Q(paid=False))
			overdue_count = Bill.objects.filter(Q(creator_id=user.id) & Q(due_date__lte=today) & Q(paid=False)).aggregate(Count('id'))['id__count'] or 0



			context = {
				'overdue_bills': overdue_bills,
				'overdue_count': overdue_count,
				'user': user,
			}

			subject = "Overdue Bills"
			html_message = render_to_string(settings.BASE_DIR + '/templates/reports/overdue-report.html', context)
			plain_message = strip_tags(html_message)
			from_email = 'test@profimak.mk'
			to = [user.email]

			send_mail(subject, plain_message, from_email, to, html_message=html_message)

