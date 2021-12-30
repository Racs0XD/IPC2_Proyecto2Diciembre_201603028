from django.shortcuts import render, redirect
import requests
from django.views.decorators.csrf import csrf_protect

# Create your views here.

from django.http import HttpResponse
from django.template.loader import get_template

endpoint = 'http://localhost:4000{}'
@csrf_protect

def inicio(request):
    plantilla_inicio = get_template('inicio.html')
    rend_plantilla = plantilla_inicio.render()

    return HttpResponse(rend_plantilla)

"""def carga_csv(request):
    if request.method == 'GET':
        url = endpoint.format('/csv')  # http://localhost:4000/datos
        data = requests.get(url)  # consulta a la API
        context = {
            'data': data.text,
        }
        return render(request, 'csv.html', context)
    elif request.method == 'POST':
        docs = request.FILES['document']
        data = docs.read()
        url = endpoint.format('/csv')
        requests.post(url, data)
        return redirect('CSV')"""

def carga_csv(request):
    if request.method == 'GET':
        url = endpoint.format('/csv')  # http://localhost:4000/datos
        data = requests.get(url)  # consulta a la API
        context = {
            'data': data.text,
        }
        return render(request, 'csv.html', context)
    elif request.method == 'POST':
        docs = request.FILES['document']
        data = docs.read()
        url = endpoint.format('/csv')
        requests.post(url, data)
        return redirect('CSV')



def carga_xml(request):
    if request.method == 'GET':
        url = endpoint.format('/xml')  # http://localhost:4000/datos
        data = requests.get(url)  # consulta a la API
        context = {
            'data': data.text,
        }
        return render(request, 'xml.html', context)
    elif request.method == 'POST':
        docs = request.FILES['document']
        data = docs.read()
        url = endpoint.format('/xml')
        requests.post(url, data)
        return redirect('XML')


"""def carga_xmlcopleto(ruta):   
    contenido = open(ruta).read()
    biblioteca = ET.fromstring(contenido)
    for biblio in biblioteca.iter("biblioteca"):
        for can in biblio.iter("cancion"):
            nombre = can.attrib['nombre']
            album = ""
            artista = ""
            imagen = ""
            ruta = ""
            for ar in can.iter("artista"):
                artista += ar.text  
            for al in can.iter("album"):
                album += al.text  
            for im in can.iter("imagen"):
                imagen += im.text 
            for ru in can.iter("ruta"):
                ruta += ru.text   
            Listar.agregarCancion(artista,album,imagen,ruta,nombre)"""
 

def carga_masiva():
    print("Hola carga Masiva")




# Create your views here.





def reports(request):
    if request.method == 'GET':
        date = request.GET.get('date', None)
        code = request.GET.get('code', None)

        context = {
            'date': None,
            'code': None,
        }
        if date is not None:
            context['date'] = date

        if code is not None:
            context['code'] = code
        return render(request, 'reports.html', context)


def calc(request):
    if request.method == 'GET':
        num_1 = request.GET.get('num_1', 0)
        num_2 = request.GET.get('num_2', 0)

        url = endpoint.format('/potencia')

        potencia = requests.get(url, {
            'num_1': num_1,
            'num_2': num_2,
        })

        context = {
            'potencia': potencia.text,
        }

        return render(request, 'calc.html', context)
    
