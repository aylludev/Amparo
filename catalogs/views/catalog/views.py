from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from catalogs.models import CatalogCrop

# Create your views here.
class DashboardView(LoginRequiredMixin, ListView):
    template_name = 'catalog/gestionar_cultivos.html'
    context_object_name = 'farms'
    
    def get_queryset(self):
        return CatalogCrop.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_farms'] = self.get_queryset().count()
        return context
