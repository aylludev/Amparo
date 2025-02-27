from django.urls import path
from erp.views.dashboard.views import DashboardView

app_name = 'erp'

urlpatterns = [
    # home
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
]
