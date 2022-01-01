from django import forms

class cancion(forms.Form):
    artista = forms.CharField(label="artista")
    vecesReproducida = forms.CharField(label="vecesReproducida")
    album = forms.CharField(label="album")
    imagen = forms.CharField(label="imagen")
    ruta = forms.CharField(label="ruta")
    nombre = forms.CharField(label="nombre")