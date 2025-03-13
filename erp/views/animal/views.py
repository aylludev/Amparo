from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import DetailView, CreateView, DeleteView, UpdateView
from erp.forms import AnimalForm
from erp.models import Activity, Animal, Farm, Crop
from django.urls import reverse_lazy
from erp.mixins import ValidatePermissionRequiredMixin
from django.http import JsonResponse

class AnimalListView(LoginRequiredMixin, DetailView):
    model = Animal
    template_name = 'animal/list.html'
    context_object_name = 'farm'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        farm = self.get_object()
        context['animals'] = Animal.objects.filter(farm_id=farm)
        return context

class AnimalCreateView(LoginRequiredMixin, CreateView):
    model = Animal
    form_class = AnimalForm
    template_name = 'animal/create.html'
    success_url = reverse_lazy('erp:farm_list')
    permission_required = 'add_farm'
    
    def form_valid(self, form):
        data = {}
        try:
            farm_id = self.kwargs.get('pk')  # Obtener el ID de la finca desde la URL
            if not farm_id:
                raise ValueError("No se ha proporcionado un ID de finca válido.")
            farm = Farm.objects.get(id=farm_id)  # Buscar la finca en la BD
            animal = form.save(commit=False)  # No guardar aún
            animal.farm = farm  # Asignar la finca al cultivo
            animal.save()  # Guardar el cultivo
        except Exception as e:
            data['error'] = str(e) 
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación un Cultivo'
        context['entity'] = 'Fincas'
        farm_id = self.kwargs.get('pk')
        context['farm'] = Farm.objects.get(id=farm_id)
        context['action'] = 'add'
        return context

class AnimalUpdateView(LoginRequiredMixin, UpdateView):
    model = Animal
    form_class = AnimalForm
    template_name = 'animal/create.html'
    success_url = reverse_lazy('erp:self_list')
    url_redirect = success_url

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición un Animal'
        context['entity'] = 'Animal'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context

class AnimalDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Animal
    template_name = 'animal/delete.html'
    permission_required = 'delete_crop'

    def post(self, request, *args, **kwargs):
        data = {}
        if not request.user.has_perm(self.permission_required):
            return JsonResponse({'error': 'No tienes permiso para eliminar este animal.'}, status=403)
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
        context['entity'] = 'Animales'
        context['list_url'] = self.success_url 
        return context

class AnimalDetailView(LoginRequiredMixin, DetailView):
    model = Animal 
    template_name = 'activity/list.html'
    context_object_name = 'animal'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        animal = self.get_object()
        context['activitys'] = Activity.objects.filter(animal_id=animal)
        context['total_activitys'] = len(context['activitys'])
        return context
