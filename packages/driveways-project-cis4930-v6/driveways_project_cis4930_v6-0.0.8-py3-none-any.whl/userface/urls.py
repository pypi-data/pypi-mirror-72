from django.urls import path
import re
from . import views
from django.conf.urls import url

app_name = 'userface'
urlpatterns = [
    path('', views.index, name='index'),
]

urlpatterns += [
    path('myvehicles/', views.VehicleListView.as_view(), name='my-vehicles'),
    path('register/', views.register, name='register'),
    path('search/', views.search, name='search'),
    path('registervehicle/',views.registervehicle, name = 'registervehicle'),
    path('addspot/',views.addspot, name = 'addspot')
    #url(r'^mapview/(?P<pk>[0-9]+)$', views.DestinationDetailView.as_view(), name='search_results')
]