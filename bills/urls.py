from django.urls import path

from . import views

urlpatterns = [
	# path('new-bill/', views.newBill, name="newBill"),
	path('dashboard/', views.dashboard, name="dashboard"),

	path('new-bill/<bill_type_id>', views.newBill, name="newBill"),
	path('billing-overview/', views.billingOverview, name="billingOverview"),
	path('all-bills/<bill_type_id>', views.allBills, name="allBills"),

	path('pay/<bill_id>', views.payBill, name="payBill"),
	path('undo/<bill_id>', views.undoBill, name="undoBill"),
	path('update-bill/<bill_id>', views.updateBill, name="updateBill"),
	path('delete/bill/<bill_id>', views.deleteBill, name="deleteBill"),

	path('remove/note/<bill_id>', views.removeNote, name="removeNote"),

]