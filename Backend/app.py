import json
from os import replace
from flask import Flask, Response, jsonify, request
from flask_cors import CORS

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
        
        im = img3.replace('\\','//')
        ru = rut3.replace('\\','//')
        cancion = {            
            "artista":art3,
            "album":alb3,  
            "vecesReproducida":rep3,      
            "imagen":im,
            "nombre":nom3,
            "ruta":ru,     
        }        
        if canciones == []:
            canciones.append(cancion)
        else:
            d = len(canciones) - 1
            if nom3 not in canciones[d]['nombre']:
                canciones.append(cancion)       


    print(canciones)
    return jsonify({"Biblioteca": "Lista agreada satisfactoriamente"})

@app.route('/mostrar')
def listado():    
    return jsonify(canciones)

@app.route('/csv', methods=['GET'])
def get_datos():
    save_file = open('save_file.txt', 'r+')
    return Response(status=200,
                    response=save_file.read(),
                    content_type='text/plain')


@app.route('/csv', methods=['POST'])
def post_data():
    str_file = request.data.decode('utf-8')
    save_file = open('save_file.txt', 'w+')
    save_file.write(str_file)
    save_file.close()
    return Response(status=204)



if __name__ == '__main__':
    app.run(debug=True, port=4000)