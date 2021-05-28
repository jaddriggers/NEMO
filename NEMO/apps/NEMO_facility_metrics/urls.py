from django.urls import path
from django.views.generic import TemplateView

from NEMO.apps.NEMO_facility_metrics import views

urlpatterns = [
	path('NEMO_facility_metrics', views.tool_usage, name='table'),
	path('NEMO_facility_metrics', views.user_usage, name='table2'),
	# Add your urls here.
]