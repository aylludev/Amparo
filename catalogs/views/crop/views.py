from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import DetailView, CreateView, DeleteView, UpdateView, ListView
from catalogs.forms import CropForm
from catalogs.models import CatalogCrop, CatalogVariety, CatalogAgricultureActivity
from django.urls import reverse_lazy
from erp.mixins import ValidatePermissionRequiredMixin
from django.http import JsonResponse

class CropListView(LoginRequiredMixin, ListView):
    model = CatalogCrop
    template_name = 'catalog_crop/list.html'
    context_object_name = 'crops'

class CropCreateView(LoginRequiredMixin, CreateView):
    model = CatalogCrop
    form_class = CropForm
    template_name = 'catalog_crop/create.html'
    success_url = reverse_lazy('catalogs:crop_list')
    permission_required = 'add_farm'
    
    def form_valid(self, form):
        data = {}
        try:
            crop = form.save(commit=False)  # No guardar aún
            crop.save()  # Guardar el cultivo
        except Exception as e:
            data['error'] = str(e) 
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación un Cultivo'
        context['action'] = 'add'
        return context

class CropUpdateView(LoginRequiredMixin, UpdateView):
    model = CatalogCrop
    form_class = CropForm
    template_name = 'catalog_crop/create.html'
    success_url = reverse_lazy('erp:farm_list')
    url_redirect = success_url

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición un Cultivo'
        context['entity'] = 'Cultivo'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context

class CropDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = CatalogCrop
    template_name = 'catalog_crop/delete.html'
    permission_required = 'delete_crop'
    success_url = reverse_lazy('catalogs:crop_list')

    def post(self, request, *args, **kwargs):
        data = {}
        if not request.user.has_perm(self.permission_required):
            return JsonResponse({'error': 'No tienes permiso para eliminar este cultivo.'}, status=403)
        try:
            self.object = self.get_object()
            farm_id = self.object.farm.id
            self.object.delete()
            data['success_url'] = reverse_lazy('erp:crop_list', kwargs={'pk': farm_id})
        except Exception as e:
            data['error'] = str(e)
        return redirect(data['success_url'])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación de un Cultivo'
        context['entity'] = 'Cultivos'
        context['list_url'] = self.success_url
        return context

class CropDetailView(DetailView):
    model = CatalogCrop
    template_name = "catalog_crop/detail.html"
    context_object_name = "crop"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        crop = self.get_object()
        context["varieties"] = CatalogVariety.objects.filter(crop=crop)  # Lista de variedades del cultivo
        context["activities"] = CatalogAgricultureActivity.objects.filter(crop=crop)  # Lista de actividades del cultivo
        return context
        return context
