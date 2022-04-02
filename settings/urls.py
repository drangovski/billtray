from django.urls import path

from . import views
from .views import PassChangeView

urlpatterns = [
	path('settings/', views.settings, name="settings"),
	path('settings/', PassChangeView.as_view(), name="password_change"),
]