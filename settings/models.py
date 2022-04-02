from django.db import models
from django.contrib.auth.models import User

class Report(models.Model):
	foruser = models.ForeignKey(User, on_delete=models.CASCADE, related_name="foruser")
	report_overdue = models.BooleanField(default=True)
	report_recurring = models.BooleanField(default=True)
	report_missing = models.BooleanField(default=True)
	report_monthly = models.BooleanField(default=True)

	def __int__(self):
		return self.foruser.email
