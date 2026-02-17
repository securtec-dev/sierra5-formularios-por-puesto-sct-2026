from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('estado-de-equipos/<slug:slug>/', views.formulario, name='formulario'),
]