# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 10:37:23 2018

@author: amanosalva
"""

import json
import os
import requests
import re

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
        documento = parameters.get("phone-number")
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

    if intentName == "bytebot.avb.seleccion.documento-doc.digitado-canal.digitado":        
        parameters = result.get("parameters")
        canal = parameters.get("canal")
        documento = 74563192
        r=requests.get('http://181.177.228.114:5001/clientes/' + str(documento))
        json_object = r.json()
        telefono = json_object["result"]["clientes"]["telefono"]


        if canal == "E-mail":
            speech = "Aún no tenemos implementado ese servicio :("
            return {                
                "speech": speech,
                "displayText": speech,
                "source": "bytebot-virtual-agent-webhook"

        }
        else:
            speech = "Estoy enviando el código de verificación al celular (******" + str(telefono[9:]) + ")"
            #r_token=requests.get('http://181.177.228.114:5000/enviatoken/' + str(telefono))
            return{
                "speech": speech,
                "messages": [                    
                    { "type": 0, "platform": "facebook", "speech": speech},
                    { "type": 0, "platform": "facebook", "speech": "Por favor, ingresa tu clave de registro de 4 dígitos que te envié :)"}
                ]
            }


    if intentName == "bytebot.avb.seleccion.documento-doc.digitado-canal.digitado-no.me.llega":        
        speech = "Que extraño 🤔. ¿Deseas que te envíe el código nuevamente?"
        return {
                "speech": speech,
                "messages": [
                    { "type": 4, "platform": "facebook", "payload": { "facebook": { "attachment": { "type": "template", "payload": { "template_type": "button", "text": speech,
                                "buttons": [ 
                                    { "type": "postback", "title": "Sí", "payload": "Si" },
                                    {"type": "postback", "title": "No", "payload": "No"}
                                ]}}}}
                    },
                    { "type": 0, "speech": "" }
                ]
            }

        


    
    if intentName == "bytebot.avb.seleccion.documento-doc.digitado-canal.digitado-token":      
        #Parámetros del contexto
        contexts = result.get("contexts")
        last_context = contexts[len(contexts)-1] 
        parameters_context = last_context["parameters"]
        producto = parameters_context.get("producto")  

        #Parámetros normales
        parameters = result.get("parameters")
        token = parameters.get("number")
        documento = 74563192
        r_clientes=requests.get('http://181.177.228.114:5001/clientes/' + str(documento))
        json_object_clientes = r_clientes.json()
        nombre = json_object_clientes["result"]["clientes"]["cliente"]
        r=requests.get('http://181.177.228.114:5000/validatoken/' + str(token))
        json_object = r.json()
        acceso = json_object["result"]["codigo"]

        if acceso == "0":
            speech = "El código es incorrecto 😓. ¿Deseas qué te reenvíe el código?"
            return {
                "speech": speech,
                "messages": [
                    { "type": 4, "platform": "facebook", "payload": { "facebook": { "attachment": { "type": "template", "payload": { "template_type": "button", "text": speech,
                                "buttons": [ 
                                    { "type": "postback", "title": "Sí", "payload": "Si" },
                                    {"type": "postback", "title": "No", "payload": "No"}
                                ]}}}}
                    },
                    { "type": 0, "speech": "" }
                ]
            }
        else:
            primer_nombre = re.split('\s+', nombre)[0]
            speech1 = "✌ Autenticación realizada con éxito ✌"
            speech2 = "Bienvenido " + primer_nombre + "! ✨" 
            r=requests.get('http://181.177.228.114:5000/login/' + str(documento))
            #Recuperando la opción presionada al inicio:
            #r_context = requests.get('http://181.177.228.114:5001/clientes/' + str(documento))

            if producto == "Cuentas":
                debito=json_object_clientes['result']['clientes']['debito']
                cuentas_debito = []
                json_string_inicio_00 = u'{"type": 0,"platform": "facebook","speech": "' + speech1 +  '"}'
                json_string_inicio_0 = u'{"type": 0,"platform": "facebook","speech": "' + speech2 +  '"}'
                json_string_inicio = u'{"type": 0,"platform": "facebook","speech": "Estos son todos tus tipos de cuenta, selecciona alguna :)"}'
                objeto_inicio_00 = json.loads(json_string_inicio_00)
                objeto_inicio_0 = json.loads(json_string_inicio_0)
                objeto_inicio = json.loads(json_string_inicio)
                cuentas_debito.append(objeto_inicio_00)
                cuentas_debito.append(objeto_inicio_0)
                cuentas_debito.append(objeto_inicio)
                objeto = ''
                for i in range(0,len(debito)):
                    json_string = u'{"type": 1,"platform": "facebook","title": "' + str(debito[i]["nombre"]) + '","imageUrl":  "' + str(debito[i]["imageUrl"]) + '","buttons": [{"text": "Seleccionar Cuenta","postback": "' + str(debito[i]["nombre"]) + '"}]}'
                    objeto  = json.loads(json_string)
                    cuentas_debito.append(objeto)

                return {
                    "speech": "hey",
                    "displayText": "hey",
                    "source": "apiai-weather-webhook",
                    "messages": cuentas_debito
                }


            
            #return{
            #    "speech": speech1,
            #    "messages": [  
            #        { "type": 0, "platform": "facebook", "speech": speech1},                  
            #        { "type": 0, "platform": "facebook", "speech": speech2}
            #        #{ "type": 0, "platform": "facebook", "speech": "Por favor, ingresa tu clave de registro de 4 dígitos que te envié :)"}
            #    ]
            #}
    
    if intentName == "bytebot.avb.seleccion.documento-doc.digitado-canal.digitado-respuesta":        
        parameters = result.get("parameters")
        respuesta = parameters.get("respuesta")
        documento = 74563192
        r=requests.get('http://181.177.228.114:5001/clientes/' + str(documento))
        json_object = r.json()
        telefono = json_object["result"]["clientes"]["telefono"]


        if respuesta == "No":
            speech = "Oh ni modo, en caso de que te llegue el mensaje puedes mandármelo o ignorarlo :("
            return {                
                "speech": speech,
                "displayText": speech,
                "source": "bytebot-virtual-agent-webhook"

        }
        elif respuesta == "Si":
            speech = "Ok! Estoy enviando el código de verificación al celular (******" + str(telefono[9:]) + ")"
            #r_token=requests.get('http://181.177.228.114:5000/enviatoken/' + str(telefono))
            return{
                "speech": speech,
                "messages": [                    
                    { "type": 0, "platform": "facebook", "speech": speech},
                    { "type": 0, "platform": "facebook", "speech": "Por favor, ingresa tu clave de registro de 4 dígitos que te envié :)"}
                ]
            }
        else:
            speech = "Ya nos salimos del tema :("
            return{
                "speech": speech,
                "messages": [                    
                    { "type": 0, "platform": "facebook", "speech": speech}
                ]
            }

    if intentName == "bytebot.avb.consultar.cuentas":
        #Verificación: ¿El estado de la tabla BBOTSEFAC es true o false?        
        verificacion = verificacion()
        
        if int(verificacion) != 0:  
            contexts = result.get("contexts")
            last_context = contexts[len(contexts)-1] 
            parameters_context = last_context["parameters"]
            producto = parameters_context.get("producto")

            r_query = requests.get('http://181.177.228.114:5000/query')
            json_object_query = r_query.json()
            documento = int(json_object_query["result"]["documento"])

            r=requests.get('http://181.177.228.114:5001/clientes/' + str(documento))
            json_object = r.json()


            if producto == "Cuentas":
                debito=json_object['result']['clientes']['debito']
                cuentas_debito = []
                json_string_inicio = u'{"type": 0,"platform": "facebook","speech": "Estos son todos tus tipos de cuenta, selecciona alguna :)"}'
                objeto_inicio = json.loads(json_string_inicio)
                cuentas_debito.append(objeto_inicio)
                objeto = ''
                for i in range(0,len(debito)):
                    json_string = u'{"type": 1,"platform": "facebook","title": "' + str(debito[i]["nombre"]) + '","imageUrl":  "' + str(debito[i]["imageUrl"]) + '","buttons": [{"text": "Seleccionar Cuenta","postback": "' + str(debito[i]["nombre"]) + '"}]}'
                    objeto  = json.loads(json_string)
                    cuentas_debito.append(objeto)

                return {
                    "speech": "hey",
                    "displayText": "hey",
                    "source": "apiai-weather-webhook",
                    "messages": cuentas_debito
                }

        else:
            return verificacion_response

    if intentName == "bytebot.avb.cuenta.debito.sueldo":
        #Verificación: ¿El estado de la tabla BBOTSEFAC es true o false?        
        verificacion = verificacion()
        
        
        if int(verificacion) != 0:  
            contexts = result.get("contexts")
            last_context = contexts[len(contexts)-1] 
            parameters_context = last_context["parameters"]
            debito = parameters_context.get("debito")

            r_query = requests.get('http://181.177.228.114:5000/query')
            json_object_query = r_query.json()
            documento = int(json_object_query["result"]["documento"])            
        

            r=requests.get('http://181.177.228.114:5001/clientes/' + str(documento))
            json_object = r.json()


            if debito == "Cuenta sueldo":
                debito=json_object['result']['clientes']['debito']
                cuentas_sueldo_array = []
                cuentas_sueldo_nombres = []
                cuentas_sueldo_tarjetas_array = []
                cuentas_sueldo_url_array = []
                for i in range(0,len(debito)):
                    if debito[i]['nombre'] == 'Cuenta Sueldo':
                        cuentas_json = debito[i]['cuentas']
                        for j in range(0,len(cuentas_json)):
                            cuentas_sueldo = cuentas_json[j]["alias"]
                            cuentas_sueldo_tarjetas = cuentas_json[j]["numero"]
                            cuentas_sueldo_url = cuentas_json[j]["imageUrl"]
                            cuentas_sueldo_nombres.append(cuentas_sueldo)
                            cuentas_sueldo_tarjetas_array.append(cuentas_sueldo_tarjetas)
                            cuentas_sueldo_url_array.append(cuentas_sueldo_url)
                            json_string = u'{"type": 1,"platform": "facebook","title": "' + str(debito[i]['nombre']) + ' - '+ str(cuentas_sueldo_nombres[j]) + '", "subtitle":"'+str(cuentas_sueldo_tarjetas_array[j]) +'", "imageUrl":  "' + str(cuentas_sueldo_url_array[j]) + '","buttons": [{"text": "Consultar saldos","postback": "Consultar Saldos ' + str(debito[i]["nombre"]) + '"},{"text": "Consultar Movimientos","postback": "Consultar Movmientos ' + str(debito[i]["nombre"]) + '"},{"text": "Análisis","postback": "Análisis ' + str(debito[i]["nombre"]) + '"}]}'
                            objeto  = json.loads(json_string)
                            cuentas_sueldo_array.append(objeto)
                return {
                    "speech": "hey",
                    "displayText": "hey",
                    "source": "apiai-weather-webhook",
                    "messages": cuentas_sueldo_array
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

    if intentName == "bytebot.avb.consultar.cerrar.sesion":     
        documento = 74563192   
        r=requests.get('http://181.177.228.114:5000/logout/' + str(documento))
        json_object = r.json()
        sesion = json_object["result"]["codigo"]

        if  int(sesion) == 1:
            speech1 = "Has cerrado sesión correctamente! "
            speech2 = "Si deseas que te vuelva a ayudar, debes volver a autenticarte :)"
            return {
                "speech": speech1,
                "messages": [                    
                    { "type": 0, "platform": "facebook", "speech": speech1},
                    { "type": 0, "platform": "facebook", "speech": speech2},
                    { "type": 0, "speech": "" }
                ]
            }
        elif int(sesion) == 0:
            speech1 = "Usted nunca inició sesión 😟"            
            return {
                "speech": speech1,
                "messages": [                    
                    { "type": 0, "platform": "facebook", "speech": speech1},
                    { "type": 0, "speech": "" }
                ]
            }

        
        
        
            
            

        
    
    


        
    
    
    
    
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')

















