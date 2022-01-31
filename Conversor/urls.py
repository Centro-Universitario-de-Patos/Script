from django.urls import path
from . import views

urlpatterns = [
    path('', views.converter, name='converter'),
    path('export_csv', views.export_csv, name='export_csv'),
    path('curso', views.retorna_curso, name='curso'),
]
