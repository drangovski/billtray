from django.urls import path

from . import views

urlpatterns = [
	path('delete-account/', views.deleteAccount, name="deleteAccount"),
	path('logout/', views.logout, name='logout'),
]