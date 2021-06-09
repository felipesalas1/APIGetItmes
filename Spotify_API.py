#!/usr/bin/env python
# coding: utf-8

# # Proyecto Final Humanidades Digitales - FSalasNoguera
# 
# Este script hace peticiones al API de Spotify
# 
# 1. ### Se importan las librerias y se pone el Token de Auth para el API de Spotify
# 
# 

# In[19]:


#Importación de librerías
import datetime
import requests
import csv
import json
import random
import pandas as pd
import csv



# Timestamp como identificador de los archivos CSV
d = datetime.datetime.now()
timestamp = d.strftime("%Y-%m-%dT%H%M%S")
print(timestamp)


# Token de auth
token = 'BQDfN_rFGKp1d4w4splx568pBhqGYcB-wkFZTiELaTaL5hBM_VXrQwUS0vhb5VLql90SfZdDq46mj0F_hNtFeFnhIPvkgfzM62cUntrBN50s-3RCJHnP3r3oiO-eDtZComixXseqzhV31s-wk9educG7Zis5NRxj8Ro3TGzmqtw71HJMFq675aj2kzsvv40'
username = "felipesalas1234"

# Para obtener el Auth toca usar oAuth2.0, esto lo estoy haciendo desde Postman


# 2. ### Ingresa por teclado el nombre de un artista y lo busca en Spotify 

# In[20]:


#URL base del API

baseUrl = "https://api.spotify.com/v1/"

#Pide un input para buscar a un artista

artistNameInput = input()

id = 0


##https://api.spotify.com/v1/search?q=artistNameInput&type=artist&limit=1

url = "https://api.spotify.com/v1/" + "search?q=" + artistNameInput + "&type=artist&limit=1"



payload={}
headers = {
  'Accept': 'application/json',
  'Authorization': 'Bearer ' + token
}

response = requests.request("GET", url, headers=headers, data=payload)

#Si la respuesta del servidor es 200 o que fue satisfactoria almacena la respuesta JSON en una variable

if response.status_code == 200:

    searchArtist = response.json()

else: print(response.status_code)

#Obtiene el nombre del artista, su popularidad y ID
artists = searchArtist['artists']
theArtist = artists['items']
searchArtistName = theArtist[0]
theArtistName = searchArtistName['name']
theArtistId = searchArtistName['id']
theArtistPop = searchArtistName['popularity'] 

print("El artista ingresado es " + theArtistName)
print("Su popularidad es " + str(theArtistPop))
print("Su popularidad es " + str(theArtistId))

id = theArtistId

#Añade el nombre del artista en una variable para usar más adelante
artista = theArtistName


print("El artista ingresado es " + artista)

#Nombre del archivo de salida
csv_out = artista + "TracksAndRelated" + timestamp + ".csv"



#print(response.text)
    


# ### Opcional, buscar el artista por ID

# In[ ]:



#Opcional, Obtener info del artista por ID

id = input()

url = "https://api.spotify.com/v1/" + "artists/" + id

payload={}
headers = {
  'Accept': 'application/json',
  'Authorization': 'Bearer ' + token
}

response = requests.request("GET", url, headers=headers, data=payload)

if response.status_code == 200:

    artist = response.json()

else: print(response,status_code)

  # Store the artist name in the environment
artista = artist['name']


print("El artista ingresado es " + artista)


# 3. ### Obtenemos artistas relacionados del artista

# In[21]:


#URL para hacer el request GET para obtener los artistas relacionados con el artista que se ingreso anteriormente
url = "https://api.spotify.com/v1/artists/" + id + "/related-artists"

payload={}
headers = {
  'Accept': 'application/json',
  'Authorization': 'Bearer ' + token
}

response = requests.request("GET", url, headers=headers, data=payload)


if response.status_code == 200:

    responseRelated = response.json()
    
else: print(response,status_code)

#contador para el for y Lista de los artistas relacionados
count = 0
idRelated = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

for artistNum in responseRelated['artists']:
    artistsNames = artistNum['name']
    artistsIds = artistNum['id']
    #Imprime cada artista relacionado que informa Spotify
    print(artistsNames)
    idRelated [count] = artistNum['id']
    count += 1
    
    


            


# 4. ### Se crea un playlist en la cuenta del usuario

# In[26]:


#URL para el request POST para crear la playlist en el usuario

url = "https://api.spotify.com/v1/users/"+ username +"/playlists"

