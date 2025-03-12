from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from erp.models import Farm

# Create your views here.
class DashboardView(LoginRequiredMixin, ListView):
    template_name = 'dashboard.html'
    model = Farm
    context_object_name = 'farms'
    
    def get_queryset(self):
        return Farm.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_farms'] = self.get_queryset().count()
        return context
