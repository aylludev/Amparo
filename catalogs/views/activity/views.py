from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import CreateView, DeleteView, UpdateView, ListView
from catalogs.forms import ActivityForm 
from catalogs.models import CatalogAgricultureActivity, CatalogCrop 
from django.urls import reverse_lazy
from erp.mixins import ValidatePermissionRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

class ActivityCreateView(LoginRequiredMixin, CreateView):
    model = CatalogAgricultureActivity
    form_class = ActivityForm
    template_name = 'catalog_activity/create.html'
    success_url = reverse_lazy('catalogs:crop_list')
    permission_required = 'add_farm'
    
    def form_valid(self, form):
        data = {}
        try:
            activity = form.save(commit=False)  # No guardar aún
            crop = get_object_or_404(CatalogCrop, pk=self.kwargs["pk"])
            activity.crop = crop  
            activity.save()# Guardar el cultivo
        except Exception as e:
            data['error'] = str(e) 
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación una Actividad'
        context['action'] = 'add'
        return context

class ActivityUpdateView(LoginRequiredMixin, UpdateView):
    model = CatalogAgricultureActivity
    form_class = ActivityForm
    template_name = 'catalog_activity/create.html'
    success_url = reverse_lazy('catalogs:crop_list')
    url_redirect = success_url

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición una Variedad'
        context['entity'] = 'Actividad'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context

class ActivityDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = CatalogAgricultureActivity
    template_name = 'catalog_activity/delete.html'
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
        context['title'] = 'Eliminación de una Actividad'
        context['entity'] = 'Actividad'
        context['list_url'] = self.success_url
        return context

