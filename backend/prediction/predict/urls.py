from django.urls import path
from . import views

urlpatterns = [
    path('api/predict/', views.form_api, name='form_api'),
]