from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import CreateView, DeleteView, UpdateView, ListView
from catalogs.forms import VarietyForm
from catalogs.models import Variety
from django.urls import reverse_lazy
from erp.mixins import ValidatePermissionRequiredMixin
from django.http import JsonResponse

class VarietyListView(LoginRequiredMixin, ListView):
    model = Variety
    template_name = 'catalog_variety/list.html'
    context_object_name = 'varieties'

class VarietyCreateView(LoginRequiredMixin, CreateView):
    model = Variety
    form_class = VarietyForm
    template_name = 'catalog_variety/create.html'
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
        context['title'] = 'Creación una Variedad'
        context['action'] = 'add'
        return context

class VarietyUpdateView(LoginRequiredMixin, UpdateView):
    model = Variety
    form_class = Variety
    template_name = 'catalog_variety/create.html'
    success_url = reverse_lazy('catalogs:variety_list')
    url_redirect = success_url

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición una Variedad'
        context['entity'] = 'Variedad'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context

class VarietyDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Variety
    template_name = 'catalog_variety/delete.html'
    permission_required = 'delete_crop'
    success_url = reverse_lazy('catalogs:variety_list')

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
        context['title'] = 'Eliminación de una Variedad'
        context['entity'] = 'Variedad'
        context['list_url'] = self.success_url
        return context

