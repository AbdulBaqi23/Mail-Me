from django.urls import path
from . import views

urlpatterns = [
    path('inbox/', views.inbox_api, name='api-inbox'),
    path('sent/', views.sent_api, name='api-sent'),
    path('compose/', views.compose_api, name='api-compose'),
]
