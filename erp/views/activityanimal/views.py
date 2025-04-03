from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import DetailView, CreateView, DeleteView, UpdateView
from erp.forms import ActivityAnimalForm, CropForm
from erp.models import Animal, ActivityAnimal
from django.urls import reverse_lazy
from erp.mixins import ValidatePermissionRequiredMixin
from django.http import JsonResponse

class ActivityAnimalListView(LoginRequiredMixin, DetailView):
    model = ActivityAnimal
    template_name = 'activityanimal/list.html'
    context_object_name = 'activity'

    def get_queryset(self):
        crop_id = self.kwargs.get('pk')
        return ActivityAnimal.objects.filter(crop=crop_id)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        crop = self.get_object()
        context['activity'] = ActivityAnimal.objects.filter(farm_id=crop)
        return context

class ActivityAnimalCreateView(LoginRequiredMixin, CreateView):
    model = ActivityAnimal
    form_class = ActivityAnimalForm
    template_name = 'activityanimal/create.html'
    success_url = reverse_lazy('erp:farm_list')
    permission_required = 'add_farm'
    
    def form_valid(self, form):
        data = {}
        try:
            crop_id = self.kwargs.get('pk')  # Obtener el ID de la finca desde la URL
            if not crop_id:
                raise ValueError("No se ha proporcionado un ID de finca válido.")
            crop = Animal.objects.get(id=crop_id)  # Buscar la finca en la BD
            activity = form.save(commit=False)  # No guardar aún
            activity.crop = crop  # Asignar la finca al cultivo
            activity.save()  # Guardar el cultivo
        except Exception as e:
            data['error'] = str(e) 
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación de una Actividad'
        context['entity'] = 'Fincas'
        context['action'] = 'add'
        return context

class ActivityAnimalUpdateView(LoginRequiredMixin, UpdateView):
    model = ActivityAnimal
    form_class = ActivityAnimalForm
    template_name = 'activityanimal/create.html'
    success_url = reverse_lazy('erp:farm_list')
    url_redirect = success_url

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición una Actividad'
        context['entity'] = 'Cultivo'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context

class ActivityAnimalDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = ActivityAnimal
    template_name = 'activityanimal/delete.html'
    permission_required = 'delete_activity'

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
        context['title'] = 'Eliminación de una Actividad'
        context['entity'] = 'Actividad'
        context['list_url'] = self.success_url
        return context
