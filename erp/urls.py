from django.urls import path
from erp.views.dashboard.views import DashboardView
from erp.views.farm.views import *
from erp.views.crop.views import *
from erp.views.worker.views import *
from erp.views.activity.views import *
from erp.views.animal.views import *

app_name = 'erp'

urlpatterns = [
    # home
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    # farms
    path('farm/list/', FarmListView.as_view(), name='farm_list'),
    path('farm/add/', FarmCreateView.as_view(), name='farm_add'),
    path('farm/update/<int:pk>/', FarmUpdateView.as_view(), name='farm_edit'),
    path('farm/delete/<int:pk>/', FarmDeleteView.as_view(), name='farm_delete'),
    path('farm/detail/<int:pk>/', FarmDetailView.as_view(), name='farm_detail'),
    # crops
    path('farm/<int:pk>/crops/', CropListView.as_view(), name='crop_list'),
    path('farm/<int:pk>/crops/add/', CropCreateView.as_view(), name='crop_add'),
    path('crops/delete/<int:pk>/', CropDeleteView.as_view(), name='crop_delete'),
    path('crops/update/<int:pk>/', CropUpdateView.as_view(), name='crop_edit'),
    path('crops/detail/<int:pk>/', CropDetailView.as_view(), name='crop_detail'),
    # animals 
    path('farm/<int:pk>/animals/', AnimalListView.as_view(), name='animal_list'),
    path('farm/<int:pk>/animals/add/', AnimalCreateView.as_view(), name='animal_add'),
    path('animals/delete/<int:pk>/', AnimalDeleteView.as_view(), name='animal_delete'),
    path('animals/update/<int:pk>/', AnimalUpdateView.as_view(), name='animal_edit'),
    path('animals/detail/<int:pk>/', AnimalDetailView.as_view(), name='animal_detail'),
    # workers
    path('worker/list/', WorkerListView.as_view(), name='worker_list'),
    path('worker/add/', WorkerCreateView.as_view(), name='worker_add'),
    path('worker/delete/<int:pk>/', WorkerDeleteView.as_view(), name='worker_delete'),
    path('worker/update/<int:pk>/', WorkerUpdateView.as_view(), name='worker_edit'),
    # activitys
    path('crops/<int:pk>/activity/list/', ActivityListView.as_view(), name='activity_list'),
    path('crops/<int:pk>/activity/add/', ActivityCreateView.as_view(), name='activity_add'),
    path('activity/delete/<int:pk>/', ActivityDeleteView.as_view(), name='activity_delete'),
    path('activity/update/<int:pk>/', ActivityUpdateView.as_view(), name='activity_edit'),
    
]
