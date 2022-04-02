from django.urls import path

from . import views

urlpatterns = [
	path('billing-types/', views.billTypes, name="billTypes"),
	path('delete/bill-type/<object_id>', views.deleteBillType, name="deleteBillType"),
]