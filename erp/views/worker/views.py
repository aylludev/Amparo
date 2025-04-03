from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from erp.forms import WorkerForm
from erp.mixins import ValidatePermissionRequiredMixin
from erp.models import Worker

class WorkerListView(LoginRequiredMixin, ListView):
    model = Worker
    template_name = 'worker/list.html'
    context_object_name = 'workers'
    
    def get_queryset(self):
        return Worker.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Trabajadores'
        context['create_url'] = reverse_lazy('erp:farm_list')
        context['list_url'] = reverse_lazy('erp:farm_list')
        context['entity'] = 'Trabajadores'
        return context


class WorkerCreateView(LoginRequiredMixin, CreateView):
    model = Worker
    form_class = WorkerForm
    template_name = 'worker/create.html'
    success_url = reverse_lazy('erp:worker_list')
    permission_required = 'add_farm'
    url_redirect = success_url
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación una Trabajador'
        context['entity'] = 'Trabajador'
        context['action'] = 'add'
        return context


class WorkerUpdateView(LoginRequiredMixin, UpdateView):
    model = Worker
    form_class = WorkerForm
    template_name = 'farm/create.html'
    success_url = reverse_lazy('erp:worker_list')
    url_redirect = success_url

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición un Trabajador'
        context['entity'] = 'Trabajadores'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class WorkerDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Worker
    template_name = 'worker/delete.html'
    success_url = reverse_lazy('erp:worker_list')
    permission_required = 'delete_worker'
    url_redirect = success_url

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación de un Trabajador'
        context['entity'] = 'Trabajador'
        context['list_url'] = self.success_url
        return context

