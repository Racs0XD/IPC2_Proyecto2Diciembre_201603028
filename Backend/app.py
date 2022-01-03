import json
from flask import Flask, Response, jsonify, request
from flask_cors import CORS

import matplotlib
import matplotlib.pyplot as plt
import numpy as np


app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origin": "*"}})#habilita el acceso a la api desde rutas externas

biblioteca = []
listas = []

artistas=[]
albums = []
canciones = []

@app.route('/carga', methods=['POST'])
def add_usuario():   
    a = request.json    
    for arts1 in a :                
        art1 = arts1["artista"]                       
        artista = {            
            "artista":art1,
            } 
        if artistas == []:       
            artistas.append(artista)
        else:
            b = len(artistas) - 1
            if art1 not in artistas[b]['artista']:
                artistas.append(artista)
    
    for arts2 in a :                
        art2 = arts2["artista"]
        alb2 = arts2["album"]
        
        
        album = {
            "album":alb2,      
            "artista":art2,  
        }

        if albums == []:
            albums.append(album)
        else:
            c = len(albums) - 1
            if alb2 not in albums[c]['album']:
                albums.append(album)
                
            
    for arts3 in a :                
        art3 = arts3["artista"]
        alb3 = arts3["album"]
        rep3 = arts3["vecesReproducida"]
        img3 = arts3["imagen"]
        rut3 = arts3["ruta"]
        nom3 = arts3["nombre"] 
        
        cancion = {            
            "artista":art3,
            "album":alb3,  
            "vecesReproducida":rep3,      
            "imagen":img3,
            "nombre":nom3,
            "ruta":rut3,     
        }        
        if canciones == []:
            canciones.append(cancion)
        else:
            d = len(canciones) - 1
            if nom3 not in canciones[d]['nombre']:
                canciones.append(cancion)       


    return jsonify({"Biblioteca": "Lista agreada satisfactoriamente"})

@app.route('/cargaedit', methods=['POST'])
def add_usuario_editad():   
    salida= request.json  
    a = json.dumps(salida)  
    """
    for arts1 in a :                
        art1 = arts1["artista"]                       
        artista = {            
            "artista":art1,
            } 
        if artistas == []:       
            artistas.append(artista)
        else:
            b = len(artistas) - 1
            if art1 not in artistas[b]['artista']:
                artistas.append(artista)
    
    for arts2 in a :                
        art2 = arts2["artista"]
        alb2 = arts2["album"]
        
        
        album = {
            "album":alb2,      
            "artista":art2,  
        }

        if albums == []:
            albums.append(album)
        else:
            c = len(albums) - 1
            if alb2 not in albums[c]['album']:
                albums.append(album)
                
            
    for arts3 in a :                
        art3 = arts3["artista"]
        alb3 = arts3["album"]
        rep3 = arts3["vecesReproducida"]
        img3 = arts3["imagen"]
        rut3 = arts3["ruta"]
        nom3 = arts3["nombre"] 
        
        cancion = {            
            "artista":art3,
            "album":alb3,  
            "vecesReproducida":rep3,      
            "imagen":img3,
            "nombre":nom3,
            "ruta":rut3,     
        }        
        if canciones == []:
            canciones.append(cancion)
        else:
            d = len(canciones) - 1
            if nom3 not in canciones[d]['nombre']:
                canciones.append(cancion)       
"""

    return jsonify({"Biblioteca": "Lista agreada satisfactoriamente"})

@app.route('/mostrar')
def listado():    
    return jsonify(canciones)


@app.route('/escuchadas')
def escuchadas():  
    x = []  
    y = []
    re = []
    for rep in canciones:
        top={
            'vecesReproducida':rep['vecesReproducida'],
            'nombre':rep['nombre']
        }
        
        re.append(top)

    for i in range(len(re)):
        for j in range(len(re)-1):
            if (int(re[j]['vecesReproducida']) < int(re[j+1]['vecesReproducida'])):
                temp = re[j]
                re[j] = re[j+1]
                re[j+1] = temp
    
    for rank in range(len(re)):
        if(rank <= 5):
            x.append(re[rank]['nombre'])
            y.append(re[rank]['vecesReproducida'])


    x1 = list(reversed(x))
    y1 = list(reversed(y))
    x_pos = np.arange(len(x1))    
    plt.bar(x_pos,y1)    
    plt.xticks(x_pos, x1, rotation=90)
    plt.subplots_adjust(bottom=0.4, top=0.99)
    plt.savefig('Frontend\IPCMusic\static\masEscuchadas.png')
    plt.close()
    
    return jsonify("Grafica generada")

@app.route('/reproducidas')
def reproducidos():  
    x = []  
    y = []
    re = []
    for rep in canciones:
        top={
            'vecesReproducida':rep['vecesReproducida'],
            'artista':rep['artista']
        }
        
        re.append(top)

    for i in range(len(re)):
        for j in range(len(re)-1):
            if (int(re[j]['vecesReproducida']) < int(re[j+1]['vecesReproducida'])):
                temp = re[j]
                re[j] = re[j+1]
                re[j+1] = temp
    
    for rank in range(len(re)):
        if(rank <= 5):
            x.append(re[rank]['artista'])
            y.append(re[rank]['vecesReproducida'])


    x2 = list(reversed(x))
    y2 = list(reversed(y))
    
    plt.pie(y2, labels= x2)    
    plt.savefig('Frontend\IPCMusic\static\masReproducidos.png')
    plt.close()
    return jsonify("Grafica generada")

  



if __name__ == '__main__':
    app.run(debug=True, port=4000)