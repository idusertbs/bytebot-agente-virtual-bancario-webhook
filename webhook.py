# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 10:37:23 2018

@author: amanosalva
"""

import json
import os
import requests

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    print(json.dumps(req, indent=4))
    
    res = makeResponse(req)
    
    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeResponse(req):

    result = req.get("result")
    metadata = result.get("metadata")
    intentName = metadata.get("intentName")

    def verificacion():
        r_verificacion = requests.get('http://181.177.228.114:5000/query')
        json_object_verificacion = r_verificacion.json()
        verificacion = json_object_verificacion['result']['codigo']
        return verificacion

    verificacion_response = {
                "speech": "verificación", "displayText": "verificación", "source": "apiai-weather-webhook",
                "messages": [
                    { "type": 0, "platform": "facebook", "speech": "Bien! Pero primero necesito saber tu identidad"},
                    { "type": 4, "platform": "facebook", "payload": { "facebook": { "attachment": { "type": "template", "payload": { "template_type": "button", "text": "¿Con qué tipo de documento estás registrado?",
                                "buttons": [ 
                                    { "type": "postback", "title": "DNI", "payload": "DNI" },
                                    {"type": "postback", "title": "Carné de extranjería", "payload": "Carné de extranjería"},
                                    {"type": "postback", "title": "Pasaporte", "payload": "Pasaporte" }
                                ]}}}}
                    },
                    { "type": 0, "speech": "" }
                ]
            }

    
    if intentName == "bytebot.avb.seleccion.documento-doc.digitado":        
        parameters = result.get("parameters")
        documento = parameters.get("number")
        r=requests.get('http://181.177.228.114:5001/clientes/' + str(documento))
        json_object = r.json()
        es_cliente = json_object["result"]["codigo"]

        if int(es_cliente) == 0:
            speech = "Aún no eres cliente de nuestro banco :("
            return {                
                "speech": speech,
                "displayText": speech,
                "source": "bytebot-virtual-agent-webhook"

        }
        else:
            speech = "Voy a enviar un código de verificación. Indícame a donde prefieres que lo envíe"
            return{
                "speech": speech,
                "messages": [
                    { "type": 4, "platform": "facebook", "payload": { "facebook": { "attachment": { "type": "template", "payload": { "template_type": "button", "text": speech,
                                "buttons": [ 
                                    { "type": "postback", "title": "Celular", "payload": "Celular" },
                                    {"type": "postback", "title": "E-mail", "payload": "E-mail"}
                                ]}}}}
                    },
                    { "type": 0, "speech": "" }
                ]
            }



    if intentName == "bytebot.avb.consultar.cuentas":
        #Verificación: ¿El estado de la tabla BBOTSEFAC es true o false?        
        verificacion = verificacion()
        
        if int(verificacion) != 0:              
            r=requests.get('http://181.177.228.114:5001/clientes/' + str(74563192))
            json_object = r.json()
            debito=json_object['result']['clientes']['debito']
            cuentas_debito = []
            json_string_inicio = u'{"type": 0,"platform": "facebook","speech": "Seleccione el tipo de cuenta:"}'
            objeto_inicio = json.loads(json_string_inicio)
            cuentas_debito.append(objeto_inicio)
            objeto = ''
            for i in range(0,len(debito)):
                json_string = u'{"type": 1,"platform": "facebook","title": "' + str(debito[i]["nombre"]) + '","imageUrl":  "' + str(debito[i]["imageUrl"]) + '","buttons": [{"text": "Seleccionar Cuenta","postback": "' + str(debito[i]["nombre"]) + '"}]}'
                objeto  = json.loads(json_string)
                cuentas_debito.append(objeto)
            #verificando el carrusel dinámico
            return {
                "speech": "hola",
                "displayText": "hola",
                "source": "apiai-weather-webhook",
                "messages": cuentas_debito
                }
        
        else:
            return verificacion_response


        
                 

    if intentName == "bytebot.avb.consultar.tarjetas":        
        #verificar si puede consultar cuentas
        speech = "Todavía no me implementan la opción de verificación, así que no podrás consultar tus tarjetas 😢"
        return {
            "speech": speech,
            "displayText": speech,
            "source": "bytebot-virtual-agent-webhook"

        }
    if intentName == "bytebot.avb.consultar.tipo.de.cambio":        
        #verificar si puede consultar cuentas
        speech = "Todavía no me implementan la opción de verificación, así que no podrás consultar el tipo de cambio 😢"
        return {
            "speech": speech,
            "displayText": speech,
            "source": "bytebot-virtual-agent-webhook"

        }
    
    


        
    
    
    
    
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')

















