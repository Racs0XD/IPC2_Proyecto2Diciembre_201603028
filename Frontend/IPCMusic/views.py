from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
import requests
from django.views.decorators.csrf import csrf_protect
from IPCMusic.forms import *
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
import csv
import io
import xml.etree.ElementTree as ET
def carga_csv(request):
    if request.method == 'GET':
        return render(request, 'csv.html')
    elif request.method == 'POST':
        ertxt = "Error en la linea: "
        try:
            docs = request.FILES['document']
        except:
             return render(request, 'csv.html',{'text_error':'Seleccione un documento valido'})              
       
        data = docs.read().decode('utf-8')
        io_string = io.StringIO(data)
        global csv_list
        csv_list = []
        val=""
        error_csv = True
        
        cont = 0

        usrconfig = ET.Element("usrconfig")
        usrconfig = ET.SubElement(usrconfig,"ListasReproduccion")
        
        for line in csv.DictReader(io_string, delimiter=';', quotechar='|'): 
            cont += 1          
            if line["artista"].isnumeric() is False:
                if line["album"].isnumeric() is False:
                    if line["vecesReproducida"].isnumeric() is True:    
                        if line["nombre"].isnumeric() is False:       
                            cancion =  ET.SubElement(usrconfig, "cancion")
                            cancion.attrib = {"nombre":line["nombre"]}
                            artista =  ET.SubElement(cancion, "artista")
                            artista.text = line['artista']
                            album = ET.SubElement(cancion, "album")
                            album.text = line['album']
                            veces_reproducida = ET.SubElement(cancion, "vecesReproducida")
                            veces_reproducida.text = line['vecesReproducida']
                            imagen = ET.SubElement(cancion, "imagen")
                            imagen.text = line['imagen']
                            ruta = ET.SubElement(cancion, "ruta")
                            ruta.text = line['ruta']
                            error_csv = False
                            
                            
                        else:
                            val = ertxt+str(cont)+" nombre: "+line['nombre']+" se requiere un texto."
                            error_csv = True
                            csv_list.append(val)                                             
                    else:
                        val = ertxt+str(cont)+" vecesReproducida: "+line['vecesReproducida']+" se requiere un numero entero."
                        error_csv = True
                        csv_list.append(val)
                else:
                    val = ertxt+str(cont)+" album: "+line['album']+" se requiere un texto."
                    error_csv = True
                    csv_list.append(val)
            else:
                val = ertxt+str(cont)+" artista: "+line['artista']+" se requiere texto"
                error_csv = True
                csv_list.append(val)
        root = "Output.xml"
        tree = ET.ElementTree(usrconfig)
        tree.write(root, encoding='utf-8', xml_declaration=True)
        
        contenido = open(root).read()
        biblioteca = ET.fromstring(contenido)
        for biblio in biblioteca.iter("ListasReproduccion"):
            for can in biblio.iter("cancion"):
                nombre = can.attrib['nombre']
                album = ""
                artista = ""
                veces_rep = ""
                imagen = ""
                ruta = ""
                for ar in can.iter("artista"):
                    artista += ar.text  
                for al in can.iter("album"):
                    album += al.text
                for vr in can.iter("vecesReproducida"):
                    veces_rep += vr.text       
                for im in can.iter("imagen"):
                    imagen += im.text 
                for ru in can.iter("ruta"):
                    ruta += ru.text   
                agregar_cancion = ({"artista":artista,"vecesReproducida":veces_rep,"album":album,"imagen":imagen,"ruta":ruta,"nombre":nombre})
                csv_list.append(agregar_cancion)    
        context = {
            'data': csv_list,
            'text_error':val,
            'error':error_csv,
        }
                
        if error_csv is True:
            error_csv = False  
            return render(request, 'csv.html', context)  
        else:
            error_csv = True  
            return redirect('CSV_XML')

#--------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------


def enviar_json(request):
    context = {
            'data': csv_list,
        }
    return render(request, 'csv_xml.html', context)


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
    
