from django.urls import path
from . import views

urlpatterns = [
    path('', views.portfolio_view, name='portfolio_home'),
    path('add/', views.add_portfolio_entry, name='add_portfolio'),
    path('trend/<str:ticker>/', views.stock_trend_view, name='stock_trend'),
]


