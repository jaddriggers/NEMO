from django.urls import path
from django.views.generic import TemplateView

from NEMO.apps.NEMO_facility_metrics import views

urlpatterns = [
	path('NEMO_facility_metrics', views.metrics, name='facility_metrics'),

]