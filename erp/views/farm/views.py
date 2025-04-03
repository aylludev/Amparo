from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from erp.forms import FarmForm
from erp.models import Crop, Farm

class FarmListView(LoginRequiredMixin, ListView):
    model = Farm
    template_name = 'farm/list.html'
    context_object_name = 'farms'

    def get_queryset(self):
        return Farm.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Fincas'
        context['create_url'] = reverse_lazy('erp:farm_list')
        context['list_url'] = reverse_lazy('erp:farm_list')
        context['entity'] = 'Fincas'
        return context


class FarmCreateView(LoginRequiredMixin, CreateView):
    model = Farm
    form_class = FarmForm
    template_name = 'farm/create.html'
    success_url = reverse_lazy('erp:farm_list')
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
    url_redirect = success_url

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación de una Finca'
        context['entity'] = 'Fincas'
        context['list_url'] = self.success_url
        return context

class FarmDetailView(LoginRequiredMixin, DetailView):
    model = Farm
    template_name = 'farm/detail.html'
    context_object_name = 'farm'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        farm = self.get_object()
        context['crops'] = Crop.objects.filter(farm_id=farm)
        context['total_crops'] = len(context['crops'])
        return context

