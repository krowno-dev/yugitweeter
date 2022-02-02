#https://storage.googleapis.com/ygoprodeck.com/pics_artgame/160302010.jpg
import requests
import json
from random import randint
f = open('yugi/cardinfo.php')
yugi = json.load(f)
f.close()

listaIDS = []
for carta in yugi['data']:
    listaIDS.append(carta['id'])
for i in range(1,20):
    idRand = randint(0,len(listaIDS)-1)
    for carta in yugi['data']:
        if carta['id'] == listaIDS[idRand]:
            pagina = "https://storage.googleapis.com/ygoprodeck.com/pics_artgame/" + str(carta['id']) + ".jpg"
            print(pagina)
            response = requests.get(pagina)
            nombre = "yugi/fotopeques/"+str(carta['id'])+'.jpg'
            imagen = open(nombre, "wb")
            imagen.write(response.content)
            imagen.close()