from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import DetailView, CreateView, DeleteView, UpdateView, ListView
from catalogs.forms import AnimalForm
from catalogs.models import CatalogAnimal, CatalogRace, CatalogAnimalActivity
from django.urls import reverse_lazy
from erp.mixins import ValidatePermissionRequiredMixin
from django.http import JsonResponse

class AnimalListView(LoginRequiredMixin, ListView):
    model = CatalogAnimal
    template_name = 'catalog_animal/list.html'
    context_object_name = 'crops'

class AnimalCreateView(LoginRequiredMixin, CreateView):
    model = CatalogAnimal
    form_class = AnimalForm
    template_name = 'catalog_animal/create.html'
    success_url = reverse_lazy('catalogs:dashboard')
    permission_required = 'add_farm'
    
    def form_valid(self, form):
        data = {}
        try:
            animal = form.save(commit=False)  # No guardar aún
            animal.save()  # Guardar el cultivo
        except Exception as e:
            data['error'] = str(e) 
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Registro de un Animal'
        context['action'] = 'add'
        return context

class AnimalUpdateView(LoginRequiredMixin, UpdateView):
    model = CatalogAnimal
    form_class = AnimalForm
    template_name = 'catalog_animal/create.html'
    success_url = reverse_lazy('erp:farm_list')
    url_redirect = success_url

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición un Animal'
        context['entity'] = 'Animal'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context

class AnimalDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = CatalogAnimal
    template_name = 'catalog_animal/delete.html'
    permission_required = 'delete_crop'
    success_url = reverse_lazy('catalogs:farm_list')

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
        context['title'] = 'Eliminación de un Animal'
        context['entity'] = 'Animal'
        context['list_url'] = self.success_url
        return context

class AnimalDetailView(DetailView):
    model = CatalogAnimal
    template_name = "catalog_animal/detail.html"
    context_object_name = "crop"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        crop = self.get_object()
        context["varieties"] = CatalogRace.objects.filter(crop=crop)  # Lista de variedades del cultivo
        context["activities"] = CatalogAnimalActivity.objects.filter(crop=crop)  # Lista de actividades del cultivo
        return context
