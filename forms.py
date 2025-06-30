from django import forms
from .models import Portfolio, Stock
from django.contrib.auth.models import User

class PortfolioForm(forms.ModelForm):
    user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label="User",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    stock = forms.ModelChoiceField(
        queryset=Stock.objects.all(),
        label="Stock",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    buy_date = forms.DateField(
        label="Buy Date",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )

    class Meta:
        model = Portfolio
        fields = ['user', 'stock', 'quantity', 'buy_date']

