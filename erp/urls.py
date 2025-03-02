from django.urls import path
from erp.views.dashboard.views import DashboardView
from erp.views.farm.views import *

app_name = 'erp'

urlpatterns = [
    # home
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    # client
    path('farm/list/', FarmListView.as_view(), name='farm_list'),
    path('farm/add/', FarmCreateView.as_view(), name='farm_add'),
    path('farm/update/<int:pk>/', FarmUpdateView.as_view(), name='farm_edit'),
    path('farm/delete/<int:pk>/', FarmDeleteView.as_view(), name='farm_delete'),
]
