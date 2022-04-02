from django.db import models
from datetime import datetime
from users.models import UserProfile
from django.db.models import Q, Sum, Count
from dateutil.relativedelta import *


class BillType(models.Model):
	name = models.CharField(max_length=200)
	creator = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
	created_on = models.DateTimeField(default=datetime.now, blank=True)

	# Get latest overdue for a bill type
	def get_overdue(self):
		today = datetime.now()
		return self.bills.filter(due_date__lt=today).last()

	# Get all overdue for a bill type
	def get_all_overdue(self):
		today = datetime.now()
		return self.bills.filter(due_date__lt=today)

	# Get all due for a bill type
	def get_all_active(self):
		today = datetime.now()
		return self.bills.filter(Q(due_date__gte=today) & Q(paid=False))

	# Get latest due for a bill type
	def get_latest_current(self):
		today = datetime.now()
		return self.bills.filter(Q(due_date__gte=today) & Q(paid=False)).last()

	# Get latest overdue for a bill type
	def get_latest_overdue(self):
		today = datetime.now()
		return self.bills.filter(Q(due_date__lt=today) & Q(paid=False)).last()

	# Get overdue for a bill type
	def get_overdue_count(self):
		today = datetime.now()
		return self.bills.filter(Q(due_date__lt=today) & Q(paid=False), Q(month__month=today.month) | Q(due_date__month=today.month)).aggregate(Count('id'))['id__count'] or 0

	# Get due count for a bill type
	def get_due_count(self):
		today = datetime.now()
		return self.bills.filter(Q(paid=False) & Q(due_date__gte=today), Q(month__month=today.month) | Q(due_date__month=today.month)).aggregate(Count('id'))['id__count'] or 0

	# Get total for a bill type
	def get_billtype_total(self):
		today = datetime.now()
		return self.bills.filter(Q(paid=True), Q(month__month=today.month) | Q(due_date__month=today.month)).aggregate(Sum('amount'))['amount__sum'] or 0

	# Get previous month total for a bill type
	def get_prevmonth_total(self):
		today = datetime.now()
		previous_month = today + relativedelta(months=-1)
		previous_month = previous_month.month
		return self.bills.filter(Q(paid=True), Q(month__month=previous_month)).aggregate(Sum('amount'))['amount__sum'] or 0

	def __str__(self):
		return self.name