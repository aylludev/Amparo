from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from erp.forms import FarmForm
from erp.mixins import ValidatePermissionRequiredMixin
from erp.models import Farm
from erp.services import get_departments

class FarmListView(LoginRequiredMixin, ListView):
    model = Farm
    template_name = 'farm/list.html'
    context_object_name = 'farms'

    def get_queryset(self):
        return Farm.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Clientes'
        context['create_url'] = reverse_lazy('erp:farm_list')
        context['list_url'] = reverse_lazy('erp:farm_list')
        context['entity'] = 'Fincas'
        return context


class FarmCreateView(LoginRequiredMixin, CreateView):
    model = Farm
    form_class = FarmForm
    template_name = 'farm/create.html'
    success_url = reverse_lazy('erp:dashboard')
    permission_required = 'add_farm'
    url_redirect = success_url
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación una Finca'
        context['entity'] = 'Fincas'
        context['action'] = 'add'
        return context


class FarmUpdateView(LoginRequiredMixin, UpdateView):
    model = Farm
    form_class = FarmForm
    template_name = 'farm/create.html'
    success_url = reverse_lazy('erp:farm_list')
    url_redirect = success_url

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición una Finca'
        context['entity'] = 'Fincas'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class FarmDeleteView(LoginRequiredMixin, DeleteView):
    model = Farm
    template_name = 'farm/delete.html'
    success_url = reverse_lazy('erp:farm_list')
    permission_required = 'delete_farm'
    url_redirect = success_url

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación de una Finca'
        context['entity'] = 'Fincas'
        context['list_url'] = self.success_url
        return context

