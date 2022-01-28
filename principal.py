from time import sleep
from datetime import datetime
import requests
import json
from random import randint
from auth import (
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret
)
from twython import Twython



twitter = Twython(
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret
)

def textolargo(tocho):
    if len(tocho) >= 270:
        tochoIzq = tocho[:269]
        tochoDer = tocho[269:]
        tochoPr = tochoIchoPr = tochoIzq + "[...]"
        print(tochoPr)

        tweet = twitter.get_user_timeline(
        screen_name="twbotyugioh",
        count=1)
        twID = tweet[0]["id"]
        twitter.update_status(status=tochoPr, in_reply_to_status_id=twID)
        textolargo(tochoDer)
    else:
        print(tocho)
        tweet = twitter.get_user_timeline(
        screen_name="twbotyugioh",
        count=1)
        twID = tweet[0]["id"]
        twitter.update_status(status=tocho, in_reply_to_status_id=twID)

response = requests.get("https://db.ygoprodeck.com/api/v7/cardinfo.php")
datosBD = open("cardinfo.php", "wb")
datosBD.write(response.content)
datosBD.close()
        

f = open('cardinfo.php')
yugi = json.load(f)
f.close()

listaIDS = []
for elemento in yugi["data"]:
    #print (elemento["id"])
    listaIDS.append(elemento["id"])

print(len(listaIDS))
totalCartas = len(listaIDS)


bucle = True

while bucle == True:
    
    sleep(30)
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    horaP = current_time[3:5]
    print(horaP)
    
    if  horaP == "00" or horaP == "30":

        numID = randint(0,len(listaIDS)-1)
        idRand = listaIDS[numID]
        #idRand = 4538826 #chaos emperor armageddon - texto largo
        print(idRand)
        listaIDS.remove(idRand)

        for elemento in yugi["data"]:
            if elemento["id"] == idRand:
                primerTwit = True
                nombre = elemento["name"]
                tipo = elemento["type"]
                desc = elemento["desc"]
                direccion = elemento["card_images"][0]["image_url"]

                
                texto = ("%s  //  %s\n\n%s"%(nombre,tipo,desc))
                #print(texto)
                


                response = requests.get(direccion)
                imagen = open("subida.png", "wb")
                imagen.write(response.content)
                imagen.close()
                photo = open('subida.png', 'rb')
                
                if len(texto) >= 270:
                    textoIzq = texto[:269]
                    textoDer = texto[269:]
                    textoPr = textoIzq + "[...]"
                    print(textoPr)
                    response = twitter.upload_media(media=photo)
                    twitter.update_status(status=textoPr,media_ids=[response["media_id"]])

                    textolargo(textoDer)
                else:
                    print(texto)
                    response = twitter.upload_media(media=photo)
                    twitter.update_status(status=texto,media_ids=[response["media_id"]])

                photo.close()

                tweet = twitter.get_user_timeline(
                screen_name="twbotyugioh",
                count=1)
                twID = tweet[0]["id"]
                
                pagina = "https://db.ygoprodeck.com/card/?search=" + str(idRand)
                respuesta = "go " + pagina + " to know more about " + nombre + "!!!"

                twitter.update_status(status=respuesta, in_reply_to_status_id=twID)


                #registro = nombre + " subido a las " + current_time + "\n"
                registro = current_time + "  -  "+ nombre + "\n"
                print(registro)
                registroArch = open('registro.txt','a')
                registroArch.write(registro)
                registroArch.close()
        
        sleep(1600)
    if len(listaIDS) == 0:
        bucle == False



textoPr = "I have uploaded all " + str(totalCartas) + " cards!!!!!!!!"
photo = open('celebracion.png', 'rb')
response = twitter.upload_media(media=photo)
twitter.update_status(status=textoPr,media_ids=[response["media_id"]])
