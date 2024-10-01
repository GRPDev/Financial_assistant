from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.views.generic import CreateView, TemplateView, View, ListView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from .models import History
from .forms import CreateUserForm
import requests
from django.db.models import Sum
from django.http import HttpResponse
import json

def logout_view(request):
    logout(request)
    return redirect('login') 

def getBalance(user):
    deposit_sum = user.history.filter(type='deposit', status='success').aggregate(depo_sum=Sum('amount'))['depo_sum'] or 0
    withdraw_sum = user.history.filter(type='withdraw', status='success').aggregate(withd_sum=Sum('amount'))['withd_sum'] or 0
    balance = float(deposit_sum) - float(abs(withdraw_sum))
    return balance
   
def getCurrencyParams():
    url = "https://fake-api.apps.berlintech.ai/api/currency_exchange" #input()
    response = requests.get(url)
    if response.status_code == 200:
        lista = []
        """ rates = json.loads(response.text) """ #should work, but doesnt due test
        rates = response.json()
        for key, value in rates.items():
            lista.append((key, f'{key} ({value})'))
        return rates, lista
    else:
        lista = [None, None] 
        return lista

class CreateUserView(CreateView):
    model = User
    template_name = 'app/create_account.html'
    success_url = reverse_lazy('login')
    form_class = CreateUserForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['username'] = self.request.user.username
        return context

class CustomLoginView(LoginView):
    template_name = 'app/login.html'

    def get_success_url(self):
        return reverse_lazy('main_menu')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['username'] = self.request.user.username
        return context

class MainMenuView(LoginRequiredMixin, TemplateView):
    template_name = 'app/main_menu.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['username'] = self.request.user.username
        return context

class BalanceOperationsView(LoginRequiredMixin, View):
    template_name = 'app/operations.html'
    
    def get(self, request):
        context= {'balance': getBalance(request.user),'username':request.user.username}
        return render(request,self.template_name, context=context)

    def post(self, request):
        transaction = request.POST.get('operation')
        trans_amount = request.POST.get('amount')
        trans_amount = float(trans_amount)
        balance_temp = getBalance(request.user)
        if transaction == 'withdraw' and trans_amount > balance_temp:
            trans_status = 'failure'
            error1 = 'Withdraw amount cannot exceed balance '
        else:
            trans_status = 'success'
        transaction_record = History(
            status = trans_status, 
            amount = trans_amount, 
            type = transaction, 
            user= request.user)
        transaction_record.save()
        balance_recalc = getBalance(request.user)
        context = {'balance': balance_recalc,
                   'username': request.user.username}
        if trans_status == 'failure':
            context['error'] = error1
        return render(request, self.template_name, context=context) 

class ViewTransactionHistoryView(LoginRequiredMixin, ListView):
    model = History
    template_name = 'app/history.html'
    context_object_name = 'transactions'
    ordering = ['-datetime']

    def get_queryset(self):
        return History.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = self.request.user.username
        return context

class CurrencyExchangeView(LoginRequiredMixin, View):
    template_name = 'app/currency_exchange.html'
    empty_context = {'currency_choices': [], 'amount': None, 'currency': None, 'exchanged_amount': None}

    def get(self, request):
        _, currency_choices = getCurrencyParams()
        context = {
            'currency_choices': currency_choices, 
            'amount': None, 
            'currency': None, 
            'exchanged_amount': None,
            'username': request.user.username,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        data, currency_choices = getCurrencyParams()
        if float(request.POST.get('amount')):
            amount = float(request.POST.get('amount'))
        else:
            amount = None
        cur = request.POST.get('currency')
        if amount == None or data == None:
            return render(request, self.template_name, self.empty_context)
        else:
            exchange_rate = data.get(cur)
            exchanged_amount = amount * exchange_rate
            context = {
            'currency_choices': currency_choices, 
            'amount': amount, 
            'currency': cur, 
            'exchanged_amount': exchanged_amount,
            'username': request.user.username,
            }
            return render(request, self.template_name, context)