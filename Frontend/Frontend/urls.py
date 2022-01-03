"""Frontend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from IPCMusic.views import *

urlpatterns = [
    path('', inicio, name = "Inicio"),
    path('csv/', carga_csv, name = "CSV"),
    path('csv_xml/', enviar_json, name = "CSV_XML"),
    path('xml/', carga_xml, name = "XML"),
    path('escuchadas/', escuchadas, name = "escuchadas"),
    path('reproducidas/', reproducidas, name = "reproducidas"),
    path('clasificacion/', clasificacion, name = "clasificacion"),
    path('escuchadasL/', escuchadasL, name = "escuchadasL"),
    path('reproducidasL/', reproducidasL, name = "reproducidasL"),
    path('info/', info, name = "info"),
    path('doc/', doc, name = "doc"),
    path('editar/', editar, name = "editar"),


]
