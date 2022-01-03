from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
import requests
from django.views.decorators.csrf import csrf_protect
from IPCMusic.forms import *
import csv
import io
import xml.etree.ElementTree as ET

global csv_list
csv_list = []
endpoint = 'http://localhost:4000{}'
@csrf_protect

def inicio(request):
    if request.method == 'GET':
        url = endpoint.format('/mostrar')  # http://localhost:4000/datos
        data = requests.get(url)  # consulta a la API
        context = {
            'data': data.json,
        }
        return render(request, 'inicio.html', context)    

root = "Output.xml"
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
        context = {'text_error':val,
            'error':error_csv}                
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

def carga_xml(request):
    if request.method == 'GET':
        return render(request, 'xml.html')
    elif request.method == 'POST':
        ertxt = "Error en la linea: "
        try:
            docs = request.FILES['document']
        except:
            return render(request, 'xml.html',{'text_error':'Seleccione un documento valido'})
        data = docs.read().decode('utf-8')
        biblioteca = ET.fromstring(data)
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
                        album += str(al.text)
                    for vr in can.iter("vecesReproducida"):
                        veces_rep += vr.text       
                    for im in can.iter("imagen"):
                        imagen += im.text 
                    for ru in can.iter("ruta"):
                        ruta += ru.text   
                    agregar_cancion = ({"artista":artista,"vecesReproducida":veces_rep,"album":album,"imagen":imagen,"ruta":ruta,"nombre":nombre})
                    csv_list.append(agregar_cancion) 
    return redirect('CSV_XML')

def enviar_json(request):    
    if request.method == 'GET':
        context = {'data': csv_list}
        return render(request, 'csv_xml.html', context)
    elif request.method == 'POST':        
        url = endpoint.format('/carga')
        requests.post(url,json=csv_list) 
        csv_list.clear()      
        return redirect("Inicio")

