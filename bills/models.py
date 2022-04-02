from django.db import models
from datetime import datetime
from billtypes.models import BillType
from users.models import UserProfile

class Bill(models.Model):
	bill_type = models.ForeignKey(BillType, on_delete=models.CASCADE, related_name='bills')
	creator = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='billcreator')
	month = models.DateField(blank=True)
	amount = models.IntegerField()
	due_date = models.DateField(blank=True)
	note = models.TextField(blank=True)
	recurring = models.BooleanField(default=False)
	currency = models.CharField(max_length=100)
	paid = models.BooleanField(default=False)
	paid_on = models.DateField(null=True, blank=True)
	created_on = models.DateField(default=datetime.now, blank=True)

	def __date__(self):
		return self.month