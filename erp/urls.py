from django.urls import path
from erp.views.dashboard.views import DashboardView
from erp.views.finca.views import *

app_name = 'erp'

urlpatterns = [
    # home
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    # client
    path('farm/list/', ClientListView.as_view(), name='client_list'),
    path('farm/add/', ClientCreateView.as_view(), name='client_create'),
    path('farm/update/<int:pk>/', ClientUpdateView.as_view(), name='client_update'),
    path('farm/delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),
]
