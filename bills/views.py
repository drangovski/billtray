from django.shortcuts import render, get_object_or_404, redirect
from .models import BillType, Bill
from billtray.forms import newBillForm, updateBillForm
from datetime import datetime, date
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Sum, Count
from django.db.models.functions import TruncMonth, ExtractMonth

###
###  Dashboard ###
###
@login_required
def dashboard(request):
	creator_id = request.user.userprofile.id
	today = datetime.now()

	# Sum calculations
	total_due = Bill.objects.filter(Q(creator_id=creator_id) & Q(paid=False) & Q(due_date__gte=today), Q(month__month=today.month) | Q(due_date__month=today.month)).aggregate(Sum('amount'))['amount__sum'] or 0
	total_paid = Bill.objects.filter(Q(creator_id=creator_id) & Q(paid=True), Q(month__month=today.month) | Q(due_date__month=today.month)).aggregate(Sum('amount'))['amount__sum'] or 0
	total_overdue = Bill.objects.filter(Q(creator_id=creator_id) & Q(due_date__lt=today) & Q(paid=False) & Q(month__month=today.month)).aggregate(Sum('amount'))['amount__sum'] or 0
	
	# Bills count
	overdue_count = Bill.objects.filter(Q(creator_id=creator_id) & Q(due_date__lt=today) & Q(paid=False), Q(month__month=today.month) | Q(due_date__month=today.month)).aggregate(Count('id'))['id__count'] or 0
	paid_count = Bill.objects.filter(Q(creator_id=creator_id) & Q(paid=True), Q(month__month=today.month) | Q(due_date__month=today.month)).aggregate(Count('id'))['id__count'] or 0
	due_count = Bill.objects.filter(Q(creator_id=creator_id) & Q(paid=False) & Q(due_date__gte=today), Q(month__month=today.month) | Q(due_date__month=today.month)).aggregate(Count('id'))['id__count'] or 0


	# Total sum calculation
	total = Bill.objects.filter(Q(creator_id=creator_id), Q(month__month=today.month) | Q(due_date__month=today.month)).aggregate(total=Sum('amount'))['total']

	if total_paid == None:
		total_paid = 0
		percentage = 0
	elif total == None:
		total = 0
		percentage = 0
	else:
		calculate_percentage =  total_paid / total
		percentage = calculate_percentage * 100

	# Billtype Due / Overdue count
	billtypes = BillType.objects.filter(creator_id=creator_id)


	context = {
		'total_due': total_due,
		'total_paid': total_paid,
		'total_overdue': total_overdue,
		'paid_count': paid_count, 
		'overdue_count': overdue_count,
		'percentage': percentage,
		'due_count': due_count,
		'billtypes': billtypes,
	}

	return render(request, 'management/dashboard.html', context)

###
###  Add New Bill  ###
###
@login_required
def newBill(request, bill_type_id):
	creator_id = request.user.userprofile.id
	if request.method == 'POST':
		# This is taking the entire row from BillType model and returning self.name 
		btid = get_object_or_404(BillType, pk=bill_type_id, creator_id=creator_id)

		form = newBillForm(request.POST)

		if form.is_valid():
			form = form.save(commit=False)
			# So here the pk would be selected from the entire row and assigned to form.bill_type_id
			form.bill_type_id = btid.pk
			form.creator_id = creator_id
			form.save()
			return redirect('newBill', bill_type_id=bill_type_id)
	else:
		form = newBillForm()

	bill_types = get_object_or_404(BillType, pk=bill_type_id, creator_id=creator_id)


	context = {
		'form':form,
		'bill_types': bill_types,
		'bill_type_id': bill_type_id,
	}

	return render(request, 'management/new-bill.html', context)

###
###  All Bills  ###
###
@login_required
def allBills(request, bill_type_id):

	# Get creator ID of the currentlu logged user
	creator_id = request.user.userprofile.id

	# Get all bill types by creator
	bill_type = get_object_or_404(BillType, pk=bill_type_id, creator_id=creator_id)

	# Overdue total sum calculations
	today = datetime.now()
	total_overdue = Bill.objects.filter(Q(bill_type_id=bill_type) & Q(creator_id=creator_id) & Q(due_date__lt=today) & Q(paid=False)).aggregate(Sum('amount'))['amount__sum'] or 0

	# Due total sum calculation
	today = datetime.now()
	total_due = Bill.objects.filter(Q(bill_type_id=bill_type) & Q(creator_id=creator_id) & Q(paid=False)).aggregate(Sum('amount'))['amount__sum'] or 0

	# Paid total sum calculation
	total_paid = Bill.objects.filter(Q(bill_type_id=bill_type) & Q(creator_id=creator_id) & Q(paid=True)).aggregate(Sum('amount'))['amount__sum'] or 0


	context = {
		'bill_type': bill_type,
		'total_overdue': total_overdue,
		'total_due': total_due,
		'total_paid': total_paid,
	}

	return render(request, 'management/all-bills.html', context)


# Remove Note for a Bill
@login_required
def removeNote(request, bill_id):
	creator_id = request.user.userprofile.id
	Bill.objects.filter(Q(pk=bill_id) & Q(creator_id=creator_id)).update(note="")

	getBill = get_object_or_404(Bill, pk=bill_id, creator_id=creator_id)
	bill_type_id = getBill.bill_type_id

	return redirect('allBills', bill_type_id=bill_type_id)


# Pay bill
@login_required
def payBill(request, bill_id):
	creator_id = request.user.userprofile.id
	pay = get_object_or_404(Bill, pk=bill_id, creator_id=creator_id)
	pay.paid_on = datetime.now()
	pay.paid = True
	pay.save()

	return redirect(request.META['HTTP_REFERER'])

# Undo bill
@login_required
def undoBill(request, bill_id):
	creator_id = request.user.userprofile.id
	undo = get_object_or_404(Bill, pk=bill_id, creator_id=creator_id)
	undo.paid_on = None
	undo.paid = False
	undo.save()

	return redirect(request.META['HTTP_REFERER'])	

# Update bill
@login_required
def updateBill(request, bill_id):
	creator_id = request.user.userprofile.id

	getBill = get_object_or_404(Bill, pk=bill_id, creator_id=creator_id)

	bill_type_id = getBill.bill_type_id

	form = updateBillForm(instance=getBill)
	
	if request.method == 'POST':
		form = updateBillForm(request.POST, instance=getBill)
		if form.is_valid():
			form.save()
			return redirect('allBills', bill_type_id=bill_type_id)
		else:
			return redirect('dasboard')

	else:
		form = updateBillForm(instance=getBill)


	context = {
		'form':form,
		'bill_type_id': bill_type_id,
		'bill_id': getBill.id
	}
	return render(request, 'management/update-bill.html', context)

# Delete bill
@login_required
def deleteBill(request, bill_id):
	creator_id = request.user.userprofile.id
	getBill = get_object_or_404(Bill, pk=bill_id, creator_id=creator_id)
	bill_type_id = getBill.bill_type_id

	getBill.delete()

	return redirect('allBills', bill_type_id=bill_type_id)


###
###  Billing Overview  ###
###
@login_required
def billingOverview(request):
	creator_id = request.user.userprofile.id
	billtypes = BillType.objects.filter(creator_id=creator_id).all()


	context = {
		'billtypes': billtypes
	}

	return render(request, 'management/billing-overview.html', context)