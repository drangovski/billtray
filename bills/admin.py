from django.contrib import admin

from .models import Bill

class BillAdmin(admin.ModelAdmin):
	list_display = ('month', 'bill_type', 'amount', 'recurring', 'paid', 'creator_id')


admin.site.register(Bill, BillAdmin)