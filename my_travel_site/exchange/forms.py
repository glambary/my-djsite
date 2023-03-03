from django import forms


class ExchangeForm(forms.Form):
    percent = forms.FloatField(label='Процент банков', max_value=100, min_value=0, initial=2)
    foreign_rate = forms.FloatField(label='Курс интересуемой валюты (сейчас в Беларуси)', min_value=0.001, initial=2.807)
    amount = forms.FloatField(label='Сколько денег поменять (рос. рублей)', min_value=1, initial=5000)
    #a = forms.IntegerField(empty_value=2)