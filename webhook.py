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
from math import ceil

import time
from datetime import datetime

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

    def formatear_array_fechas(fecha):
        formato_fechas_movimientos = []
        for i in range(0,len(fecha)):
            datetime_object = datetime.strptime(fecha[i], '%b %d %Y %I:%M%p')
            final = str(datetime_object.day).zfill(2) + "/" + str(datetime_object.month).zfill(2) + "/" + str(datetime_object.year)
            formato_fechas_movimientos.append(final)
        return formato_fechas_movimientos

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

    primer_carrusel_cuentas = {"type": 1, "platform": "facebook", "title": "Mantenerte al día con tus cuentas", "subtitle": "Consulta los últimos saldos y movimientos de tus cuentas", "imageUrl": "https://www.bbvacontinental.pe/fbin/mult/cuentas-sueldo-ancho-completo_tcm1105-662879.png", "buttons": [ { "text": "Consultar Cuentas", "postback": "Consultar Cuentas" }]}
    primer_carrusel_cuentas_objeto = json.loads(json.dumps(primer_carrusel_cuentas))
    primer_carrusel_tarjetas = {"type": 1, "platform": "facebook", "title": "Gestiona tus Tarjetas de Crédito", "subtitle": "Movimientos, fecha de pago, pago mínimo y máximo","imageUrl": "https://www.bbvacontinental.pe/fbin/mult/tarjetas-puntos-vida-destacado_tcm1105-646001.png", "buttons": [{"text": "Consultar Tarjetas", "postback": "Consultar Tarjetas"}]}
    primer_carrusel_tarjetas_objeto = json.loads(json.dumps(primer_carrusel_tarjetas))
    primer_carrusel_tipo_cambio = {"type": 1, "platform": "facebook", "title": "Tipo de Cambio", "subtitle": "Obtén el mejor tipo de cambio del mercado", "imageUrl": "https://www.bbvacontinental.pe/fbin/mult/bbva-continental-prestamo-libre-disponibilidad-movil_tcm1105-618544.png","buttons": [{"text": "Consultar Tipo de Cambio","postback": "Consultar Tipo de Cambio"}]}
    primer_carrusel_tipo_cambio_objeto = json.loads(json.dumps(primer_carrusel_tipo_cambio))
    primer_carrusel_cerrar_sesion = {"type": 1,"platform": "facebook","title": "Cerrar Sesión","imageUrl": "https://www.bbva.com/wp-content/uploads/2015/12/cerocomisiones1-1024x423.jpg","buttons": [{"text": "Seleccionar","postback": "Cerrar Sesion"}]}
    primer_carrusel_cerrar_sesion_objeto = json.loads(json.dumps(primer_carrusel_cerrar_sesion))

    if intentName == "bytebot.avb.seleccion.documento":  
        contexts = result.get("contexts")
        last_context = contexts[len(contexts)-1] 
        parameters_context = last_context["parameters"]
        documento_tipo = parameters_context.get("documento")  
        verificacion = verificacion()      
        if int(verificacion) == 1:
            speech = "Ya hay una sesión iniciada, cierra sesión para autenticarte denuevo."
            return {                
                "speech": speech,
                "displayText": speech,
                "source": "bytebot-virtual-agent-webhook"
            }
        else:
            speech = "Por favor,  escribe el número de tu " + documento_tipo
            return {                
                "speech": speech,
                "displayText": speech,
                "source": "bytebot-virtual-agent-webhook"
            }
    
    if intentName == "bytebot.avb.nueva.autenticacion":          
        verificacion = verificacion()      
        if int(verificacion) == 1:
            speech = "Ya hay una sesión iniciada, cierra sesión para autenticarte denuevo."
            return {                
                "speech": speech,
                "displayText": speech,
                "source": "bytebot-virtual-agent-webhook"
            }
        else:            
            return {
                "speech": "verificación", "displayText": "verificación", "source": "apiai-weather-webhook",
                "messages": [
                    { "type": 0, "platform": "facebook", "speech": "Está bien, te autenticaré :) "},
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
        #Parámetros del contexto
        contexts = result.get("contexts")
        last_context = contexts[len(contexts)-1] 
        parameters_context = last_context["parameters"]
        documento = parameters_context.get("phone-number")

        #Parámetros normales
        parameters = result.get("parameters")
        canal = parameters.get("canal")
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
        debito_context = parameters_context.get("debito")
        debito_sueldo = parameters_context.get("debito_sueldo")
        documento = parameters_context.get("phone-number")

        #Parámetros normales
        parameters = result.get("parameters")
        token = parameters.get("number")        
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
            speech1 = "Autenticación realizada con éxito ✌"
            speech2 = "¡Bienvenido " + primer_nombre + "!" 
            speech3 = "¿Qué deseas hacer?" 
            r=requests.get('http://181.177.228.114:5000/login/' + str(documento))
            #Recuperando la opción presionada al inicio:
            #r_context = requests.get('http://181.177.228.114:5001/clientes/' + str(documento))

            if producto == None:
                debito=json_object_clientes['result']['clientes']['debito']
                carrusel = []
                json_string_inicio_00 = u'{"type": 0,"platform": "facebook","speech": "' + speech1 +  '"}'
                json_string_inicio_0 = u'{"type": 0,"platform": "facebook","speech": "' + speech2 +  '"}'
                json_string_inicio = u'{"type": 0,"platform": "facebook","speech": "' + speech3 +  '"}'
                objeto_inicio_00 = json.loads(json_string_inicio_00)
                objeto_inicio_0 = json.loads(json_string_inicio_0)                
                objeto_inicio = json.loads(json_string_inicio)
                carrusel.append(objeto_inicio_00)
                carrusel.append(objeto_inicio_0)
                carrusel.append(objeto_inicio)
                carrusel.append(primer_carrusel_cuentas_objeto)
                carrusel.append(primer_carrusel_tarjetas_objeto)
                carrusel.append(primer_carrusel_tipo_cambio_objeto)
                carrusel.append(primer_carrusel_cerrar_sesion_objeto)
                
                #carrusel.append(objeto_inicio)
                
                return {
                    "speech": "hey",
                    "displayText": "hey",
                    "source": "apiai-weather-webhook",
                    "messages": carrusel
                }

            if producto == "Cuentas" or debito_sueldo != None or debito_context != None :
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
        #Parámetros del contexto
        contexts = result.get("contexts")
        last_context = contexts[len(contexts)-1] 
        parameters_context = last_context["parameters"]        
        documento = parameters_context.get("phone-number")

        # Parámetros normales
        parameters = result.get("parameters")
        respuesta = parameters.get("respuesta")
        
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

    if intentName == "bytebot.avb.cuenta.debito.tipos":
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

            '''
            if debito == "Cuenta Sueldo":
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
                            json_string = u'{"type": 1,"platform": "facebook","title": "' + str(debito[i]['nombre']) + ' - '+ str(cuentas_sueldo_nombres[j]) + '", "subtitle":"'+str(cuentas_sueldo_tarjetas_array[j]) +'", "imageUrl":  "' + str(cuentas_sueldo_url_array[j]) + '","buttons": [{"text": "Consultar saldos","postback": "Consultar Saldos ' + str(debito[i]["nombre"]) + '"},{"text": "Consultar Movimientos","postback": "Consultar Movimientos ' + str(debito[i]["nombre"]) + '"},{"text": "Análisis","postback": "Análisis ' + str(debito[i]["nombre"]) + '"}]}'
                            objeto  = json.loads(json_string)
                            cuentas_sueldo_array.append(objeto)
                return {
                    "speech": "hey",
                    "displayText": "hey",
                    "source": "apiai-weather-webhook",
                    "messages": cuentas_sueldo_array
                }
            elif debito == "Cuenta Ahorros":
                debito=json_object['result']['clientes']['debito']
                cuentas_ahorro_array = []
                cuentas_ahorro_nombres = []
                cuentas_ahorro_tarjetas_array = []
                cuentas_ahorro_url_array = []
                for i in range(0,len(debito)): 
                    if debito[i]['nombre'] == 'Cuenta Ahorros':
                        cuentas_json = debito[i]['cuentas']
                        for j in range(0,len(cuentas_json)):
                            cuentas_ahorro = cuentas_json[j]["alias"]
                            cuentas_ahorro_tarjetas = cuentas_json[j]["numero"]
                            cuentas_ahorro_url = cuentas_json[j]["imageUrl"]
                            cuentas_ahorro_nombres.append(cuentas_ahorro)
                            cuentas_ahorro_tarjetas_array.append(cuentas_ahorro_tarjetas)
                            cuentas_ahorro_url_array.append(cuentas_ahorro_url)
                            json_string = u'{"type": 1,"platform": "facebook","title": "' + str(cuentas_ahorro_nombres[j]) + '", "subtitle":"'+str(cuentas_ahorro_tarjetas_array[j]) +'", "imageUrl":  "' + str(cuentas_ahorro_url_array[j]) + '","buttons": [{"text": "Consultar saldos","postback": "Consultar Saldos ' + str(debito[i]["nombre"]) + '"},{"text": "Consultar Movimientos","postback": "Consultar Movmientos ' + str(debito[i]["nombre"]) + '"},{"text": "Análisis","postback": "Análisis ' + str(debito[i]["nombre"]) + '"}]}'
                            objeto  = json.loads(json_string)
                            cuentas_ahorro_array.append(objeto)
                return {
                    "speech": "hey",
                    "displayText": "hey",
                    "source": "apiai-weather-webhook",
                    "messages": cuentas_ahorro_array
                }
            else:
                speech = "Qué extraño.. no tengo configurado este tipo de tarjeta en mi sistema :("
                return{
                    "speech": speech,
                    "messages": [
                        { "type": 0, "platform": "facebook", "speech": speech} 
                        ]
                }
            '''
            
            debito_df=json_object['result']['clientes']['debito']
            cuentas_sueldo = ''
            cuentas_sueldo_tarjetas = ''
            cuentas_sueldo_url = ''
            cuentas_sueldo_array = []
            cuentas_sueldo_nombres = []
            cuentas_sueldo_tarjetas_array = []
            cuentas_sueldo_url_array = []
            objeto = ''
            i = 0
            for i in range(0,len(debito_df)):
                if debito_df[i]['nombre'] == debito:
                    cuentas_json = debito_df[i]['cuentas']
                    speech = "Estas son tus  " + str(debito_df[i]['nombre']) + ". Puedes consultar las que desees :)"                    
                    json_string_0 = u'{"type": 0,"platform": "facebook","speech":"'+ speech +'"}'
                    objeto_0 = json.loads(json_string_0)
                    cuentas_sueldo_array.append(objeto_0)
                    for j in range(0,len(cuentas_json)):
                        cuentas_sueldo = cuentas_json[j]["alias"]
                        cuentas_sueldo_tarjetas = cuentas_json[j]["numero"]
                        cuentas_sueldo_url = cuentas_json[j]["imageUrl"]
                        cuentas_sueldo_nombres.append(cuentas_sueldo)
                        cuentas_sueldo_tarjetas_array.append(cuentas_sueldo_tarjetas)
                        cuentas_sueldo_url_array.append(cuentas_sueldo_url)
                        json_string = u'{"type": 1,"platform": "facebook","title": "' + str(debito_df[i]['nombre']) + ' - '+ str(cuentas_sueldo_nombres[j]) + '", "subtitle":"'+str(cuentas_sueldo_tarjetas_array[j]) +'", "imageUrl":  "' + str(cuentas_sueldo_url_array[j]) + '","buttons": [{"text": "Consultar saldos","postback": "Consultar Saldos ' + str(debito_df[i]['nombre']) + " " + str(cuentas_sueldo_nombres[j]) + '"},{"text": "Consultar Movimientos","postback": "Consultar Movimientos ' + str(debito_df[i]['nombre']) + " " + str(cuentas_sueldo_nombres[j]) + '"},{"text": "Análisis","postback": "Generar Grafica ' + str(debito_df[i]['nombre']) + " " + str(cuentas_sueldo_nombres[j]) + '"}]}'                        
                        objeto  = json.loads(json_string)                        
                        cuentas_sueldo_array.append(objeto)
            return {
                    "speech": debito_df[i]['nombre'],
                    "displayText": "Cancelado",
                    "source": "apiai-weather-webhook",
                    "messages": cuentas_sueldo_array
            }

        else:
            return verificacion_response

    if intentName == "bytebot.avb.cuenta.debito.tipos.saldos":
        #Verificación: ¿El estado de la tabla BBOTSEFAC es true o false?        
        verificacion = verificacion()
        
        
        if int(verificacion) != 0:  
            contexts = result.get("contexts")
            last_context = contexts[len(contexts)-1] 
            parameters_context = last_context["parameters"]
            debito_context = parameters_context.get("debito")
            debito_sueldo = parameters_context.get("debito_sueldo")

            if debito_context == None or debito_context == "":
                if debito_sueldo == "Gastos Personales" or debito_sueldo == "Laboral":
                    debito_context = "Cuenta Sueldo"
                else:
                    debito_context = "Cuenta Ahorros"

            if debito_sueldo == "Gastos Personales" or debito_sueldo == "Laboral":
                debito_context = "Cuenta Sueldo"
            else:
                debito_context = "Cuenta Ahorros"
            

            r_query = requests.get('http://181.177.228.114:5000/query')
            json_object_query = r_query.json()
            documento = int(json_object_query["result"]["documento"])            
        

            r=requests.get('http://181.177.228.114:5001/clientes/' + str(documento))
            json_object = r.json()

            debito=json_object['result']['clientes']['debito']
            cuentas_tipo_saldo_array = []
            cuentas_tipo_saldo_nombres = []
            cuentas_tipo_saldo_tarjetas_array = []
            cuentas_tipo_saldo_url_array = []
            cuentas_tipo_saldo_saldos_array = []
            cuentas_tipo_saldo_monedas_array = []
            for i in range(0,len(debito)): 
                if debito[i]['nombre'] == debito_context:
                    cuentas_json = debito[i]['cuentas']
                    for j in range(0,len(cuentas_json)):
                        if cuentas_json[j]["alias"] == debito_sueldo:                            
                            cuentas_tipo_saldo = cuentas_json[j]["alias"]
                            cuentas_tipo_saldo_tarjetas = cuentas_json[j]["numero"]
                            cuentas_tipo_saldo_url = cuentas_json[j]["imageUrl"]
                            cuentas_tipo_saldo_saldos = cuentas_json[j]["saldo"]
                            cuentas_tipo_saldo_monedas = cuentas_json[j]["moneda"]
                            cuentas_tipo_saldo_nombres.append(cuentas_tipo_saldo)
                            cuentas_tipo_saldo_tarjetas_array.append(cuentas_tipo_saldo_tarjetas)
                            cuentas_tipo_saldo_url_array.append(cuentas_tipo_saldo_url)
                            cuentas_tipo_saldo_saldos_array.append(cuentas_tipo_saldo_saldos)
                            cuentas_tipo_saldo_monedas_array.append(cuentas_tipo_saldo_monedas)
                            speech = "Tu saldo actual es:"
                            speech_saldo_1 = str(cuentas_tipo_saldo_monedas_array[0]) + " " + str(cuentas_tipo_saldo_saldos_array[0]) 
                            speech_saldo_2 = str(debito[i]['nombre']) + " - " + str(cuentas_tipo_saldo_nombres[0])
                            speech_saldo_3 = str(cuentas_tipo_saldo_tarjetas_array[0])
                            #json_string = u'{"type": 1,"platform": "facebook","title": "' + str(cuentas_tipo_saldo_nombres[j]) + '", "subtitle":"'+str(cuentas_tipo_saldo_tarjetas_array[j]) +'", "imageUrl":  "' + str(cuentas_tipo_saldo_url_array[j]) + '","buttons": [{"text": "Consultar saldos","postback": "Consultar Saldos ' + str(debito[i]["nombre"]) + '"},{"text": "Consultar Movimientos","postback": "Consultar Movmientos ' + str(debito[i]["nombre"]) + '"},{"text": "Análisis","postback": "Análisis ' + str(debito[i]["nombre"]) + '"}]}'
                            json_string_0 = u'{"type": 0,"platform": "facebook","speech":"'+ speech +'"}'
                            #json_string = u'{"type": 0,"platform": "facebook","speech":"'+ speech_saldo_1 + "\n" + speech_saldo_2  + "\n" + speech_saldo_3 +'"}'
                            #json_string = u'{ "type": 4, "platform": "facebook", "payload": { "facebook": { "attachment": { "type": "template", "payload": { "template_type": "button", "text": "'+ speech_saldo_1 + "\n" + speech_saldo_2  + "\n" + speech_saldo_3 +'","buttons": [{ "type": "postback", "title": "Generar Gráfica", "payload": "Generar Grafica ' + str(debito[i]['nombre']) + " " + str(cuentas_tipo_saldo_nombres[0]) + '" },{"type": "postback", "title": "Consultar Movimientos", "payload": "Consultar Movimientos ' + str(debito[i]['nombre']) + " " + str(cuentas_tipo_saldo_nombres[0])  +'"}]}}}} }'
                            json_string = u'{ "type": 4, "platform": "facebook", "payload": { "facebook": { "attachment": { "type": "template", "payload": { "template_type": "button", "text": "'+ speech_saldo_1 + "\n" + speech_saldo_2  + "\n" + speech_saldo_3 +'","buttons": [{"type": "postback", "title": "Consultar Movimientos", "payload": "Consultar Movimientos ' + str(debito[i]['nombre']) + " " + str(cuentas_tipo_saldo_nombres[0])  +'"}]}}}} }'
                            objeto_0 = json.loads(json_string_0)
                            objeto  = json.loads(json_string,strict=False)
                            cuentas_tipo_saldo_array.append(objeto_0) 
                            cuentas_tipo_saldo_array.append(objeto)   
            return {
                "speech": "Cancelado :/",
                "displayText": "Cancelado",
                "source": "apiai-weather-webhook",
                "messages": cuentas_tipo_saldo_array
            } 
            

        else:
            return verificacion_response
    
    if intentName == "bytebot.avb.cuenta.debito.tipos.movimientos":
        #Verificación: ¿El estado de la tabla BBOTSEFAC es true o false?        
        verificacion = verificacion()
        
        
        if int(verificacion) != 0:  
            contexts = result.get("contexts")
            last_context = contexts[len(contexts)-1] 
            parameters_context = last_context["parameters"]
            debito_context = parameters_context.get("debito")
            debito_sueldo = parameters_context.get("debito_sueldo")

            if debito_context == None or debito_context == "":
                if debito_sueldo == "Gastos Personales" or debito_sueldo == "Laboral":
                    debito_context = "Cuenta Sueldo"
                else:
                    debito_context = "Cuenta Ahorros"

            if debito_sueldo == "Gastos Personales" or debito_sueldo == "Laboral":
                    debito_context = "Cuenta Sueldo"
            else:
                debito_context = "Cuenta Ahorros"

            r_query = requests.get('http://181.177.228.114:5000/query')
            json_object_query = r_query.json()
            documento = int(json_object_query["result"]["documento"])            
        

            r=requests.get('http://181.177.228.114:5001/clientes/' + str(documento))
            json_object = r.json()

            #speech = "Estos son los movimientos de tu cuenta " + debito_sueldo
            #json_string_inicio = u'{ "type": 0, "platform": "facebook", "speech": "Estos son los movimientos de tu cuenta ' + debito_sueldo  + '"}'
            #objeto_inicio = json.loads(json_string_inicio, strict = False)

            
            debito=json_object['result']['clientes']['debito']
            cuentas_tipo_movimiento_array = []
            #cuentas_tipo_movimiento_array.append(objeto_inicio)  
            for i in range(0,len(debito)): 
                if debito[i]['nombre'] == debito_context:
                    cuentas_json = debito[i]['cuentas']        
                    for j in range(0,len(cuentas_json)):
                        if cuentas_json[j]["alias"] == debito_sueldo:
                            if len(cuentas_json[j]["movimientos_dias"]) == 1:
                                numero_pantallas = 1
                                solo_carrusel = True
                                indice_final_pagina = 1
                            elif len(cuentas_json[j]["movimientos_dias"])%2 == 0:
                                solo_carrusel = False
                                numero_pantallas = ceil(len(cuentas_json[j]["movimientos_dias"])/4)
                                if len(cuentas_json[j]["movimientos_monto"]) > 4:
                                    indice_final_pagina = 0 + 4
                                else:
                                    indice_final_pagina =  len(cuentas_json[j]["movimientos_monto"]) 
                            else:
                                numero_pantallas = ceil(len(cuentas_json[j]["movimientos_dias"])/3)
                                solo_carrusel = False
                                if len(cuentas_json[j]["movimientos_monto"]) > 3:
                                    indice_final_pagina = 0 + 3
                                else:
                                    indice_final_pagina =  len(cuentas_json[j]["movimientos_monto"]) 
                                
                            #numero_pantallas = ceil(len(cuentas_json[j]["movimientos_dias"])/4)
                            cuentas_tipo_movimiento_monedas = cuentas_json[j]["moneda"]
                            cuentas_tipo_movimiento_dias = formatear_array_fechas(cuentas_json[j]["movimientos_dias"])
                            cuentas_tipo_movimiento_monto = cuentas_json[j]["movimientos_monto"]   
                            cuentas_tipo_movimiento_descripcion = cuentas_json[j]["movimientos_descripcion"]                            
                            for k in range(0,indice_final_pagina):
                                if float(cuentas_tipo_movimiento_monto[k]) > 0:
                                    if solo_carrusel:
                                        json_string = u'{ "type": 1, "platform": "facebook", "title": "' + cuentas_tipo_movimiento_monedas + " " + cuentas_tipo_movimiento_monto[k] + '", "subtitle": "' + cuentas_tipo_movimiento_descripcion[k] + cuentas_tipo_movimiento_dias[k] +'","imageUrl": "https://raw.githubusercontent.com/idusertbs/bytebot-agente-virtual-bancario-webhook/master/bytebot_agente_bancario_assets/plus_carrusel.png", "buttons": [] }'
                                    else: 
                                        json_string = u'{"title": "' + cuentas_tipo_movimiento_monedas + " " + cuentas_tipo_movimiento_monto[k] + '", "subtitle": "' + cuentas_tipo_movimiento_descripcion[k] + cuentas_tipo_movimiento_dias[k] +'","image_url": "https://raw.githubusercontent.com/idusertbs/bytebot-agente-virtual-bancario-webhook/master/bytebot_agente_bancario_assets/plus.png"}'
                                else:
                                    if solo_carrusel:
                                        json_string = u'{ "type": 1, "platform": "facebook", "title": "' + cuentas_tipo_movimiento_monedas + " " + cuentas_tipo_movimiento_monto[k] + '", "subtitle": "' + cuentas_tipo_movimiento_descripcion[k] + cuentas_tipo_movimiento_dias[k] +'","imageUrl": "https://raw.githubusercontent.com/idusertbs/bytebot-agente-virtual-bancario-webhook/master/bytebot_agente_bancario_assets/minus_carrusel.png", "buttons": [] }'
                                    else: 
                                        json_string = u'{"title": "' + cuentas_tipo_movimiento_monedas + " " + cuentas_tipo_movimiento_monto[k] + '", "subtitle": "' + cuentas_tipo_movimiento_descripcion[k] + cuentas_tipo_movimiento_dias[k] +'","image_url": "https://raw.githubusercontent.com/idusertbs/bytebot-agente-virtual-bancario-webhook/master/bytebot_agente_bancario_assets/minus.png"}'

                                    
                                    
                                objeto  = json.loads(json_string,strict=False)
                                cuentas_tipo_movimiento_array.append(objeto)   


            if numero_pantallas == 1:
                button_ver_mas = []
            else: 
                button_ver_mas = [{"title": "+ Movimientos", "type": "postback", "payload": "pagina2"} ]

            if solo_carrusel:
                return {
                    "speech": "Cancelado :/",
                    "displayText": "heyo",
                    "source": "apiai-weather-webhook",
                    "messages": 
                        cuentas_tipo_movimiento_array
                }
            else: 
                return {
                "speech": "Cancelado :/",
                "displayText": "heyo",
                "source": "apiai-weather-webhook",
                "messages": [
                    {"type": 0, "platform": "facebook", "speech": "Estos son los movimientos de tu cuenta " + debito_sueldo },
                    {"type": 4, "platform": "facebook", "payload": { "facebook": { "attachment": { "type": "template", "payload": { "template_type": "list", "top_element_style": "compact",
                  "elements": 
                    cuentas_tipo_movimiento_array
                  ,
                  "buttons": button_ver_mas
                    }}}}}
                ]

            } 


            
            

        else:
            return verificacion_response


    if intentName == "bytebot.avb.cuenta.sueldo.grafica":
        #Verificación: ¿El estado de la tabla BBOTSEFAC es true o false?        
        verificacion = verificacion()
        
        
        if int(verificacion) != 0:  
            contexts = result.get("contexts")
            last_context = contexts[len(contexts)-1] 
            parameters_context = last_context["parameters"]
            debito_context = parameters_context.get("debito")
            debito_sueldo = parameters_context.get("debito_sueldo")      

            if debito_context == None or debito_context == "":
                if debito_sueldo == "Gastos Personales" or debito_sueldo == "Laboral":
                    debito_context = "Cuenta Sueldo"
                else:
                    debito_context = "Cuenta Ahorros"

            if debito_sueldo == "Gastos Personales" or debito_sueldo == "Laboral":
                debito_context = "Cuenta Sueldo"
            else:
                debito_context = "Cuenta Ahorros"      

            r_query = requests.get('http://181.177.228.114:5000/query')
            json_object_query = r_query.json()
            documento = int(json_object_query["result"]["documento"])            
        

            r=requests.get('http://181.177.228.114:5001/clientes/' + str(documento))
            json_object = r.json()

            debito=json_object['result']['clientes']['debito']
            cuentas_tipo_saldo_array = []
            cuentas_tipo_saldo_nombres = []
            cuentas_tipo_saldo_tarjetas_array = []
            cuentas_tipo_saldo_url_array = []
            cuentas_tipo_saldo_saldos_array = []
            cuentas_tipo_saldo_monedas_array = []
            url_imagen = ''
            for i in range(0,len(debito)): 
                if debito[i]['nombre'] == debito_context:
                    cuentas_json = debito[i]['cuentas']
                    for j in range(0,len(cuentas_json)):
                        if cuentas_json[j]["alias"] == debito_sueldo:
                            cuentas_tipo_saldo = cuentas_json[j]["alias"]
                            cuentas_tipo_saldo_tarjetas = cuentas_json[j]["numero"]
                            cuentas_tipo_saldo_url = cuentas_json[j]["imageUrl"]
                            cuentas_tipo_saldo_saldos = cuentas_json[j]["saldo"]
                            cuentas_tipo_saldo_monedas = cuentas_json[j]["moneda"]
                            cuentas_tipo_saldo_movimientos_dias = cuentas_json[j]["movimientos_dias"]
                            cuentas_tipo_saldo_movimientos_monto = cuentas_json[j]["movimientos_monto"]
                            cuentas_tipo_saldo_nombres.append(cuentas_tipo_saldo)
                            cuentas_tipo_saldo_tarjetas_array.append(cuentas_tipo_saldo_tarjetas)
                            cuentas_tipo_saldo_url_array.append(cuentas_tipo_saldo_url)
                            cuentas_tipo_saldo_saldos_array.append(cuentas_tipo_saldo_saldos)
                            cuentas_tipo_saldo_monedas_array.append(cuentas_tipo_saldo_monedas)
                            url_final = 'http://181.177.228.114:5000/grafica/' + str(cuentas_tipo_saldo_movimientos_dias) +'/'+ str(cuentas_tipo_saldo_movimientos_monto) +'/' + cuentas_tipo_saldo_saldos +'/'+ str(documento) + '/Cuentas/' + debito_context + '/' + debito_sueldo +'/' + cuentas_tipo_saldo_monedas
                            url_final_final = url_final.replace(" ", "%20")
                            r_grafica = requests.get(url_final_final)
                            json_url_imagen = r_grafica.json()
                            url_imagen = json_url_imagen["result"]["url"]

            ultima_fecha  = cuentas_tipo_saldo_movimientos_dias[0]
            primera_fecha = cuentas_tipo_saldo_movimientos_dias[len(cuentas_tipo_saldo_movimientos_dias) - 1]
            datetime_object = datetime.strptime(ultima_fecha, '%b %d %Y %I:%M%p')
            datetime_object_2 = datetime.strptime(primera_fecha, '%b %d %Y %I:%M%p')
            fecha_final_formateada = str(datetime_object.day).zfill(2) + "/" + str(datetime_object.month).zfill(2) + "/" + str(datetime_object.year)
            fecha_inicial_formateada = str(datetime_object_2.day).zfill(2) + "/" + str(datetime_object_2.month).zfill(2) + "/" + str(datetime_object_2.year)
            
            

            return {
                "speech": "-",
                "displayText": "-",
                "source": "apiai-weather-webhook",
                "messages": [
                    {
                        "type": 0,
                        "platform": "facebook",
                        "speech": "Esta es una gráfica de la evolución de tu saldo a lo largo del mes.\nDesde el " + fecha_inicial_formateada + " al " + fecha_final_formateada
                    },
                    {
                        "type": 3,
                        "platform": "facebook",
                        "imageUrl": url_imagen
                    }
                ]

            }
                            
            

        else:
            return verificacion_response

    if intentName == "bytebot.avb.cuenta.debito.tipos.movimientos-next":
        #Verificación: ¿El estado de la tabla BBOTSEFAC es true o false?        
        verificacion = verificacion()
        
        
        if int(verificacion) != 0:  
            contexts = result.get("contexts")
            last_context = contexts[len(contexts)-1] 
            parameters_context = last_context["parameters"]
            debito_context = parameters_context.get("debito")
            debito_sueldo = parameters_context.get("debito_sueldo")
            pagina = int(parameters_context.get("paginas")[6:])

            if debito_context == None or debito_context == "":
                if debito_sueldo == "Gastos Personales" or debito_sueldo == "Laboral":
                    debito_context = "Cuenta Sueldo"
                else:
                    debito_context = "Cuenta Ahorros"
            
            if debito_sueldo == "Gastos Personales" or debito_sueldo == "Laboral":
                    debito_context = "Cuenta Sueldo"
            else:
                debito_context = "Cuenta Ahorros"

            r_query = requests.get('http://181.177.228.114:5000/query')
            json_object_query = r_query.json()
            documento = int(json_object_query["result"]["documento"])            
        

            r=requests.get('http://181.177.228.114:5001/clientes/' + str(documento))
            json_object = r.json()

            debito=json_object['result']['clientes']['debito']
            cuentas_tipo_movimiento_array = []
            for i in range(0,len(debito)): 
                if debito[i]['nombre'] == debito_context:
                    cuentas_json = debito[i]['cuentas']        
                    for j in range(0,len(cuentas_json)):
                        if cuentas_json[j]["alias"] == debito_sueldo:
                            if len(cuentas_json[j]["movimientos_dias"])%2 == 0:
                                numero_pantallas = ceil(len(cuentas_json[j]["movimientos_dias"])/4)
                                indice_inicio_pagina = 5*(pagina-1)-(pagina-1)
                                if len(cuentas_json[j]["movimientos_monto"]) - (indice_inicio_pagina+1) > 4:
                                    indice_final_pagina = indice_inicio_pagina + 4 
                                else:
                                    indice_final_pagina =  len(cuentas_json[j]["movimientos_monto"]) 
                            else:
                                numero_pantallas = ceil(len(cuentas_json[j]["movimientos_dias"])/3) 
                                indice_inicio_pagina = 4*(pagina-1)-(pagina-1)
                                if len(cuentas_json[j]["movimientos_monto"]) - (indice_inicio_pagina+1) > 3:
                                    indice_final_pagina = indice_inicio_pagina + 3
                                else:
                                    indice_final_pagina =  len(cuentas_json[j]["movimientos_monto"]) 

                            cuentas_tipo_movimiento_monedas = cuentas_json[j]["moneda"]
                            cuentas_tipo_movimiento_dias = formatear_array_fechas(cuentas_json[j]["movimientos_dias"])
                            cuentas_tipo_movimiento_monto = cuentas_json[j]["movimientos_monto"]
                            cuentas_tipo_movimiento_descripcion = cuentas_json[j]["movimientos_descripcion"] 
                            #for k in range(0,len(cuentas_tipo_movimiento_monto)):
                            for k in range(indice_inicio_pagina,indice_final_pagina):
                                if float(cuentas_tipo_movimiento_monto[k]) > 0:
                                    json_string = u'{"title": "' + cuentas_tipo_movimiento_monedas + " " + cuentas_tipo_movimiento_monto[k] + '", "subtitle": "' + cuentas_tipo_movimiento_descripcion[k] + cuentas_tipo_movimiento_dias[k] +'","image_url": "https://raw.githubusercontent.com/idusertbs/bytebot-agente-virtual-bancario-webhook/master/bytebot_agente_bancario_assets/plus.png"}'
                                else:
                                    json_string = u'{"title": "' + cuentas_tipo_movimiento_monedas + " " + cuentas_tipo_movimiento_monto[k] + '", "subtitle": "' + cuentas_tipo_movimiento_descripcion[k] + cuentas_tipo_movimiento_dias[k] +'","image_url": "https://raw.githubusercontent.com/idusertbs/bytebot-agente-virtual-bancario-webhook/master/bytebot_agente_bancario_assets/minus.png"}'
                                    
                                objeto  = json.loads(json_string,strict=False)
                                cuentas_tipo_movimiento_array.append(objeto)   


            if numero_pantallas == pagina:
                button_ver_mas = []
            else: 
                button_ver_mas = [{"title": "+ Movimientos", "type": "postback", "payload": "pagina" + str(pagina+1)} ]

            return {
                "speech": "Cancelado :/",
                "displayText": "Cancelado :/",
                "source": "apiai-weather-webhook",
                "messages": [
                    {"type": 4, "platform": "facebook", "payload": { "facebook": { "attachment": { "type": "template", "payload": { "template_type": "list", "top_element_style": "compact",
                  "elements": 
                    cuentas_tipo_movimiento_array
                  ,
                  "buttons": button_ver_mas
                    }}}}}
                ]

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
        r_query = requests.get('http://181.177.228.114:5000/query')
        json_object_query = r_query.json()
        haysesion = int(json_object_query["result"]["codigo"])

        if haysesion == 0:
            documento = 99999999
        else:
            documento = int(json_object_query["result"]["documento"])

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

















