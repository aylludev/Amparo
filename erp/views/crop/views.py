from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from erp.models import Farm, Crop, Activity

class FarmDetailView(LoginRequiredMixin, DetailView):
    model = Farm
    template_name = 'farm_detail.html'
    context_object_name = 'farm'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        farm = self.get_object()
        context['cultivos'] = Crop.objects.filter(finca=farm)
        context['actividades'] = Activity.objects.filter(cultivo__finca=farm)
        return context
