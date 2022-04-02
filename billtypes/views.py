from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from .models import BillType, UserProfile
from django.contrib.auth.decorators import login_required
from django.db.models import Q
	
@login_required
def billTypes(request):
	creator_id = request.user.userprofile.id
	if request.method == 'POST' and 'createBillType' in request.POST:
		billingTypeName = request.POST['billingTypeName']

		if BillType.objects.filter(Q(name=billingTypeName) & Q(creator_id=creator_id)).exists():
			messages.error(request, 'That billing type already exists.')
			return redirect('billTypes')
		else:
			billType = BillType.objects.create(name=billingTypeName, creator_id=creator_id)


	if request.method == 'POST' and 'updateBillType' in request.POST:
		updatedBillingTypeName = request.POST['updatedBillingTypeName']
		object_id = request.POST.get('billTypeId')
		billType = get_object_or_404(BillType, id=object_id, creator_id=creator_id)

		if BillType.objects.filter(Q(name=updatedBillingTypeName) & Q(creator_id=creator_id)).exists():
			messages.error(request, 'That billing type name already exist.')
		else:
			billType.name = updatedBillingTypeName
			billType.save()
			return redirect('billTypes')

	bill_types = BillType.objects.filter(creator_id=creator_id).all()

	context = {
		'bill_types': bill_types,
		'creator_id': creator_id
	}

	return render(request, 'management/billing-types.html', context)

@login_required
def deleteBillType(request, object_id):
	creator_id = request.user.userprofile.id
	billType = get_object_or_404(BillType, pk=object_id, creator_id=creator_id)
	billType.delete()
	return redirect('billTypes')

