from django.urls import path
from erp.views.dashboard.views import DashboardView
from erp.views.farm.views import *
from erp.views.crop.views import *
from erp.views.worker.views import *
from erp.views.activity.views import *
from erp.views.animal.views import *
from erp.views.activityanimal.views import *
from erp.views.category.views import *
from erp.views.client.views import *
from erp.views.dashboard.views import *
from erp.views.product.views import *
from erp.views.sale.views import *
from erp.views.cotization.view import *
from erp.views.tests.views import TestView
from erp.views.credit.view import *
from erp.views.suply.views import *
from erp.views.equipment.views import *

app_name = 'erp'

urlpatterns = [
    # home
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('reports/', ReportView.as_view(), name='reports'),
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
    path('farm/<int:farm_pk>/crops/update/<int:pk>/', CropUpdateView.as_view(), name='crop_edit'),
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
    # suply
    path('suply/list/', SuplyListView.as_view(), name='suply_list'),
    path('suply/add/', SuplyCreateView.as_view(), name='suply_create'),
    path('suply/update/<int:pk>/', SuplyUpdateView.as_view(), name='suply_update'),
    path('suply/delete/<int:pk>/', SuplyDeleteView.as_view(), name='suply_delete'),
    # equipment
    path('equipment/list/', EquipmentListView.as_view(), name='equipment_list'),
    path('equipment/add/', EquipmentCreateView.as_view(), name='equipment_create'),
    path('equipment/update/<int:pk>/', EquipmentUpdateView.as_view(), name='equipment_update'),
    path('equipment/delete/<int:pk>/', EquipmentDeleteView.as_view(), name='equipment_delete'),
    # activitys
    path('crops/<int:pk>/activity/list/', CropDetailView.as_view(), name='activity_list'),
    path('crops/<int:pk>/activity/add/', ActivityCreateView.as_view(), name='activity_add'),
    path('activity/delete/<int:pk>/', ActivityDeleteView.as_view(), name='activity_delete'),
    path('activity/update/<int:pk>/', ActivityUpdateView.as_view(), name='activity_edit'),
    # activityanimal
    path('animal/<int:pk>/activity/list/', ActivityAnimalListView.as_view(), name='activityanimal_list'),
    path('animal/<int:pk>/activity/add/', ActivityAnimalCreateView.as_view(), name='activityanimal_add'),
    path('activityanimal/delete/<int:pk>/', ActivityAnimalDeleteView.as_view(), name='activityanimal_delete'),
    path('activityanimal/update/<int:pk>/', ActivityAnimalUpdateView.as_view(), name='activityanimal_edit'),
    # category
    path('category/list/', CategoryListView.as_view(), name='category_list'),
    path('category/add/', CategoryCreateView.as_view(), name='category_create'),
    path('category/update/<int:pk>/', CategoryUpdateView.as_view(), name='category_update'),
    path('category/delete/<int:pk>/', CategoryDeleteView.as_view(), name='category_delete'),
    # client
    path('client/list/', ClientListView.as_view(), name='client_list'),
    path('client/add/', ClientCreateView.as_view(), name='client_create'),
    path('client/update/<int:pk>/', ClientUpdateView.as_view(), name='client_update'),
    path('client/delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),
    # product
    path('product/list/', ProductListView.as_view(), name='product_list'),
    path('product/add/', ProductCreateView.as_view(), name='product_create'),
    path('product/update/<int:pk>/', ProductUpdateView.as_view(), name='product_update'),
    path('product/delete/<int:pk>/', ProductDeleteView.as_view(), name='product_delete'),
    # home
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    # test
    path('test/', TestView.as_view(), name='test'),
    # sale
    path('sale/list/', SaleListView.as_view(), name='sale_list'),
    path('sale/add/', SaleCreateView.as_view(), name='sale_create'),
    path('sale/delete/<int:pk>/', SaleDeleteView.as_view(), name='sale_delete'),
    path('sale/update/<int:pk>/', SaleUpdateView.as_view(), name='sale_update'),
    path('sale/invoice/pdf/<int:pk>/', SaleInvoicePdfView.as_view(), name='sale_invoice_pdf'),
    # cotization
    path('cotization/list/', CotizationListView.as_view(), name='cotization_list'),
    path('cotization/add/', CotizationCreateView.as_view(), name='cotization_create'),
    path('cotization/delete/<int:pk>/', CotizationDeleteView.as_view(), name='cotization_delete'),
    path('cotization/update/<int:pk>/', CotizationUpdateView.as_view(), name='cotization_update'),
    path('cotization/invoice/pdf/<int:pk>/', CotizationInvoicePdfView.as_view(), name='cotization_invoice_pdf'),
    # credit 
    path('credit/list/', CreditSaleListView.as_view(), name='credit_list'),
    path('credit/payment/<int:pk>/', CreditPaymentView.as_view(), name='credit_payment')
]
