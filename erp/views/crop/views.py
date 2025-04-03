from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import DetailView, CreateView, DeleteView, UpdateView
from erp.forms import CropForm
from erp.models import Activity, Farm, Crop
from django.urls import reverse_lazy, reverse
from erp.mixins import ValidatePermissionRequiredMixin
from django.http import JsonResponse

class CropListView(LoginRequiredMixin, DetailView):
    model = Farm
    template_name = 'crop/list.html'
    context_object_name = 'farm'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        farm = self.get_object()
        context['crops'] = Crop.objects.filter(farm_id=farm)
        return context

class CropCreateView(LoginRequiredMixin, CreateView):
    model = Crop
    form_class = CropForm
    template_name = 'crop/create.html'
    permission_required = 'add_farm'
    
    def form_valid(self, form):
        data = {}
        try:
            farm_id = self.kwargs.get('pk')  # Obtener el ID de la finca desde la URL
            if not farm_id:
                raise ValueError("No se ha proporcionado un ID de finca válido.")
            farm = Farm.objects.get(id=farm_id)  # Buscar la finca en la BD
            crop = form.save(commit=False)  # No guardar aún
            crop.farm = farm  # Asignar la finca al cultivo
            crop.save()  # Guardar el cultivo
        except Exception as e:
            data['error'] = str(e) 
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('erp:crop_list', kwargs={'pk': self.kwargs.get('pk')})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación un Cultivo'
        context['entity'] = 'Fincas'
        farm_id = self.kwargs.get('pk')
        context['farm'] = Farm.objects.get(id=farm_id)
        context['list_url'] = reverse_lazy('erp:crop_list', kwargs={'pk': self.kwargs.get('pk')})
        context['action'] = 'add'
        return context

class CropUpdateView(LoginRequiredMixin, UpdateView):
    model = Crop
    form_class = CropForm
    template_name = 'crop/create.html'
    
    def get_success_url(self):
        return reverse('erp:crop_list', kwargs={'pk': self.object.farm.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición un Cultivo'
        context['entity'] = 'Cultivo'
        context['list_url'] = reverse_lazy('erp:crop_list', kwargs={'pk': self.object.farm.pk})
        context['action'] = 'edit'
        return context

class CropDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Crop
    template_name = 'farm/delete.html'
    permission_required = 'delete_crop'

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
        context['title'] = 'Eliminación de un Cultivo'
        context['entity'] = 'Cultivos'
        context['list_url'] = self.success_url
        return context

class CropDetailView(LoginRequiredMixin, DetailView):
    model = Crop
    template_name = 'activity/list.html'
    context_object_name = 'crop'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        crop = self.get_object()
        context['activitys'] = Activity.objects.filter(crop_id=crop)
        context['total_activitys'] = len(context['activitys'])
        context['create_url'] = reverse_lazy('erp:activity_add', kwargs={'pk': self.object.pk})
        return context
