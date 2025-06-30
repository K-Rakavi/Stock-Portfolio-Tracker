# models.py

from django.db import models
from django.contrib.auth.models import User

class Stock(models.Model):
    name = models.CharField(max_length=100)
    ticker = models.CharField(max_length=10)
    sector = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    def get_price_change_trend(self):
         import random
         return random.choice(['up', 'down'])
class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    buy_date = models.DateField(null=False)
    buy_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)  
    investment = models.DecimalField(max_digits=12, decimal_places=2, null=True)  

    def __str__(self):
        return f"{self.user} - {self.stock}"




