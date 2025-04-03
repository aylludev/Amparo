from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from erp.forms import EquipmentForm
from erp.models import Equipment

class EquipmentListView(LoginRequiredMixin, ListView):
    model = Equipment
    template_name = 'equipment/list.html'
    context_object_name = 'equipments'
    
    def get_queryset(self):
        return Equipment.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Equipos'
        context['create_url'] = reverse_lazy('erp:equipment_list')
        context['list_url'] = reverse_lazy('erp:equipment_list')
        context['entity'] = 'Equipos'
        return context

class EquipmentCreateView(LoginRequiredMixin, CreateView):
    model = Equipment
    form_class = EquipmentForm
    template_name = 'equipment/create.html'

    def get_success_url(self):
        return reverse_lazy('erp:equipment_list')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación de un Equipo'
        context['entity'] = 'Equipos'
        context['action'] = 'add'
        return context

class EquipmentUpdateView(LoginRequiredMixin, UpdateView):
    model = Equipment
    form_class = EquipmentForm
    template_name = 'equipment/create.html'
    success_url = reverse_lazy('erp:equipment_list')
    url_redirect = success_url
    
    def get_success_url(self):
        return reverse_lazy('erp:equipment_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición un Equipo'
        context['entity'] = 'Equipos'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class EquipmentDeleteView(LoginRequiredMixin, DeleteView):
    model = Equipment
    template_name = 'equipment/delete.html'
    success_url = reverse_lazy('erp:equipment_list')
    permission_required = 'delete_worker'
    url_redirect = success_url

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación de un Equipo'
        context['entity'] = 'Equipos'
        context['list_url'] = self.success_url
        return context

