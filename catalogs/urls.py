from django.urls import path
from catalogs.views.catalog.views import *
from catalogs.views.crop.views import *
from catalogs.views.variety.views import *
from catalogs.views.activity.views import *
from catalogs.views.animal.views import *
from catalogs.views.race.views import *
from catalogs.views.aactivity.views import *
app_name = 'catalogs'

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    # crops
    path('crops/', CropListView.as_view(), name='crop_list'),
    path('crops/add/', CropCreateView.as_view(), name='crop_add'),
    path('crops/delete/<int:pk>/', CropDeleteView.as_view(), name='crop_delete'),
    path('crops/update/<int:pk>/', CropUpdateView.as_view(), name='crop_edit'),
    path('crop/<int:pk>/detail/', CropDetailView.as_view(), name='crop_detail'),
    # variety
    path('crop/<int:pk>/variety/add/', VarietyCreateView.as_view(), name='variety_add'),
    path('variety/delete/<int:pk>/', VarietyDeleteView.as_view(), name='variety_delete'),
    path('variety/update/<int:pk>/', VarietyUpdateView.as_view(), name='variety_edit'),
    # activity
    path('crop/<int:pk>/activity/add/', ActivityCreateView.as_view(), name='activity_add'),
    path('activity/delete/<int:pk>/', ActivityDeleteView.as_view(), name='activity_delete'),
    path('activity/update/<int:pk>/', ActivityUpdateView.as_view(), name='activity_edit'),
    # animal 
    path('animals/', AnimalListView.as_view(), name='animal_list'),
    path('animals/add/', AnimalCreateView.as_view(), name='animal_add'),
    path('animals/delete/<int:pk>/', AnimalDeleteView.as_view(), name='animal_delete'),
    path('animals/update/<int:pk>/', AnimalUpdateView.as_view(), name='animal_edit'),
    path('animals/<int:pk>/detail/', AnimalDetailView.as_view(), name='animal_detail'),
    # variety
    path('animal/<int:pk>/race/add/', RaceCreateView.as_view(), name='race_add'),
    path('race/delete/<int:pk>/', RaceDeleteView.as_view(), name='race_delete'),
    path('race/update/<int:pk>/', RaceUpdateView.as_view(), name='race_edit'),
    # activitya 
    path('animal/<int:pk>/activity/add/', ActivityAnCreateView.as_view(), name='activityan_add'),
    path('activityan/delete/<int:pk>/', ActivityAnDeleteView.as_view(), name='activityan_delete'),
    path('activityan/update/<int:pk>/', ActivityAnUpdateView.as_view(), name='activityan_edit'),
]
