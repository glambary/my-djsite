from django.shortcuts import render

from .forms import *


# Create your views here.
def index(request):
    import datetime
    from .additional_module import get_currency_rate

    if request.method == 'POST':
        form = ExchangeForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            # print(fc)
            # print(form.cleaned_data)
        # percent = float(request.POST.get('percent'))
        # foreign_rate = float(request.POST.get('foreign_rate'))
        # amount = float(request.POST.get('amount'))
        percent = cleaned_data['percent']
        foreign_rate = cleaned_data['foreign_rate']
        amount = cleaned_data['amount']
    elif request.method == 'GET':
        form = ExchangeForm()
        percent = form.fields['percent'].initial
        foreign_rate = form.fields['foreign_rate'].initial
        amount = form.fields['amount'].initial

    rate = get_currency_rate.get_exchange_rate_bel_rub()
    rate_of_bank = round(rate * (1 + percent / 100), 2)

    now = datetime.datetime.now()
    today_date = now.strftime("%d.%m.%Y")
    today_time = now.strftime("%H:%M")

    context = {'title': 'Exchange',
               'form': form,
               'rate': rate,
               'rate_of_bank': rate_of_bank,
               'rate_to': round(10000 / rate, 2), # курс в пересчёте на старую валюту
               'rate_of_bank_to': round(10000 / rate_of_bank, 2), # курс (от банка) в пересчёте на старую валюту
               'today_date': today_date,
               'today_time': today_time,
               'percent': percent,
               'foreign_rate': round(foreign_rate * rate_of_bank, 2),
               'amount_foreign_money': round(amount / (foreign_rate * rate_of_bank), 2),
               'amount_bel_money': round(amount / rate_of_bank, 2),
               }
    return render(request, 'exchange/index.html', context=context)


