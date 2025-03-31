from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import CreateView, DeleteView, UpdateView, ListView
from catalogs.forms import VarietyForm
from catalogs.models import CatalogVariety, CatalogCrop
from django.urls import reverse_lazy
from erp.mixins import ValidatePermissionRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

class VarietyListView(ListView):
    model = CatalogVariety
    template_name = "catalog_variety/list.html"
    context_object_name = "varieties"

    def get_queryset(self):
        crop = get_object_or_404(Crop, pk=self.kwargs["pk"])
        return CatalogVariety.objects.filter(crop=crop)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["crop"] = get_object_or_404(CatalogCrop, pk=self.kwargs["pk"])  # Pasamos el cultivo al template
        return context

class VarietyCreateView(LoginRequiredMixin, CreateView):
    model = CatalogVariety
    form_class = VarietyForm
    template_name = 'catalog_variety/create.html'
    success_url = reverse_lazy('catalogs:crop_list')
    permission_required = 'add_farm'
    
    def form_valid(self, form):
        data = {}
        try:
            variety = form.save(commit=False)  # No guardar aún
            crop = get_object_or_404(CatalogCrop, pk=self.kwargs["pk"])
            variety.crop = crop  
            variety.save()# Guardar el cultivo
        except Exception as e:
            data['error'] = str(e) 
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación una Variedad'
        context['action'] = 'add'
        return context

class VarietyUpdateView(LoginRequiredMixin, UpdateView):
    model = CatalogVariety
    form_class = VarietyForm
    template_name = 'catalog_variety/create.html'
    success_url = reverse_lazy('catalogs:crop_list')
    url_redirect = success_url

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición una Variedad'
        context['entity'] = 'Variedad'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context

class VarietyDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = CatalogVariety
    template_name = 'catalog_variety/delete.html'
    permission_required = 'delete_crop'
    success_url = reverse_lazy('catalogs:crop_list')

    def post(self, request, *args, **kwargs):
        data = {}
        if not request.user.has_perm(self.permission_required):
            return JsonResponse({'error': 'No tienes permiso para eliminar este cultivo.'}, status=403)
        try:
            self.object = self.get_object()
            self.object.delete()
            data['success_url'] = reverse_lazy('catalogs:crop_list')
        except Exception as e:
            data['error'] = str(e)
        return redirect(data['success_url'])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación de una Variedad'
        context['entity'] = 'Variedad'
        context['list_url'] = self.success_url
        return context

