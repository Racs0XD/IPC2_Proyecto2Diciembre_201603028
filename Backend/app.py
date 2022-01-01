from flask import Flask, Response, jsonify, request
from flask_cors import CORS

from math import pow

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origin": "*"}})#habilita el acceso a la api desde rutas externas

biblioteca = []

@app.route('/carga', methods=['POST'])
def add_usuario():  
    new_song = {
        "artista": request.json['username'],
        "vecesReproducida": request.json['vecesReproducida'],
        "album": request.json['album'],
        "imagen": request.json['imagen'],
        "url": request.json['url'],
        "nombre": request.json['nombre']
    }
    biblioteca.append(new_song)            
    return jsonify({'ok':True, "Usuario": "Usuario agreado satisfactoriamente"})

@app.route('/mostrar')
def listado():    
    return jsonify(biblioteca)

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