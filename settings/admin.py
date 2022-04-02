from django.contrib import admin

from .models import Report

class ReportAdmin(admin.ModelAdmin):
	list_display = ('report_overdue', 'report_recurring', 'report_missing', 'report_monthly', 'foruser_id')


admin.site.register(Report, ReportAdmin)