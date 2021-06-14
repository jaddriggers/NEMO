from django.urls import path
from django.views.generic import TemplateView

from NEMO.apps.NEMO_facility_metrics import views

urlpatterns = [
	path('facility_metrics/', views.metrics, name='facility_metrics'),
	path('facility_metrics/user_usage/', views.user_metrics, name='user_metrics'),

]