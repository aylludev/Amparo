from django.urls import path
from catalogs.models import Variety
from catalogs.views.catalog.views import *
from catalogs.views.crop.views import *
from catalogs.views.variety.views import *
app_name = 'catalogs'

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    # crops
    path('crops/', CropListView.as_view(), name='crop_list'),
    path('crops/add/', CropCreateView.as_view(), name='crop_add'),
    path('crops/delete/<int:pk>/', CropDeleteView.as_view(), name='crop_delete'),
    path('crops/update/<int:pk>/', CropUpdateView.as_view(), name='crop_edit'),
    # variety
    path('variety/', VarietyListView.as_view(), name='variety_list'),
    path('variety/add/', VarietyCreateView.as_view(), name='variety_add'),
    path('variety/delete/<int:pk>/', VarietyDeleteView.as_view(), name='variety_delete'),
    path('variety/update/<int:pk>/', VarietyUpdateView.as_view(), name='variety_edit'),
]
