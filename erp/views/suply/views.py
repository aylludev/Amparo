from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from erp.forms import SuplyForm
from erp.mixins import ValidatePermissionRequiredMixin
from erp.models import Suply

class SuplyListView(LoginRequiredMixin, ListView):
    model = Suply
    template_name = 'suply/list.html'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Suply.objects.filter(user=request.user):
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Insumos'
        context['create_url'] = reverse_lazy('erp:suply_create')
        context['list_url'] = reverse_lazy('erp:suply_list')
        context['entity'] = 'Insumos'
        return context

class SuplyCreateView(LoginRequiredMixin, CreateView):
    model = Suply
    form_class = SuplyForm
    template_name = 'suply/create.html'
    success_url = reverse_lazy('erp:suply_list')
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                form.instance.user = self.request.user
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación de un Insumo'
        context['entity'] = 'Insumos'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context

class SuplyUpdateView(LoginRequiredMixin, UpdateView):
    model = Suply
    form_class = SuplyForm
    template_name = 'suply/create.html'
    success_url = reverse_lazy('erp:suply_list')
    permission_required = 'change_product'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición de un Insumo'
        context['entity'] = 'Insumos'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class SuplyDeleteView(LoginRequiredMixin, DeleteView):
    model = Suply
    template_name = 'suply/delete.html'
    success_url = reverse_lazy('erp:suply_list')
    permission_required = 'delete_product'
    url_redirect = success_url

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación de un Insumo'
        context['entity'] = 'Insumos'
        context['list_url'] = self.success_url
        return context
