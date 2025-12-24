# predict/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('predict/', views.predict, name='predict'),
    path('',views.home,name='home'),
    path('retrain/', views.trigger_retrain, name='retrain'),
    path('info/', views.model_info, name='info'),
]