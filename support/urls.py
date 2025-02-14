from django.urls import path
from . import views

app_name = 'support'

urlpatterns = [
    path('ticket/create/', views.create_ticket, name='create_ticket'),
    path('tickets/', views.ticket_list, name='ticket_list'),
]