payload = json.dumps({
  "name": artista + " Mix",
  "public": False
})
headers = {
  'Accept': 'application/json',
  'Authorization': 'Bearer '+token,
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

responsePlaylist = response.json()

#Obtiene los datos del JSON y los almacena en las variables
elNombre = responsePlaylist['name']
playlistId = responsePlaylist['id']

print("El nombre de la playlist creada es: " + elNombre)


# 5. ### Toma los Top Tracks del artista y los artistas relacionados. crea un CSV con los datos y los prepara para enviarlos a spotify
# 
# 
# 
# 

# In[23]:


#Contador para el for de las canciones
count = 0

#Pepara el CSV para guardar los datos obtenidos de Spotify
with open(csv_out, 'w') as csvfile:

  
  #Instanciación del objeto writer de la librería CSV
  tablewriter = csv.writer(csvfile, delimiter=',', quotechar='"')
  

  # Headers para el CSV
  headers = ["track_title","track_id","track_artist","track_pop","track_uri","track_rDate"]

   # Se escriben los encabezados en la tabla
  tablewriter.writerow(headers)

  # campos a buscar en los metadatos
  track_title = ""
  track_id = ""
  track_artist = ""
  track_pop = ""
  track_uri = ""
  track_rDate = ""



  #Toma los top tacks de las bandas relacionadas
  #Contadores para el For y los IF
  countb = 0
  counta = 0
  #Lista de los tracks relacionados, crea 90 y los llena con un dato Dummie
  idTracks = ["spotify:track:3ZLElfsFXSMmNCliIGhIb7"] * 90

  #Para cada artista relacionado hace una petición para obtener sus top tracks
  for band in idRelated:
      url = "https://api.spotify.com/v1/artists/" + idRelated[countb] + "/top-tracks?country=co"
      payload={}
      headers = {
      'Accept': 'application/json',
      'Authorization': 'Bearer '+token,
      'Content-Type': 'application/json'
      }

      response = requests.request("GET", url, headers=headers, data=payload)

    
      
      if response.status_code == 200:

        responseTracks = response.json()
      
      else: print(response.status_code)

      
     #contador para el for
      countd = 0
      for trackId in responseTracks['tracks']:
        

        #Toma datos del Json
        track_title = trackId['name']
        print(track_title)
        track_id = trackId['id']
        countc = 0
        for trackArt in trackId['artists']:
          
          if countc > 0:
            track_artist = track_artist + " - " + trackArt['name']
          else:
            track_artist = trackArt['name']
          countc += 1
          print(track_artist)
        track_pop = trackId['popularity']
        track_uri = trackId['uri']
        track_rDate = trackId['album']['release_date']

        new_row = [track_title,track_id,track_artist,track_pop,track_uri,track_rDate]

        #escribimos la fila en la tabla
        tablewriter.writerow(new_row) 

        print(countd)

        #toma solamente tres tracks para añadirlo a la playlist creada los otros datos son solamente para el CSV
        if countd <= 3:
        
          #trackIds = trackId['id']
          idTracks [counta] = trackId['uri']
          countd += 1
          counta += 1
        else: print("Artista número: " + str(countb))
        

      countb += 1 

  print(idTracks)

  #Añade las canciones del artista principal

  url = "https://api.spotify.com/v1/artists/" + id + "/top-tracks?country=co"
  payload={}
  headers = {
  'Accept': 'application/json',
  'Authorization': 'Bearer '+token,
  'Content-Type': 'application/json'
  }

  response = requests.request("GET", url, headers=headers, data=payload)

    
      
  if response.status_code == 200:

      responseTracks = response.json()

  else: print(response.status_code)

      
  #Añade las canciones del artista principal a la lista de tracks  
  for trackId in responseTracks['tracks']:
      #trackIds = trackId['id']
      idTracks [counta] = trackId['uri']
      track_title = trackId['name']
      print(track_title)
      track_id = trackId['id']
      countc = 0
      for trackArt in trackId['artists']:
          
        if countc > 0:
          track_artist = track_artist + " - " + trackArt['name']
        else:
          track_artist = trackArt['name']
        countc += 1
        print(track_artist)
        track_pop = trackId['popularity']
        track_uri = trackId['uri']
        track_rDate = trackId['album']['release_date']

        new_row = [track_title,track_id,track_artist,track_pop,track_uri,track_rDate]

        #escribimos la fila en la tabla
        tablewriter.writerow(new_row) 
      counta += 1



# 6. ### Desorganiza los items y los añade al playlist

# In[25]:


#Random el orden las pistas de la playlist

random.shuffle(idTracks)

print(idTracks)

#Prepara los URIS para que Spotify lo acepte

uris = ",".join(idTracks)

print(uris)

url = "https://api.spotify.com/v1/users/felipesalas1234/playlists/" + playlistId + "/tracks?uris=" + uris

payload={}
headers = {'Accept': 'application/json','Authorization': 'Bearer '+token,'Content-Type': 'application/json'}

response = requests.request("POST", url, headers=headers, data=payload)


    
if response.status_code == 200:

    responseTracks = response.json()
else: print(response.status_code)

print("se ha creado la playlist en la cuenta de: " + username)

