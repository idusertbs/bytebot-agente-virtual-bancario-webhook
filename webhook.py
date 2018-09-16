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
from datetime import datetime, timedelta

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

    #Formatea a número con formato millar.
    #format_numero = lambda x:'{:,}'.format(x)

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

    def past_days_from_current_day(number_of_days):
        now = datetime.today()
        movimiento_dias = []
        for i in range(0,number_of_days):
            past = now - timedelta(days=i)    
            movimiento_dias.append(past.strftime("%b %d %Y  10:22PM"))
        return(movimiento_dias)

    def group_two_lists_by_first_list(keys, values):
        values = list(map(float,values))
        #dictionary = dict(zip(keys, values))

        class DictList(dict):
            def __setitem__(self, key, value):
                try:
                    # Assumes there is a list on the key
                    self[key].append(value) 
                except KeyError: # if fails because there is no key
                    super(DictList, self).__setitem__(key, value)
                except AttributeError: # if fails because it is not a list
                    super(DictList, self).__setitem__(key, [self[key], value])

        data = DictList()
        for i in range(0, len(keys)):
            data[keys[i]] = values[i]

        values_group = list(data.values())
        keys = list(data.keys())

        values_sum = []
        for i in range(0,len(values_group)):
            if type(values_group[i]) == float or type(values_group[i]) == int:
                values_sum.append(values_group[i])
            else:
                values_sum.append(sum(values_group[i]))
        return keys, list(map(str,values_sum))


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
        name_context = last_context["name"]
        if name_context == "generic":
            last_context = contexts[len(contexts)-2]  
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
        name_context = last_context["name"]
        if name_context == "generic":
            last_context = contexts[len(contexts)-2]  
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
            r_token=requests.get('http://181.177.228.114:5000/enviatoken/' + str(telefono))
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
        name_context = last_context["name"]
        if name_context == "generic":
            last_context = contexts[len(contexts)-2]   
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
                    json_string = u'{"type": 1,"platform": "facebook","title": "' + str(debito[i]["nombre"]) + '","subtitle":  "' + str(debito[i]["descripcion"]) + '","imageUrl":  "' + str(debito[i]["imageUrl"]) + '","buttons": [{"text": "Seleccionar Cuenta","postback": "' + str(debito[i]["nombre"]) + '"}]}'
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
        name_context = last_context["name"]
        if name_context == "generic":
            last_context = contexts[len(contexts)-2]   
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
            r_token=requests.get('http://181.177.228.114:5000/enviatoken/' + str(telefono))
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

    if intentName == "bytebot.avb.consultar":
        #Verificación: ¿El estado de la tabla BBOTSEFAC es true o false?        
        verificacion = verificacion()
        
        if int(verificacion) != 0:  
            contexts = result.get("contexts")
            last_context = contexts[len(contexts)-1]
            name_context = last_context["name"]
            if name_context == "generic":
                last_context = contexts[len(contexts)-2]   
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
                    json_string = u'{"type": 1,"platform": "facebook","title": "' + str(debito[i]["nombre"]) + '","subtitle":  "' + str(debito[i]["descripcion"]) + '","imageUrl":  "' + str(debito[i]["imageUrl"]) + '","buttons": [{"text": "Seleccionar Cuenta","postback": "' + str(debito[i]["nombre"]) + '"}]}'
                    objeto  = json.loads(json_string)
                    cuentas_debito.append(objeto)

                return {
                    "speech": "hey",
                    "displayText": "hey",
                    "source": "apiai-weather-webhook",
                    "messages": cuentas_debito
                }

            if producto == "Tarjetas":
                credito=json_object['result']['clientes']['credito']
                tarjetas_credito = []
                json_string_inicio = u'{"type": 0,"platform": "facebook","speech": "Estas son tus tarjetas de crédito"}'
                objeto_inicio = json.loads(json_string_inicio)
                tarjetas_credito.append(objeto_inicio)
                objeto = ''
                for i in range(0,len(credito)):
                    json_string = u'{"type": 1,"platform": "facebook","title": "' + str(credito[i]["nombre"]) + '","subtitle": "' + str(credito[i]["numero"])  +'","imageUrl": "' + str(credito[i]["imageUrl"]) + '","buttons": [{"text": "Consultar Saldo","postback": "Consultar Saldo ' + str(credito[i]["nombre"]) + '"},{"text": "Próximo Pago","postback": "Información Próximo Pago ' + str(credito[i]["nombre"]) + '"},{"text": "Análisis por Consumo","postback": "Análisis por Consumo ' + str(credito[i]["nombre"]) + '"}]}'
                    objeto  = json.loads(json_string)
                    tarjetas_credito.append(objeto)

                return {
                    "speech": "hey",
                    "displayText": "hey",
                    "source": "apiai-weather-webhook",
                    "messages": tarjetas_credito
                }

        else:
            return verificacion_response

    if intentName == "bytebot.avb.cuenta.debito.tipos":
        #Verificación: ¿El estado de la tabla BBOTSEFAC es true o false?        
        verificacion = verificacion()
        
        
        if int(verificacion) != 0:  
            contexts = result.get("contexts")
            last_context = contexts[len(contexts)-1] 
            name_context = last_context["name"]
            if name_context == "generic":
                last_context = contexts[len(contexts)-2]  
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
                            json_string = u'{"type": 1,"platform": "facebook","title": "' + str(debito[i]['nombre']) + ' - '+ str(cuentas_sueldo_nombres[j]) + '", "subtitle":"'+str(cuentas_sueldo_tarjetas_array[j]) +'", "imageUrl":  "' + str(cuentas_sueldo_url_array[j]) + '","buttons": [{"text": "Consultar saldos","postback": "Consultar Saldos ' + str(debito[i]["nombre"]) + '"},{"text": "Ver Movimientos","postback": "Consultar Movimientos ' + str(debito[i]["nombre"]) + '"},{"text": "Análisis","postback": "Análisis ' + str(debito[i]["nombre"]) + '"}]}'
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
                            json_string = u'{"type": 1,"platform": "facebook","title": "' + str(cuentas_ahorro_nombres[j]) + '", "subtitle":"'+str(cuentas_ahorro_tarjetas_array[j]) +'", "imageUrl":  "' + str(cuentas_ahorro_url_array[j]) + '","buttons": [{"text": "Consultar saldos","postback": "Consultar Saldos ' + str(debito[i]["nombre"]) + '"},{"text": "Ver Movimientos","postback": "Consultar Movmientos ' + str(debito[i]["nombre"]) + '"},{"text": "Análisis","postback": "Análisis ' + str(debito[i]["nombre"]) + '"}]}'
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
                    speech = "Estas son tus  " + str(debito_df[i]['nombre']).lower() + ". Puedes consultar las que desees :)"                    
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
                        json_string = u'{"type": 1,"platform": "facebook","title": "' + str(debito_df[i]['nombre']) + ' - '+ str(cuentas_sueldo_nombres[j]) + '", "subtitle":"'+str(cuentas_sueldo_tarjetas_array[j]) +'", "imageUrl":  "' + str(cuentas_sueldo_url_array[j]) + '","buttons": [{"text": "Consultar saldos","postback": "Consultar Saldos ' + str(debito_df[i]['nombre']) + " " + str(cuentas_sueldo_nombres[j]) + '"},{"text": "Ver Movimientos","postback": "Consultar Movimientos ' + str(debito_df[i]['nombre']) + " " + str(cuentas_sueldo_nombres[j]) + '"},{"text": "Análisis","postback": "Generar Grafica ' + str(debito_df[i]['nombre']) + " " + str(cuentas_sueldo_nombres[j]) + '"}]}'                        
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
            name_context = last_context["name"]
            if name_context == "generic":
                last_context = contexts[len(contexts)-2]  
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
                            speech_saldo_1 = str(cuentas_tipo_saldo_monedas_array[0]) + " " + str(format(float("{0:.2f}".format(float(cuentas_tipo_saldo_saldos_array[0]))),',')) 
                            speech_saldo_2 = str(debito[i]['nombre']) + " - " + str(cuentas_tipo_saldo_nombres[0])
                            speech_saldo_3 = str(cuentas_tipo_saldo_tarjetas_array[0])
                            #json_string = u'{"type": 1,"platform": "facebook","title": "' + str(cuentas_tipo_saldo_nombres[j]) + '", "subtitle":"'+str(cuentas_tipo_saldo_tarjetas_array[j]) +'", "imageUrl":  "' + str(cuentas_tipo_saldo_url_array[j]) + '","buttons": [{"text": "Consultar saldos","postback": "Consultar Saldos ' + str(debito[i]["nombre"]) + '"},{"text": "Ver Movimientos","postback": "Consultar Movmientos ' + str(debito[i]["nombre"]) + '"},{"text": "Análisis","postback": "Análisis ' + str(debito[i]["nombre"]) + '"}]}'
                            json_string_0 = u'{"type": 0,"platform": "facebook","speech":"'+ speech +'"}'
                            #json_string = u'{"type": 0,"platform": "facebook","speech":"'+ speech_saldo_1 + "\n" + speech_saldo_2  + "\n" + speech_saldo_3 +'"}'
                            #json_string = u'{ "type": 4, "platform": "facebook", "payload": { "facebook": { "attachment": { "type": "template", "payload": { "template_type": "button", "text": "'+ speech_saldo_1 + "\n" + speech_saldo_2  + "\n" + speech_saldo_3 +'","buttons": [{ "type": "postback", "title": "Generar Gráfica", "payload": "Generar Grafica ' + str(debito[i]['nombre']) + " " + str(cuentas_tipo_saldo_nombres[0]) + '" },{"type": "postback", "title": "Consultar Movimientos", "payload": "Consultar Movimientos ' + str(debito[i]['nombre']) + " " + str(cuentas_tipo_saldo_nombres[0])  +'"}]}}}} }'
                            json_string = u'{ "type": 4, "platform": "facebook", "payload": { "facebook": { "attachment": { "type": "template", "payload": { "template_type": "button", "text": "'+ speech_saldo_2 + "\n" + speech_saldo_3  + "\n" + speech_saldo_1 +'","buttons": [{"type": "postback", "title": "Generar Reporte", "payload": "Generar Reporte ' + str(debito[i]['nombre']) + " " + str(cuentas_tipo_saldo_nombres[0])  +'"},{"type": "postback", "title": "Ver Movimientos", "payload": "Consultar Movimientos ' + str(debito[i]['nombre']) + " " + str(cuentas_tipo_saldo_nombres[0])  +'"}]}}}} }'
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

    if intentName == "bytebot.avb.cuentas.generar.grafica":
        #Verificación: ¿El estado de la tabla BBOTSEFAC es true o false?        
        verificacion = verificacion()
        
        
        if int(verificacion) != 0:  
            contexts = result.get("contexts")
            last_context = contexts[len(contexts)-1]
            name_context = last_context["name"]
            if name_context == "generic":
                last_context = contexts[len(contexts)-2]   
            parameters_context = last_context["parameters"]
            debito_context = parameters_context.get("debito")
            debito_sueldo = parameters_context.get("debito_sueldo")

            r_query = requests.get('http://181.177.228.114:5000/query')
            json_object_query = r_query.json()
            documento = int(json_object_query["result"]["documento"])

            #Generando reporte
            r_reporte = requests.get('http://181.177.228.114:5000/bypass_reporte/'+ str(documento) + '/' + str(debito_context).replace(' ', '%20') + '/' + str(debito_sueldo).replace(' ', '%20') )

            speech = "-"
            return{
                    "speech": speech,
                    "messages": [
                        {
                        "type": 0,
                        "platform": "facebook",
                        "speech": "Te generaré un reporte para que tengas el detalle de tus movimientos siempre a tu alcance :)"
                        },
                        {
                        "type": 0,
                        "platform": "facebook",
                        "speech": "Espera un momento porfavor"
                        },
                        {
                        "type": 4,
                        "platform": "facebook",
                        "payload": {
                            "facebook": {
                            "attachment": {
                                "type": "file",
                                "payload": {
                                "url": "http://181.177.228.114:81/reporte/reporte_" + str(documento) + ".pdf"
                                }
                            }
                            }
                        }
                        },
                        {
                        "type": 0,
                        "speech": ""
                        }
                    ]
            }
            

        else:
            return verificacion_response
    
    if intentName == "bytebot.avb.cuenta.debito.tipos.movimientos":
        #Verificación: ¿El estado de la tabla BBOTSEFAC es true o false?        
        verificacion = verificacion()
        
        
        if int(verificacion) != 0:  
            contexts = result.get("contexts")
            last_context = contexts[len(contexts)-1]
            name_context = last_context["name"]
            if name_context == "generic":
                last_context = contexts[len(contexts)-2]   
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
                            #cuentas_tipo_movimiento_dias = formatear_array_fechas(cuentas_json[j]["movimientos_dias"])
                            #cuentas_tipo_movimiento_dias = cuentas_json[j]["movimientos_dias"]
                            cuentas_tipo_movimiento_dias = past_days_from_current_day(8)
                            cuentas_tipo_movimiento_monto = cuentas_json[j]["movimientos_monto"]   
                            cuentas_tipo_movimiento_descripcion = cuentas_json[j]["movimientos_comercio"]                            
                            for k in range(0,indice_final_pagina):
                                if float(cuentas_tipo_movimiento_monto[k]) > 0:
                                    if solo_carrusel:
                                        json_string = u'{ "type": 1, "platform": "facebook", "title": "  ' + cuentas_tipo_movimiento_monedas + " " +  format(abs(float('{0:.2f}'.format(float(cuentas_tipo_movimiento_monto[k])))),',') + '", "subtitle": "' + cuentas_tipo_movimiento_descripcion[k] +'","imageUrl": "https://raw.githubusercontent.com/idusertbs/bytebot-agente-virtual-bancario-webhook/master/bytebot_agente_bancario_assets/setiembre/' + str(datetime.strptime(cuentas_tipo_movimiento_dias[k], '%b %d %Y %I:%M%p').day).zfill(2) + '_'+ str(datetime.strptime(cuentas_tipo_movimiento_dias[k], '%b %d %Y %I:%M%p').month).zfill(2)+'.png", "buttons": [] }'
                                    else: 
                                        json_string = u'{"title": "  ' + cuentas_tipo_movimiento_monedas + " " +  format(abs(float('{0:.2f}'.format(float(cuentas_tipo_movimiento_monto[k])))),',') + '", "subtitle": "' + cuentas_tipo_movimiento_descripcion[k] +'","image_url": "https://raw.githubusercontent.com/idusertbs/bytebot-agente-virtual-bancario-webhook/master/bytebot_agente_bancario_assets/setiembre/' + str(datetime.strptime(cuentas_tipo_movimiento_dias[k], '%b %d %Y %I:%M%p').day).zfill(2) + '_'+ str(datetime.strptime(cuentas_tipo_movimiento_dias[k], '%b %d %Y %I:%M%p').month).zfill(2)+'.png"}'
                                else:
                                    if solo_carrusel:
                                        json_string = u'{ "type": 1, "platform": "facebook", "title": "- ' + cuentas_tipo_movimiento_monedas + " " +  format(abs(float('{0:.2f}'.format(float(cuentas_tipo_movimiento_monto[k])))),',') + '", "subtitle": "' + cuentas_tipo_movimiento_descripcion[k] +'","imageUrl": "https://raw.githubusercontent.com/idusertbs/bytebot-agente-virtual-bancario-webhook/master/bytebot_agente_bancario_assets/setiembre/' + str(datetime.strptime(cuentas_tipo_movimiento_dias[k], '%b %d %Y %I:%M%p').day).zfill(2) + '_'+ str(datetime.strptime(cuentas_tipo_movimiento_dias[k], '%b %d %Y %I:%M%p').month).zfill(2)+'.png", "buttons": [] }'
                                    else: 
                                        json_string = u'{"title": "- ' + cuentas_tipo_movimiento_monedas + " " +  format(abs(float('{0:.2f}'.format(float(cuentas_tipo_movimiento_monto[k])))),',') + '", "subtitle": "' + cuentas_tipo_movimiento_descripcion[k] + '","image_url": "https://raw.githubusercontent.com/idusertbs/bytebot-agente-virtual-bancario-webhook/master/bytebot_agente_bancario_assets/setiembre/' + str(datetime.strptime(cuentas_tipo_movimiento_dias[k], '%b %d %Y %I:%M%p').day).zfill(2) + '_'+ str(datetime.strptime(cuentas_tipo_movimiento_dias[k], '%b %d %Y %I:%M%p').month).zfill(2)+'.png"}'

                                    
                                    
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
            name_context = last_context["name"]
            if name_context == "generic":
                last_context = contexts[len(contexts)-2]   
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
                            #cuentas_tipo_saldo_movimientos_dias = cuentas_json[j]["movimientos_dias"]
                            cuentas_tipo_saldo_movimientos_dias = past_days_from_current_day(8)
                            cuentas_tipo_saldo_movimientos_monto = cuentas_json[j]["movimientos_monto"]
                            cuentas_tipo_saldo_nombres.append(cuentas_tipo_saldo)
                            cuentas_tipo_saldo_tarjetas_array.append(cuentas_tipo_saldo_tarjetas)
                            cuentas_tipo_saldo_url_array.append(cuentas_tipo_saldo_url)
                            cuentas_tipo_saldo_saldos_array.append(cuentas_tipo_saldo_saldos)
                            cuentas_tipo_saldo_monedas_array.append(cuentas_tipo_saldo_monedas)
                            url_final = 'http://181.177.228.114:5000/grafica/' + str(cuentas_tipo_saldo_movimientos_dias) +'/'+ str(cuentas_tipo_saldo_movimientos_monto) +'/' + cuentas_tipo_saldo_saldos +'/'+ str(documento) + '/Cuentas/' + debito_context + '/' + debito_sueldo +'/' + cuentas_tipo_saldo_monedas
                            url_final_final = url_final.replace(" ", "%20").replace("S/","S")
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
            name_context = last_context["name"]
            if name_context == "generic":
                last_context = contexts[len(contexts)-2]   
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
                            #cuentas_tipo_movimiento_dias = cuentas_json[j]["movimientos_dias"]
                            cuentas_tipo_movimiento_dias = past_days_from_current_day(8)
                            cuentas_tipo_movimiento_monto = cuentas_json[j]["movimientos_monto"]
                            cuentas_tipo_movimiento_descripcion = cuentas_json[j]["movimientos_comercio"] 
                            #for k in range(0,len(cuentas_tipo_movimiento_monto)):
                            for k in range(indice_inicio_pagina,indice_final_pagina):
                                if float(cuentas_tipo_movimiento_monto[k]) > 0:
                                    json_string = u'{"title": "  ' + cuentas_tipo_movimiento_monedas + " " + format(abs(float('{0:.2f}'.format(float(cuentas_tipo_movimiento_monto[k])))),',') + '", "subtitle": "' + cuentas_tipo_movimiento_descripcion[k] + '","image_url": "https://raw.githubusercontent.com/idusertbs/bytebot-agente-virtual-bancario-webhook/master/bytebot_agente_bancario_assets/setiembre/' + str(datetime.strptime(cuentas_tipo_movimiento_dias[k], '%b %d %Y %I:%M%p').day).zfill(2) + '_'+ str(datetime.strptime(cuentas_tipo_movimiento_dias[k], '%b %d %Y %I:%M%p').month).zfill(2)+'.png"}'                              
                                else:
                                    json_string = u'{"title": "- ' + cuentas_tipo_movimiento_monedas + " " + format(abs(float('{0:.2f}'.format(float(cuentas_tipo_movimiento_monto[k])))),',') + '", "subtitle": "' + cuentas_tipo_movimiento_descripcion[k] + '","image_url": "https://raw.githubusercontent.com/idusertbs/bytebot-agente-virtual-bancario-webhook/master/bytebot_agente_bancario_assets/setiembre/' + str(datetime.strptime(cuentas_tipo_movimiento_dias[k], '%b %d %Y %I:%M%p').day).zfill(2) + '_'+ str(datetime.strptime(cuentas_tipo_movimiento_dias[k], '%b %d %Y %I:%M%p').month).zfill(2)+'.png"}'
                                    
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


        
                 
    '''
    if intentName == "bytebot.avb.consultar.tarjetas":        
        #verificar si puede consultar cuentas
        speech = "Todavía no me implementan la opción de verificación, así que no podrás consultar tus tarjetas 😢"
        return {
            "speech": speech,
            "displayText": speech,
            "source": "bytebot-virtual-agent-webhook"

        }
    '''
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
    
    if intentName == "bytebot.avb.tarjeta.credito.saldo":
        #Verificación: ¿El estado de la tabla BBOTSEFAC es true o false?        
        verificacion = verificacion()
        
        if int(verificacion) != 0:  
            contexts = result.get("contexts")
            last_context = contexts[len(contexts)-1]
            name_context = last_context["name"]
            if name_context == "generic":
                last_context = contexts[len(contexts)-2]  
            parameters_context = last_context["parameters"]
            credito = parameters_context.get("credito")

            r_saldos = requests.get('http://181.177.228.114:5000/credito/saldos/' + str(credito).replace(" ", "%20"))
            json_object_saldos = r_saldos.json()
            documento = int(json_object_saldos["saldos_tarjeta"]["documento"])
            tarjeta_credito_saldo = []
            error = json_object_saldos["error"]
            if  error == "0":
                saldos_tarjeta = json_object_saldos["saldos_tarjeta"]
                moneda = saldos_tarjeta["moneda"]
                numero = saldos_tarjeta["numero"]
                saldo = saldos_tarjeta["saldo"]
                speech = "Tu saldo actual es:"
                speech_saldo_1 = moneda + " " + format(float("{0:.2f}".format(float(saldo))),',')
                speech_saldo_2 = credito
                speech_saldo_3 = numero                
                json_string_0 = u'{"type": 0,"platform": "facebook","speech":"'+ speech +'"}'                
                json_string = u'{ "type": 4, "platform": "facebook", "payload": { "facebook": { "attachment": { "type": "template", "payload": { "template_type": "button", "text": "'+ speech_saldo_2 + "\n" + speech_saldo_3  + "\n" + speech_saldo_1 +'","buttons": [{ "type": "postback", "title": "Generar Reporte", "payload": "Generar Reporte ' + credito + '" },{"type": "postback", "title": "Ver Movimientos", "payload": "Consultar Movimientos ' + credito + '"}]}}}} }'                
                objeto_0 = json.loads(json_string_0)
                objeto  = json.loads(json_string,strict=False)
                tarjeta_credito_saldo.append(objeto_0) 
                tarjeta_credito_saldo.append(objeto)   
                return {
                    "speech": "?? ",
                    "displayText": "??",
                    "source": "apiai-weather-webhook",
                    "messages": tarjeta_credito_saldo
                } 

            else:
                return {
                    "speech": "Al parecer no tienes esa tarjeta 😅",
                    "displayText": "Al parecer no posees esa tarjeta 😅",
                    "source": "apiai-weather-webhook"
                }

        else:
            return verificacion_response

    if intentName == "bytebot.avb.tarjeta.credito.proximo.pago" or intentName == "bytebot.avb.tarjeta.credito.proximo.pago-tarjeta":
        #Verificación: ¿El estado de la tabla BBOTSEFAC es true o false?        
        verificacion = verificacion()
        
        if int(verificacion) != 0:  
            contexts = result.get("contexts")
            if len(contexts) > 0:
                last_context = contexts[len(contexts)-1]
                name_context = last_context["name"]
                if name_context == "generic":
                    last_context = contexts[len(contexts)-2]   
                parameters_context = last_context["parameters"]
                tarjeta_credito = parameters_context.get("credito")
            else:
                tarjeta_credito = ""
            
            if tarjeta_credito == None or tarjeta_credito == "":
                tarjeta_credito = "" 

            r_query = requests.get('http://181.177.228.114:5000/query')
            json_object_query = r_query.json()
            documento = int(json_object_query["result"]["documento"])    
            r=requests.get('http://181.177.228.114:5001/clientes/' + str(documento))
            json_object = r.json()

            credito=json_object['result']['clientes']['credito']
            if len(tarjeta_credito) == 0: 
                tarjetas_array = []  
                for j in range(0,len(credito)):            
                    json_string = u'{"content_type": "text","title": "' + credito[j]["nombre"] + '","payload": "'+credito[j]["nombre"] + '"}'
                    objeto  = json.loads(json_string,strict=False)
                    tarjetas_array.append(objeto)
                return { "speech": "","messages": [ 
                        { "type": 4, "platform": "facebook", "payload": { "facebook": { "text": "¿Para qué tarjeta de crédito deseas saber aquella información? 🤔", "quick_replies": tarjetas_array }}},
                        { "type": 0, "speech": ""}
                    ]
                }
            else:
                r_proximo_pago = requests.get('http://181.177.228.114:5000/credito/proximo_pago/' + str(tarjeta_credito).replace(" ", "%20"))
                json_object_proximo_pago = r_proximo_pago.json()
                documento = int(json_object_proximo_pago["proximo_pago"]["documento"])
                tarjeta_credito_proximo_pago = []
                error = json_object_proximo_pago["error"]
                if  error == "0":
                    proximo_pago = json_object_proximo_pago["proximo_pago"]
                    fecha_pago = proximo_pago["fecha_pago"]
                    linea_credito = proximo_pago["linea_credito"]
                    moneda = proximo_pago["moneda"]
                    monto_minimo = proximo_pago["monto_minimo"]
                    monto_total = proximo_pago["monto_total"]
                    saldo_disponible = proximo_pago["saldo_disponible"]
                    speech = "Tarjeta " + tarjeta_credito + "\n\nLínea de Crédito: " + moneda + " " + format(abs(float('{0:.2f}'.format(float(linea_credito)))),',') + "\nSaldo Disponible: " + moneda + " " + format(abs(float('{0:.2f}'.format(float(saldo_disponible)))),',')  + "\n\nPagos" + "\n\nFecha de pago: " + fecha_pago + "\nMonto mínimo: " + moneda + " " + format(abs(float('{0:.2f}'.format(float(monto_minimo)))),',') + "\nMonto total: " + moneda + " " + format(abs(float('{0:.2f}'.format(float(monto_total)))),',')
                    json_string_0 = u'{"type": 0,"platform": "facebook","speech":"'+ speech +'"}'                
                    
                    objeto_0 = json.loads(json_string_0,strict=False)
                    tarjeta_credito_proximo_pago.append(objeto_0) 
                    return {
                        "speech": "Cancelado :/",
                        "displayText": "Cancelado",
                        "source": "apiai-weather-webhook",
                        "messages": tarjeta_credito_proximo_pago
                    } 

                else:
                    return {
                        "speech": "Al parecer no posees esa tarjeta 😅",
                        "displayText": "Al parecer no posees esa tarjeta 😅",
                        "source": "apiai-weather-webhook"
                    }

        else:
            return verificacion_response
    

    if intentName == "bytebot.avb.tarjeta.credito.movimientos":
        #Verificación: ¿El estado de la tabla BBOTSEFAC es true o false?        
        verificacion = verificacion()
        
        
        if int(verificacion) != 0:  
            contexts = result.get("contexts")
            last_context = contexts[len(contexts)-1]
            name_context = last_context["name"]
            if name_context == "generic":
                last_context = contexts[len(contexts)-2]   
            parameters_context = last_context["parameters"]
            tarjeta_credito = parameters_context.get("credito")

            r_query = requests.get('http://181.177.228.114:5000/query')
            json_object_query = r_query.json()
            documento = int(json_object_query["result"]["documento"])            
        

            r=requests.get('http://181.177.228.114:5001/clientes/' + str(documento))
            json_object = r.json()

            hay_tarjeta = False
            credito=json_object['result']['clientes']['credito']
            credito_movimiento_array = []
            #cuentas_tipo_movimiento_array.append(objeto_inicio)  
            movimientos_dias = past_days_from_current_day(6)
            for i in range(0,len(credito)):                
                if credito[i]["nombre"] == tarjeta_credito:
                    hay_tarjeta = True
                    #if len(credito[i]["movimientos_dias"]) == 1:
                    if len(movimientos_dias) == 1:
                        numero_pantallas = 1
                        solo_carrusel = True
                        indice_final_pagina = 1
                    #elif len(credito[i]["movimientos_dias"])%2 == 0:
                    elif len(movimientos_dias)%2 == 0:
                        solo_carrusel = False
                        #numero_pantallas = ceil(len(credito[i]["movimientos_dias"])/4)
                        numero_pantallas = ceil(len(movimientos_dias)/4)
                        #if len(credito[i]["movimientos_monto"]) > 4:
                        if len(movimientos_dias) > 4:
                            indice_final_pagina = 0 + 4
                        else:
                            #indice_final_pagina =  len(credito[i]["movimientos_monto"]) 
                            indice_final_pagina =  len(movimientos_dias) 
                    else:
                        #numero_pantallas = ceil(len(credito[i]["movimientos_dias"])/3)
                        numero_pantallas = ceil(len(movimientos_dias)/3)
                        solo_carrusel = False
                        #if len(credito[i]["movimientos_monto"]) > 3:
                        if len(movimientos_dias) > 3:
                            indice_final_pagina = 0 + 3
                        else:
                            #indice_final_pagina =  len(credito[i]["movimientos_monto"]) 
                            indice_final_pagina =  len(movimientos_dias) 
                        
                    moneda = credito[i]["moneda"]
                    #movimientos_dias = formatear_array_fechas(credito[i]["movimientos_dias"])
                    #movimientos_dias = credito[i]["movimientos_dias"]
                    movimientos_dias = past_days_from_current_day(6)
                    movimientos_monto = credito[i]["movimientos_monto"]   
                    movimientos_descripcion = credito[i]["movimientos_comercio"]                            
                    for k in range(0,indice_final_pagina):
                        if float(movimientos_monto[k]) > 0:
                            if solo_carrusel:
                                json_string = u'{ "type": 1, "platform": "facebook", "title": "  ' + moneda + " " + format(abs(float('{0:.2f}'.format(float(movimientos_monto[k])))),',') + '", "subtitle": "' + movimientos_descripcion[k] +'","imageUrl": "https://raw.githubusercontent.com/idusertbs/bytebot-agente-virtual-bancario-webhook/master/bytebot_agente_bancario_assets/setiembre/' + str(datetime.strptime(movimientos_dias[k], '%b %d %Y %I:%M%p').day).zfill(2) + '_'+ str(datetime.strptime(movimientos_dias[k], '%b %d %Y %I:%M%p').month).zfill(2)+'.png", "buttons": [] }'
                            else: 
                                json_string = u'{"title": "- ' + moneda + " " + format(abs(float('{0:.2f}'.format(float(movimientos_monto[k])))),',') + '", "subtitle": "' + movimientos_descripcion[k] + '","image_url": "https://raw.githubusercontent.com/idusertbs/bytebot-agente-virtual-bancario-webhook/master/bytebot_agente_bancario_assets/setiembre/' + str(datetime.strptime(movimientos_dias[k], '%b %d %Y %I:%M%p').day).zfill(2) + '_'+ str(datetime.strptime(movimientos_dias[k], '%b %d %Y %I:%M%p').month).zfill(2)+'.png"}'
                        else:
                            if solo_carrusel:
                                json_string = u'{ "type": 1, "platform": "facebook", "title": "- ' + moneda + " " + format(abs(float('{0:.2f}'.format(float(movimientos_monto[k])))),',') + '", "subtitle": "' + movimientos_descripcion[k] + '","imageUrl": "https://raw.githubusercontent.com/idusertbs/bytebot-agente-virtual-bancario-webhook/master/bytebot_agente_bancario_assets/setiembre/' + str(datetime.strptime(movimientos_dias[k], '%b %d %Y %I:%M%p').day).zfill(2) + '_'+ str(datetime.strptime(movimientos_dias[k], '%b %d %Y %I:%M%p').month).zfill(2)+'.png", "buttons": [] }'
                            else: 
                                json_string = u'{"title": "- ' + moneda + " " + format(abs(float('{0:.2f}'.format(float(movimientos_monto[k])))),',') + '", "subtitle": "' + movimientos_descripcion[k] + '","image_url": "https://raw.githubusercontent.com/idusertbs/bytebot-agente-virtual-bancario-webhook/master/bytebot_agente_bancario_assets/setiembre/' + str(datetime.strptime(movimientos_dias[k], '%b %d %Y %I:%M%p').day).zfill(2) + '_'+ str(datetime.strptime(movimientos_dias[k], '%b %d %Y %I:%M%p').month).zfill(2)+'.png"}'
                            
                            
                        objeto  = json.loads(json_string,strict=False)
                        credito_movimiento_array.append(objeto)

            if not(hay_tarjeta):
                    return {
                            "speech": "-",
                            "displayText": "-",
                            "source": "bytebot-webhook",
                            "messages": [
                                {
                                    "type": 0,
                                    "platform": "facebook",
                                    "speech": "Usted no posee esa tarjeta 😅"
                                }
                            ]

                        }
            else:
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
                            credito_movimiento_array
                    }
                else: 
                    return {
                    "speech": "Cancelado :/",
                    "displayText": "heyo",
                    "source": "apiai-weather-webhook",
                    "messages": [
                        {"type": 0, "platform": "facebook", "speech": "Estos son los movimientos de tu tarjeta " + tarjeta_credito },
                        {"type": 4, "platform": "facebook", "payload": { "facebook": { "attachment": { "type": "template", "payload": { "template_type": "list", "top_element_style": "compact",
                    "elements": 
                        credito_movimiento_array
                    ,
                    "buttons": button_ver_mas
                        }}}}}
                    ]

                } 


            
            

        else:
            return verificacion_response
    
    if intentName == "bytebot.avb.tarjeta.credito.movimientos-next":
        #Verificación: ¿El estado de la tabla BBOTSEFAC es true o false?        
        verificacion = verificacion()
        
        
        if int(verificacion) != 0:  
            contexts = result.get("contexts")
            last_context = contexts[len(contexts)-1]
            name_context = last_context["name"]
            if name_context == "generic":
                last_context = contexts[len(contexts)-2]            
            parameters_context = last_context["parameters"]
            tarjeta_credito = parameters_context.get("credito")
            pagina = int(parameters_context.get("paginas")[6:])


            r_query = requests.get('http://181.177.228.114:5000/query')
            json_object_query = r_query.json()
            documento = int(json_object_query["result"]["documento"])            
        

            r=requests.get('http://181.177.228.114:5001/clientes/' + str(documento))
            json_object = r.json()

            credito=json_object['result']['clientes']['credito']
            credito_movimiento_array = []      
            movimientos_dias = past_days_from_current_day(6)
            for j in range(0,len(credito)):
                if credito[j]["nombre"] == tarjeta_credito:
                    if len(movimientos_dias)%2 == 0:
                        numero_pantallas = ceil(len(movimientos_dias)/4)
                        indice_inicio_pagina = 5*(pagina-1)-(pagina-1)
                        if len(movimientos_dias) - (indice_inicio_pagina+1) > 4:
                            indice_final_pagina = indice_inicio_pagina + 4 
                        else:
                            indice_final_pagina =  len(movimientos_dias) 
                    else:
                        numero_pantallas = ceil(len(movimientos_dias)/3) 
                        indice_inicio_pagina = 4*(pagina-1)-(pagina-1)
                        if len(movimientos_dias) - (indice_inicio_pagina+1) > 3:
                            indice_final_pagina = indice_inicio_pagina + 3
                        else:
                            indice_final_pagina =  len(movimientos_dias) 

                    moneda = credito[j]["moneda"]                    
                    #movimientos_dias = credito[j]["movimientos_dias"]
                    movimientos_dias = past_days_from_current_day(6)
                    movimientos_monto = credito[j]["movimientos_monto"]
                    movimientos_descripcion = credito[j]["movimientos_comercio"] 
                    for k in range(indice_inicio_pagina,indice_final_pagina):
                        if float(movimientos_monto[k]) > 0:
                            json_string = u'{"title": "- ' + moneda + " " + format(abs(float('{0:.2f}'.format(float(movimientos_monto[k])))),',') + '", "subtitle": "' + movimientos_descripcion[k] + '","image_url": "https://raw.githubusercontent.com/idusertbs/bytebot-agente-virtual-bancario-webhook/master/bytebot_agente_bancario_assets/setiembre/' + str(datetime.strptime(movimientos_dias[k], '%b %d %Y %I:%M%p').day).zfill(2) + '_'+ str(datetime.strptime(movimientos_dias[k], '%b %d %Y %I:%M%p').month).zfill(2)+'.png"}'
                        else:
                            json_string = u'{"title": "- ' + moneda + " " + format(abs(float('{0:.2f}'.format(float(movimientos_monto[k])))),',') + '", "subtitle": "' + movimientos_descripcion[k] + '","image_url": "https://raw.githubusercontent.com/idusertbs/bytebot-agente-virtual-bancario-webhook/master/bytebot_agente_bancario_assets/setiembre/' + str(datetime.strptime(movimientos_dias[k], '%b %d %Y %I:%M%p').day).zfill(2) + '_'+ str(datetime.strptime(movimientos_dias[k], '%b %d %Y %I:%M%p').month).zfill(2)+'.png"}'
                            
                        objeto  = json.loads(json_string,strict=False)
                        credito_movimiento_array.append(objeto)   


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
                    credito_movimiento_array
                  ,
                  "buttons": button_ver_mas
                    }}}}}
                ]

            } 
            

        else:
            return verificacion_response

    if intentName == "bytebot.avb.tarjeta.credito.analisis.consumo":
        #Verificación: ¿El estado de la tabla BBOTSEFAC es true o false?        
        verificacion = verificacion()
        
        
        if int(verificacion) != 0:  
            contexts = result.get("contexts")
            last_context = contexts[len(contexts)-1] 
            name_context = last_context["name"]
            if name_context == "generic":
                last_context = contexts[len(contexts)-2]  
            parameters_context = last_context["parameters"]
            tarjeta_credito = parameters_context.get("credito")

            r_query = requests.get('http://181.177.228.114:5000/query')
            json_object_query = r_query.json()
            documento = int(json_object_query["result"]["documento"])            
        

            r=requests.get('http://181.177.228.114:5001/clientes/' + str(documento))
            json_object = r.json()

            return {
                "speech": "análisis", "displayText": "análisis", "source": "bytebot-webhook",
                "messages": [                    
                    { "type": 4, "platform": "facebook", "payload": { "facebook": { "attachment": { "type": "template", "payload": { "template_type": "button", "text": "Seleccione el tipo de Análisis: ",
                                "buttons": [ 
                                    { "type": "postback", "title": "Consumo por Concepto", "payload": "Consumo por Concepto " + tarjeta_credito},
                                    {"type": "postback", "title": "Consumo por Comercio", "payload": "Consumo por Comercio " + tarjeta_credito}
                                ]}}}}
                    },
                    { "type": 0, "speech": "" }
                ]
            }
            

        else:
            return verificacion_response

    if intentName == "bytebot.avb.tarjeta.credito.analisis.consumo.grafica" or intentName == "bytebot.avb.tarjeta.credito.analisis.consumo.grafica-tarjeta":
        #Verificación: ¿El estado de la tabla BBOTSEFAC es true o false?        
        verificacion = verificacion()
        
        
        if int(verificacion) != 0:  
            contexts = result.get("contexts")
            if len(contexts) > 0:
                last_context = contexts[len(contexts)-1] 
                name_context = last_context["name"]
                if name_context == "generic":
                    last_context = contexts[len(contexts)-2]  
                parameters_context = last_context["parameters"]
                tarjeta_credito = parameters_context.get("credito")
                consumo = parameters_context.get("consumo")     
            else:
                tarjeta_credito = ""
                consumo = ""
            if tarjeta_credito == None or tarjeta_credito == "":
                tarjeta_credito = ""  

            if consumo == "" or consumo == None:
                consumo = "ese consumo"

            r_query = requests.get('http://181.177.228.114:5000/query')
            json_object_query = r_query.json()
            documento = int(json_object_query["result"]["documento"])            
        

            r=requests.get('http://181.177.228.114:5001/clientes/' + str(documento))
            json_object = r.json()

            credito=json_object['result']['clientes']['credito']
            credito_movimiento_array = []     
            
            if len(tarjeta_credito) == 0: 
                tarjetas_array = []  
                for j in range(0,len(credito)):            
                    json_string = u'{"content_type": "text","title": "' + credito[j]["nombre"] + '","payload": "'+credito[j]["nombre"] + " " + consumo +'"  }'
                    objeto  = json.loads(json_string,strict=False)
                    tarjetas_array.append(objeto)
                return { "speech": "","messages": [ 
                        { "type": 4, "platform": "facebook", "payload": { "facebook": { "text": "¿Para qué tarjeta de crédito deseas generar la gráfica? 🤔", "quick_replies": tarjetas_array }}},
                        { "type": 0, "speech": ""}
                    ]
                }
            else:
                hay_tarjeta = False
                for j in range(0,len(credito)):
                    if credito[j]["nombre"] == tarjeta_credito:
                        hay_tarjeta = True
                        moneda = credito[j]["moneda"]
                        #movimientos_dias = formatear_array_fechas(credito[j]["movimientos_dias"])
                        movimientos_dias = formatear_array_fechas(past_days_from_current_day(8))
                        movimientos_monto = credito[j]["movimientos_monto"]
                        movimientos_descripcion = credito[j]["movimientos_descripcion"] 
                        movimientos_concepto = credito[j]["movimientos_concepto"] 
                        movimientos_comercio = credito[j]["movimientos_comercio"] 
                        url = "http://181.177.228.114:5000/credito/grafica/" + str(movimientos_monto) + "/" + str(movimientos_concepto) + "/" + str(movimientos_comercio) + "/" + str(moneda) + "/" + str(tarjeta_credito) + "/" + str(consumo)
                        url = url.replace(" ", "%20").replace("S/","S")
                        r_grafica = requests.get(url)
                        json_url_imagen = r_grafica.json()
                        url_imagen = json_url_imagen["result"]["url"]

                        fecha_final_formateada  = movimientos_dias[0]
                        fecha_inicial_formateada = movimientos_dias[len(movimientos_dias) - 1]

                        return {
                            "speech": "-",
                            "displayText": "-",
                            "source": "apiai-weather-webhook",
                            "messages": [
                                {
                                    "type": 0,
                                    "platform": "facebook",
                                    "speech": "Esta es el consumo de tu tarjeta a lo largo del mes.\nDesde el " + fecha_inicial_formateada + " al " + fecha_final_formateada
                                },
                                {
                                    "type": 3,
                                    "platform": "facebook",
                                    "imageUrl": url_imagen
                                }
                            ]

                        }
                if not(hay_tarjeta):
                    return {
                            "speech": "-",
                            "displayText": "-",
                            "source": "bytebot-webhook",
                            "messages": [
                                {
                                    "type": 0,
                                    "platform": "facebook",
                                    "speech": "Al parecer usted no posee esa tarjeta 😅"
                                }
                            ]

                        }
                            
            

        else:
            return verificacion_response

    
    if intentName == "bytebot.avb.tarjeta.sueltas.gastos.concepto" or intentName == "bytebot.avb.tarjeta.sueltas.gastos.concepto-tarjeta":
        #Verificación: ¿El estado de la tabla BBOTSEFAC es true o false?        
        verificacion = verificacion()
        
        
        if int(verificacion) != 0:  
            contexts = result.get("contexts")
            if len(contexts) > 0:
                last_context = contexts[len(contexts)-1]
                name_context = last_context["name"]
                if name_context == "generic":
                    last_context = contexts[len(contexts)-2]   
                parameters_context = last_context["parameters"]
                tarjeta_credito = parameters_context.get("credito")
                concepto = parameters_context.get("concepto") 
            else:
                tarjeta_credito = ""
                concepto = ""  

            if tarjeta_credito == None or tarjeta_credito == "":
                tarjeta_credito = ""  

            if concepto == "" or concepto == None:
                concepto = "ese concepto"

            r_query = requests.get('http://181.177.228.114:5000/query')
            json_object_query = r_query.json()
            documento = int(json_object_query["result"]["documento"])
        
            r=requests.get('http://181.177.228.114:5001/clientes/' + str(documento))
            json_object = r.json()

            credito=json_object['result']['clientes']['credito']

            if len(tarjeta_credito) == 0: 
                tarjetas_array = []  
                for j in range(0,len(credito)):            
                    json_string = u'{"content_type": "text","title": "' + credito[j]["nombre"] + '","payload": "'+credito[j]["nombre"] + " " + concepto +'"  }'
                    objeto  = json.loads(json_string,strict=False)
                    tarjetas_array.append(objeto)
                return { "speech": "","messages": [ 
                        { "type": 4, "platform": "facebook", "payload": { "facebook": { "text": "¿Para qué tarjeta de crédito deseas consultar tus gastos? 🤔", "quick_replies": tarjetas_array }}},
                        { "type": 0, "speech": ""}
                    ]
                }
            else:
                hay_tarjeta = False
                for j in range(0,len(credito)):
                    if credito[j]["nombre"] == tarjeta_credito:
                        hay_tarjeta = True
                        moneda = credito[j]["moneda"]
                        movimientos_dias = credito[j]["movimientos_dias"]
                        movimientos_monto = credito[j]["movimientos_monto"]
                        movimientos_concepto = credito[j]["movimientos_concepto"] 
                        group_conceptos, group_gastos = group_two_lists_by_first_list(movimientos_concepto, movimientos_monto)
                        for i in range(0,len(group_conceptos)):
                            if group_conceptos[i] == concepto:
                                speech1 = "Esto es lo que gastó durante el mes en " + concepto + " con su tarjeta " + tarjeta_credito + ": " + moneda + ". " + "{0:.2f}".format(float(group_gastos[i]))                                                            
                                break
                            else:
                                speech1 = "Usted no hizo ningún gasto referente a " + concepto + " con su tarjeta " + tarjeta_credito + " :)"
                        return {
                                "speech": "-",
                                "displayText": "-",
                                "source": "bytebot-webhook",
                                "messages": [
                                    {
                                        "type": 0,
                                        "platform": "facebook",
                                        "speech": speech1
                                    }
                                ]

                            }
                if not(hay_tarjeta):
                    return {
                            "speech": "-",
                            "displayText": "-",
                            "source": "bytebot-webhook",
                            "messages": [
                                {
                                    "type": 0,
                                    "platform": "facebook",
                                    "speech": "Usted no posee esa tarjeta 😅"
                                }
                            ]

                        }

        else:
            return verificacion_response
    
    if intentName == "bytebot.avb.tarjeta.sueltas.gastos.comercio" or intentName == "bytebot.avb.tarjeta.sueltas.gastos.comercio-tarjeta":
        #Verificación: ¿El estado de la tabla BBOTSEFAC es true o false?        
        verificacion = verificacion()
        
        
        if int(verificacion) != 0:  
            contexts = result.get("contexts")
            if len(contexts) > 0:
                last_context = contexts[len(contexts)-1] 
                name_context = last_context["name"]
                if name_context == "generic":
                    last_context = contexts[len(contexts)-2]  
                parameters_context = last_context["parameters"]
                tarjeta_credito = parameters_context.get("credito")
                comercio = parameters_context.get("comercio") 
            else:
                tarjeta_credito = ""
                comercio = ""  

            if tarjeta_credito == None:
                tarjeta_credito = ""  

            if comercio == "" or comercio == None:
                comercio = "ese comercio"

            r_query = requests.get('http://181.177.228.114:5000/query')
            json_object_query = r_query.json()
            documento = int(json_object_query["result"]["documento"])
        
            r=requests.get('http://181.177.228.114:5001/clientes/' + str(documento))
            json_object = r.json()

            credito=json_object['result']['clientes']['credito']

            if len(tarjeta_credito) == 0: 
                tarjetas_array = []  
                for j in range(0,len(credito)):            
                    json_string = u'{"content_type": "text","title": "' + credito[j]["nombre"] + '","payload": "'+credito[j]["nombre"] + " " + comercio +'"  }'
                    objeto  = json.loads(json_string,strict=False)
                    tarjetas_array.append(objeto)
                return { "speech": "","messages": [ 
                        { "type": 4, "platform": "facebook", "payload": { "facebook": { "text": "¿Para qué tarjeta de crédito deseas consultar tus gastos? 🤔", "quick_replies": tarjetas_array }}},
                        { "type": 0, "speech": ""}
                    ]
                }
            else:
                hay_tarjeta = False
                for j in range(0,len(credito)):
                    if credito[j]["nombre"] == tarjeta_credito:
                        hay_tarjeta = True
                        moneda = credito[j]["moneda"]
                        movimientos_dias = credito[j]["movimientos_dias"]
                        movimientos_monto = credito[j]["movimientos_monto"]
                        movimientos_comercio = credito[j]["movimientos_comercio"] 
                        group_comercio, group_gastos = group_two_lists_by_first_list(movimientos_comercio, movimientos_monto)
                        for i in range(0,len(group_comercio)):
                            if group_comercio[i] == comercio:
                                speech1 = "Esto es lo que gastó durante el mes en " + comercio + " con su tarjeta " + tarjeta_credito + ": " + moneda + ". " + "{0:.2f}".format(float(group_gastos[i]))                                                            
                                break
                            else:
                                speech1 = "Usted no hizo ningún gasto referente a " + comercio + " con su tarjeta " + tarjeta_credito + " :)"
                        return {
                                "speech": "-",
                                "displayText": "-",
                                "source": "bytebot-webhook",
                                "messages": [
                                    {
                                        "type": 0,
                                        "platform": "facebook",
                                        "speech": speech1
                                    }
                                ]

                            }
                if not(hay_tarjeta):
                    return {
                            "speech": "-",
                            "displayText": "-",
                            "source": "bytebot-webhook",
                            "messages": [
                                {
                                    "type": 0,
                                    "platform": "facebook",
                                    "speech": "Usted no posee esa tarjeta 😅"
                                }
                            ]

                        }

        else:
            return verificacion_response
    
    if intentName == "bytebot.avb.sueltas.tipo.de.cambio" or intentName == "bytebot.avb.sueltas.tipo.de.cambio-canal":        
        contexts = result.get("contexts")
        if len(contexts) > 0:
            last_context = contexts[len(contexts)-1] 
            name_context = last_context["name"]
            if name_context == "generic":
                last_context = contexts[len(contexts)-2]  
            parameters_context = last_context["parameters"]            
            canal_tipo_cambio = parameters_context.get("canal_tipo_cambio")
            cambio = parameters_context.get("cambio") 
        else:
            canal_tipo_cambio = ""  
            cambio = ""          

        if canal_tipo_cambio == "" or canal_tipo_cambio == None:
            canal_tipo_cambio = ""
        
        
        if len(canal_tipo_cambio) == 0: 
            canales = ["Agencias", "Cajeros"]
            canal_tipo_cambio_array = []
            for j in range(0,len(canales)):            
                json_string = u'{"content_type": "text","title": "' + canales[j] + '","payload": "' + canales[j] + '"  }'
                objeto  = json.loads(json_string,strict=False)
                canal_tipo_cambio_array.append(objeto)
            return { "speech": "","messages": [ 
                    { "type": 4, "platform": "facebook", "payload": { "facebook": { "text": "¿Para qué canal desea saber el tipo de cambio? 🤔", "quick_replies": canal_tipo_cambio_array }}},
                    { "type": 0, "speech": ""}
                ]
            }
        else:
            #hay_canal = False
            r_query = requests.get('http://181.177.228.114:5000/tipo_de_cambio/')
            json_object_query = r_query.json()

            if canal_tipo_cambio == "Agencia":
                if cambio == "SolesDolares":
                    monto_cambio = json_object_query["result"]["agencia"]["soles_to_dolares"]
                elif cambio == "DolaresSoles":
                    monto_cambio = json_object_query["result"]["agencia"]["dolares_to_soles"]
                else:
                    monto_cambio = "0.00"
            elif canal_tipo_cambio == "Cajero":    
                if cambio == "SolesDolares":
                    monto_cambio = json_object_query["result"]["cajero"]["soles_to_dolares"]
                elif cambio == "DolaresSoles":
                    monto_cambio = json_object_query["result"]["cajero"]["dolares_to_soles"]
                else:
                    monto_cambio = "0.00"

            
            speech1 = "El tipo de cambio solicitado en "+ canal_tipo_cambio +" es " + str(monto_cambio)
            
            return {
                        "speech": "-",
                        "displayText": "-",
                        "source": "bytebot-webhook",
                        "messages": [
                        {
                        "type": 0,
                        "platform": "facebook",
                        "speech": speech1
                    }
                ]
            }
            #if not(hay_tarjeta):
            #    return {
            #            "speech": "-",
            #            "displayText": "-",
            #            "source": "bytebot-webhook",
            #            "messages": [
            #                {
            #                    "type": 0,
            #                    "platform": "facebook",
            #                    "speech": "Usted no posee esa tarjeta 😅"
            #                }
            #            ]
            #        }
    
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')

















