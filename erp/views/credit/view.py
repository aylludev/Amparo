from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from erp.mixins import ValidatePermissionRequiredMixin
from erp.models import CreditSale, CreditPayment
from erp.forms import CreditPaymentForm
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction

class CreditSaleListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = CreditSale
    template_name = 'credit/list.html'
    context_object_name = 'credits'
    
    def get_queryset(self):
        return CreditSale.objects.filter(total_credit__gt=0).select_related('sale').order_by('-id')

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST.get('action', None)
            if action == 'searchdata':
                data = [credit.toJSON() for credit in CreditSale.objects.all()]
            else:
                data['error'] = 'Acción no válida'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Créditos'
        context['create_url'] = reverse_lazy('erp:credit_list')
        context['list_url'] = reverse_lazy('erp:credit_list')
        context['entity'] = 'Créditos'
        return context

class CreditPaymentView(LoginRequiredMixin, CreateView):
    template_name = 'credit/create.html'
    form_class = CreditPaymentForm
    success_url = reverse_lazy('erp:credit_list')

    def form_valid(self, form):
        credit = get_object_or_404(CreditSale, pk=self.kwargs['pk'])
        amount = form.cleaned_data['amount']

        if amount <= 0:
            form.add_error('amount', "El monto debe ser mayor a 0")
            return self.form_invalid(form)

        if amount > credit.total_credit - credit.down_payment:
            form.add_error('amount', "El monto excede el saldo pendiente")
            return self.form_invalid(form)

        with transaction.atomic():
            # Registrar el pago
            payment = form.save(commit=False)
            payment.credit = credit
            payment.save()

            # Actualizar el crédito
            credit.down_payment += amount
            credit.save()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        credit = get_object_or_404(CreditSale, pk=self.kwargs['pk'])
        context['pending_balance'] = float(credit.total_credit) - float(credit.total_paid())
        context['credit'] = credit
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['payments'] = credit.payments.all()
        return context
