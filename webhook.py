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
    
    if intentName == "cs.no.secuencial.unico.pg3":
        parameters = result.get("parameters")
        tiposdeproducto = parameters.get("tiposdeproducto")

        if tiposdeproducto == "Cuenta.Sueldo":
            speech = "Una franquicia, es el monto a partir del cual el Banco paga intereses: \n✔️Soles: S/500.00 \n✔️Dólares: US$220.00" 
            return {
                "speech": speech,
                "displayText": speech
            }
        else:
            speech = "La franquicia solo corresponde a la cuenta sueldo 😐. En la cuenta SUELDO una franquicia es el monto a partir del cual el Banco paga intereses: \n✔️Soles: S/500.00 \n✔️Dólares: US$220.00"
            return {
                "speech": speech,
                "displayText": speech,
                "messages": [
				{
					"type": 0,
					"speech": speech,
                    "platform": "facebook"
				}
			]
            }
    
    if intentName == "cg.no.secuencial.unico.pg1":
        parameters = result.get("parameters")
        tiposdeproducto = parameters.get("tiposdeproducto")

        if tiposdeproducto == "Cuenta.Ganadora":
            speech = "El interés se gana diario y los abonamos en tu cuenta cada fin de mes. 😀" 
            return {
                "speech": speech,
                "displayText": speech
            }
        else:
            speech = "La ganancia de intereses solo corresponden a la cuenta ganadora 😐. En la cuenta ganadora el interés se gana diario y lo abonamos en tu cuenta cada fin de mes 😀 "
            return {
                "speech": speech,
                "displayText": speech,
                "messages": [
				{
					"type": 0,
					"speech": speech,
                    "platform": "facebook"
				}
			]
            }
    if intentName == "cg.no.secuencial.unico.pg2":
        parameters = result.get("parameters")
        tiposdeproducto = parameters.get("tiposdeproducto")

        if tiposdeproducto == "Cuenta.Ganadora":
            speech = "Para participar de los sorteos, debes mantener al menos una Cuenta Ganadora con saldo medio igual o mayor a S/ 1,000 o US$ 1,000, para poder ganar una opción para el sorteo. Además, por cada S/ 1,000 o US$ 1,000 adicionales depositados en la cuenta, tienes una opción extra. Si eres cliente Mundo Sueldo o VIP tienes doble opción. Las cuentas ganadoras en soles duplican tus opciones." 
            return {
                "speech": speech,
                "displayText": speech
            }
        else:
            speech = "Los sorteos y promociones solo pertenecen a la cuenta GANADORA 😐. Si quieres participar de los sorteos con tu cuenta GANADORA, debes mantener al menos una Cuenta Ganadora con saldo medio igual o mayor a S/ 1,000 o US$ 1,000, para poder ganar una opción para el sorteo. Además, por cada S/ 1,000 o US$ 1,000 adicionales depositados en la cuenta, tienes una opción extra. Si eres cliente Mundo Sueldo o VIP tienes doble opción. Las cuentas ganadoras en soles duplican tus opciones."
            return {
                "speech": speech,
                "displayText": speech,
                "messages": [
				{
					"type": 0,
					"speech": speech,
                    "platform": "facebook"
				}
			]
            }



    if intentName == "no.secuencial.no.parametrica.pg1-options":
        parameters = result.get("parameters")
        tiposdeproducto = parameters.get("tiposdeproducto")

        if tiposdeproducto == "Cuenta.Sueldo":
            speech = "¡Ya diste el primer paso :)!, ahora solo debes acercarte a nuestras oficinas para obtener la Tarjeta de Débito que te permitirá acceder a todos nuestros canales de atención: Banca por Internet, Banca Móvil, Banca por Teléfono, entre otros. Con tu Tarjeta de Débito podrás realizar operaciones, como pagar tus servicios, realizar transferencias y mucho más."
            return {
                "speech": speech,
                "displayText": speech
            }
        else:
            speech = "¡Ya diste el primer paso :)!, ahora solo debes acercarte a nuestras oficinas para obtener la Tarjeta de Débito que te permitirá acceder a todos nuestros canales de atención: Banca por Internet, Banca Móvil, Banca por Teléfono, entre otros. Con tu Tarjeta de Débito podrás realizar operaciones, como pagar tus servicios, realizar transferencias y mucho más."
            return {
                "speech": speech,
                "displayText": speech,
                "messages": [
				{
					"type": 0,
					"speech": speech,
                    "platform": "facebook"
				}
			]
            }

    if intentName == "no.secuencial.no.parametrica.pg2-options":
        parameters = result.get("parameters")
        tiposdeproducto = parameters.get("tiposdeproducto")

        if tiposdeproducto == "Cuenta.Sueldo":
            speech = "Puedes realizar depósitos ilimitados, 2 operaciones sin costo (retiros de dinero y transferencias entre cuentas) en la misma localidad donde se contrató tu cuenta."
            return {
                "speech": speech,
                "displayText": speech
            }
        else:
            speech = "Puedes realizar depósitos ilimitados sin costo y hasta 1 operación mensual sin costo por retiros de dinero y transferencias entre cuentas (en la misma localidad donde se contrató la cuenta)."
            return {
                "speech": speech,
                "displayText": speech,
                "messages": [
				{
					"type": 0,
					"speech": speech,
                    "platform": "facebook"
				}
			]
            }

    if intentName == "no.secuencial.no.parametrica.pg3-options":
        parameters = result.get("parameters")
        tiposdeproducto = parameters.get("tiposdeproducto")

        if tiposdeproducto == "Cuenta.Sueldo":
            speech = "En cajeros del BBVA Continental puedes retirar ilimitadamente sin costo a nivel nacional.\nAdemás, puedes retirar en todos los cajeros de la red VISA en la misma ciudad donde se abrió la cuenta según el ingreso neto mensual:\n\n- 1 retiro: Hasta S/1,799.\n- 2 retiros: Desde S/1,800 hasta S/3,499.\n- 4 retiros: Desde S/3,500 hasta S/6,999.\n- 10 retiros: Desde S/7,000 a más.\n\nPara disfrutar del beneficio la Cuenta Sueldo debe estar asociada a una tarjeta de crédito o débito del BBVA Continental y aplica después de recibir un mes de abono de sueldo."
            return {
                "speech": speech,
                "displayText": speech
            }
        else:
            speech = "Ilimitados: retiro de dinero a través de todos los cajeros BBVA a nivel nacional y transferencias entre cuentas (realizados en la misma localidad donde se contrató la cuenta) y consultas de saldos y movimientos."
            return {
                "speech": speech,
                "displayText": speech,
                "messages": [
				{
					"type": 0,
					"speech": speech,
                    "platform": "facebook"
				}
			]
            }

    if intentName == "no.secuencial.no.parametrica.pg4-options":
        parameters = result.get("parameters")
        tiposdeproducto = parameters.get("tiposdeproducto")

        if tiposdeproducto == "Cuenta.Sueldo":
            speech = "Tu tarjeta de débito puedes utilizarla en la amplia red de establecimientos afiliados a Visa"
            return {
                "speech": speech,
                "displayText": speech
            }
        else:
            speech = "Tu tarjeta de débito puedes utilizarla en la amplia red de establecimientos afiliados a Visa"
            return {
                "speech": speech,
                "displayText": speech,
                "messages": [
				{
					"type": 0,
					"speech": speech,
                    "platform": "facebook"
				}
			]
            }

    if intentName == "no.secuencial.no.parametrica.pg5-options":
        parameters = result.get("parameters")
        tiposdeproducto = parameters.get("tiposdeproducto")

        if tiposdeproducto == "Cuenta.Sueldo":
            speech = "Sí, cuando lo necesites."
            return {
                "speech": speech,
                "displayText": speech
            }
        else:
            speech = "Sí. Solo en caso de haber participado de la campaña en vigencia canjeando un premio por apertura, se realizará una retención por el importe y tiempo indicado en las condiciones de la misma."
            return {
                "speech": speech,
                "displayText": speech,
                "messages": [
				{
					"type": 0,
					"speech": speech,
                    "platform": "facebook"
				}
			]
            }

    if intentName == "no.secuencial.no.parametrica.pg6-options":
        parameters = result.get("parameters")
        tiposdeproducto = parameters.get("tiposdeproducto")

        if tiposdeproducto == "Cuenta.Sueldo":
            speech = "No se reciben estados de cuenta mensuales, sin embargo se pueden emitirse si así lo solicitas."
            return {
                "speech": speech,
                "displayText": speech
            }
        else:
            speech = "No se reciben estados de cuenta mensuales, sin embargo se pueden emitirse si así lo solicitas."
            return {
                "speech": speech,
                "displayText": speech,
                "messages": [
				{
					"type": 0,
					"speech": speech,
                    "platform": "facebook"
				}
			]
            }

    if intentName == "no.secuencial.parametrica.pg1":
        parameters = result.get("parameters")
        tiposdeproducto = parameters.get("tiposdeproducto")

        if tiposdeproducto == "Cuenta.Sueldo":
            speech = "Es una cuenta en la que puedes realizar operaciones en Soles y en Dólares al tipo de cambio del día. No mantiene los saldos separados por tipo de moneda. Tu saldo se guarda en la moneda que eliges al abrir la cuenta."
            return {
                "speech": speech,
                "displayText": speech
            }
        else:
            speech = "Es una cuenta en la que puedes realizar operaciones en Soles y en Dólares a un tipo de cambio especial. No mantiene los saldos separados por tipo de moneda. Tu saldo se guarda en la moneda que eliges al abrir la cuenta."
            return {
                "speech": speech,
                "displayText": speech,
                "messages": [
				{
					"type": 0,
					"speech": speech,
                    "platform": "facebook"
				}
			]
            }
    if intentName == "no.secuencial.parametrica.pg2":
        parameters = result.get("parameters")
        tiposdeproducto = parameters.get("tiposdeproducto")

        if tiposdeproducto == "Cuenta.Sueldo":
            speech = "El mantenimiento de la cuenta sueldo no cuesta nada, siempre y cuando tu Cuenta Sueldo reciba abonos de Pago de Haberes de manera consecutiva."
            return {
                "speech": speech,
                "displayText": speech
            }
        else:
            speech = "El mantenimiento de cuenta mensual es variable, de acuerdo al saldo medio de tu cuenta:\n\n- Hasta S/ 900 o $ 300: S/ 8.00 o $ 3.00, respectivamente.\n- Mayor a S/ 900 o $ 300: SIN COSTO."
            return {
                "speech": speech,
                "displayText": speech,
                "messages": [
				{
					"type": 0,
					"speech": speech,
                    "platform": "facebook"
				}
			]
            }
    if intentName == "no.secuencial.parametrica.pg3":
        parameters = result.get("parameters")
        tiposdeproducto = parameters.get("tiposdeproducto")

        if tiposdeproducto == "Cuenta.Sueldo":
            speech = "Sí, los saldos están cubiertos por Fondo de Seguro Depósito hasta por S/98,894.00 (periodo junio – agosto 2018 N° B-2242-2018, sujeto a modificación trimestral por la SBS)."
            return {
                "speech": speech,
                "displayText": speech
            }
        else:
            speech = "Sí, los saldos están cubiertos por Fondo de Seguro Depósito hasta por S/98,894.00 (periodo junio – agosto 2018 N° B-2242-2018, sujeto a modificación trimestral por la SBS)."
            return {
                "speech": speech,
                "displayText": speech,
                "messages": [
				{
					"type": 0,
					"speech": speech,
                    "platform": "facebook"
				}
			]
            }
    if intentName == "no.secuencial.parametrica.pg4":
        parameters = result.get("parameters")
        tiposdeproducto = parameters.get("tiposdeproducto")

        if tiposdeproducto == "Cuenta.Sueldo":
            speech = "No necesitas de un depósito mínimo para abrir tu Cuenta Sueldo."
            return {
                "speech": speech,
                "displayText": speech
            }
        else:
            speech = "El depósito mínimo de apertura es S/ 300 o US$100."
            return {
                "speech": speech,
                "displayText": speech,
                "messages": [
				{
					"type": 0,
					"speech": speech,
                    "platform": "facebook"
				}
			]
            }
    if intentName == "no.secuencial.parametrica.pg5":
        parameters = result.get("parameters")
        tiposdeproducto = parameters.get("tiposdeproducto")

        if tiposdeproducto == "Cuenta.Sueldo":
            speech = "Sí, siempre."
            return {
                "speech": speech,
                "displayText": speech
            }
        else:
            speech = "Sí, siempre."
            return {
                "speech": speech,
                "displayText": speech,
                "messages": [
				{
					"type": 0,
					"speech": speech,
                    "platform": "facebook"
				}
			]
            }
    
    if intentName == "palabra.busqueda.":
        parameters = result.get("parameters")
        tiposdeproducto = parameters.get("tiposdeproducto")

        if tiposdeproducto == "Cuenta.Sueldo":
            speech = "Sí, siempre."
            return {
                "speech": speech,
                "displayText": speech
            }
        else:
            speech = "Sí, siempre."
            return {
                "speech": speech,
                "displayText": speech,
                "messages": [
				{
					"type": 0,
					"speech": speech,
                    "platform": "facebook"
				}
			]
            }
    
    #-----------------------------------------

    if intentName == "c.palabras.sueltas.operaciones-next" or intentName == "c.palabras.sueltas.context.operaciones" or intentName == "c.palabras.sueltas.tipo.producto.operaciones":
        parameters = result.get("parameters")
        tiposdeproducto = parameters.get("tiposdeproducto")

        if tiposdeproducto == "Cuenta.Sueldo":
            speech = ""
            return {
                "speech": "",
                "messages": [
                                {
                                "type": 0,
                                "platform": "facebook",
                                "speech": "Tal vez te referiste a lo siguiente: 🤔"
                                },
                                {
                                "type": 4,
                                "platform": "facebook",
                                "payload": {
                                    "facebook": {
                                    "attachment": {
                                        "type": "template",
                                        "payload": {
                                        "template_type": "list",
                                        "top_element_style": "compact",
                                        "elements": [
                                            {
                                            "title": "Operaciones Libres en Cajeros Automáticos",
                                            "subtitle": "¿Cuántas operaciones libres tengo en Cajeros Automáticos del BBVA Continental?",                                            
                                            "image_url": "https://raw.githubusercontent.com/idusertbs/bytebot-bbva-faq-webhook/Developer/assets/pics/IMG_0032-1.jpg",
                                            "buttons": [
                                                {
                                                "title": "Ver Respuesta",
                                                "type": "postback",
                                                "payload": "cs.from.lista.sucesiva.operaciones.ca"
                                                }
                                            ]
                                            },
                                            {
                                            "title": "¿Cómo hago operaciones en la web?",
                                            "subtitle": "¿Si abrí mi Cuenta por la web, ¿Cómo puedo realizar operaciones en ella?",                                            
                                            "buttons": [
                                                {
                                                "title": "Ver Respuesta",
                                                "type": "postback",
                                                "payload": "cs_from_lista_sucesiva_info_guia"
                                                }
                                            ]
                                            },
                                            {
                                            "title": "Operaciones libres en Ventanilla",
                                            "subtitle": "¿Cuántas operaciones libres tengo por ventanilla?",                                            
                                            "buttons": [
                                                {
                                                "title": "Ver Respuesta",
                                                "type": "postback",
                                                "payload": "cs_from_lista_sucesiva_operaciones_ventanilla"
                                                }
                                            ]
                                            }
                                        ]
                                        }
                                    }
                                    }
                                }
                                }
                            ]
            }
        else:
            speech = "Sí, siempre."
            return {
                "speech": speech,
                "messages": [
                                {
                                "type": 0,
                                "platform": "facebook",
                                "speech": "Tal vez te referiste a lo siguiente: 🤔"
                                },
                                {
                                "type": 4,
                                "platform": "facebook",
                                "payload": {
                                    "facebook": {
                                    "attachment": {
                                        "type": "template",
                                        "payload": {
                                        "template_type": "list",
                                        "top_element_style": "compact",
                                        "elements": [
                                            {
                                            "title": "Operaciones Libres en Cajeros Automáticos",
                                            "subtitle": "¿Cuántas operaciones libres tengo en Cajeros Automáticos del BBVA Continental?",                                            
                                            "image_url": "https://raw.githubusercontent.com/idusertbs/bytebot-bbva-faq-webhook/Developer/assets/pics/IMG_0032-1.jpg",
                                            "buttons": [
                                                {
                                                "title": "Ver Respuesta",
                                                "type": "postback",
                                                "payload": "cg.from.lista.sucesiva.operaciones.ca"
                                                }
                                            ]
                                            },
                                            {
                                            "title": "¿Cómo hago operaciones en la web?",
                                            "subtitle": "¿Si abrí mi Cuenta por la web, ¿Cómo puedo realizar operaciones en ella?",                                            
                                            "buttons": [
                                                {
                                                "title": "Ver Respuesta",
                                                "type": "postback",
                                                "payload": "cg_from_lista_sucesiva_info_guia"
                                                }
                                            ]
                                            },
                                            {
                                            "title": "Cantidad de Operaciones Libres",
                                            "subtitle": "¿Cuántas operaciones libres tengo por ventanilla?",                                            
                                            "buttons": [
                                                {
                                                "title": "Ver Respuesta",
                                                "type": "postback",
                                                "payload": "cg_from_lista_sucesiva_operaciones_ventanilla"
                                                }
                                            ]
                                            }
                                        ]
                                        }
                                    }
                                    }
                                }
                                }
                            ]
            }

    if intentName == "c.palabras.sueltas.bimoneda-next" or intentName == "c.palabras.sueltas.context.bimoneda" or intentName == "c.palabras.sueltas.tipo.producto.bimoneda":
        parameters = result.get("parameters")
        tiposdeproducto = parameters.get("tiposdeproducto")

        if tiposdeproducto == "Cuenta.Sueldo":
            speech = ""
            return {
                "speech": "",
                "messages": [
                    {
                    "type": 0,
                    "platform": "facebook",
                    "speech": "Tal vez te referiste a lo siguiente: 🤔"
                    },
                    {
                    "type": 4,
                    "platform": "facebook",
                    "payload": {
                        "facebook": {
                        "attachment": {
                            "type": "template",
                            "payload": {
                            "template_type": "generic",
                            "elements": [
                                {
                                "title": "Cuenta Sueldo Bimoneda",
                                "subtitle": "¿Qué es una cuenta sueldo bimoneda?",
                                "buttons": [
                                    {
                                    "type": "postback",
                                    "title": "Ver respuesta",
                                    "payload": "cs_from_lista_sucesiva_info_bimoneda"
                                    }
                                ]
                                }
                            ]
                            }
                        }
                        }
                    }
                    }
                ]
                
            }
        else:
            speech = "Sí, siempre."
            return {
                "speech": speech,
                "messages": [
                    {
                    "type": 0,
                    "platform": "facebook",
                    "speech": "Tal vez te referiste a lo siguiente: 🤔"
                    },
                    {
                    "type": 4,
                    "platform": "facebook",
                    "payload": {
                        "facebook": {
                        "attachment": {
                            "type": "template",
                            "payload": {
                            "template_type": "generic",
                            "elements": [
                                {
                                "title": "Cuenta Ganadora Bimoneda",
                                "subtitle": "¿Qué es una cuenta ganadora bimoneda?",
                                "buttons": [
                                    {
                                    "type": "postback",
                                    "title": "Ver respuesta",
                                    "payload": "cs_from_lista_sucesiva_info_mantenimiento"
                                    }
                                ]
                                }
                            ]
                            }
                        }
                        }
                    }
                    }
                ]
                
            }
    

    if intentName == "c.palabras.sueltas.mantenimiento-next" or intentName == "c.palabras.sueltas.context.mantenimiento" or intentName == "c.palabras.sueltas.tipo.producto.mantenimiento":
        parameters = result.get("parameters")
        tiposdeproducto = parameters.get("tiposdeproducto")

        if tiposdeproducto == "Cuenta.Sueldo":
            speech = ""
            return {
                "speech": "",
                "messages": [
                    {
                    "type": 0,
                    "platform": "facebook",
                    "speech": "Tal vez te referiste a lo siguiente: 🤔"
                    },
                    {
                    "type": 4,
                    "platform": "facebook",
                    "payload": {
                        "facebook": {
                        "attachment": {
                            "type": "template",
                            "payload": {
                            "template_type": "generic",
                            "elements": [
                                {
                                "title": "Monto por Mantenimiento",
                                "subtitle": "¿Cuánto pago al mes por mantenimiento de mi Cuenta Sueldo y mi Tarjeta de Débito?",
                                "buttons": [
                                    {
                                    "type": "postback",
                                    "title": "Ver respuesta",
                                    "payload": "cg_from_lista_sucesiva_info_mantenimiento"
                                    }
                                ]
                                }
                            ]
                            }
                        }
                        }
                    }
                    }
                ]
                
            }
        else:
            speech = "Sí, siempre."
            return {
                "speech": speech,
                "messages": [
                    {
                    "type": 0,
                    "platform": "facebook",
                    "speech": "Tal vez te referiste a lo siguiente: 🤔"
                    },
                    {
                    "type": 4,
                    "platform": "facebook",
                    "payload": {
                        "facebook": {
                        "attachment": {
                            "type": "template",
                            "payload": {
                            "template_type": "generic",
                            "elements": [
                                {
                                "title": "Monto por Mantenimiento",
                                "subtitle": "¿Cuánto pago al mes por mantenimiento de mi Cuenta Ganadora?",
                                "buttons": [
                                    {
                                    "type": "postback",
                                    "title": "Ver respuesta",
                                    "payload": "cg_from_lista_sucesiva_info_bimoneda"
                                    }
                                ]
                                }
                            ]
                            }
                        }
                        }
                    }
                    }
                ]
                
            }
    
    if intentName == "c.palabras.sueltas.fondo-next" or intentName == "c.palabras.sueltas.context.fondo"  or intentName == "c.palabras.sueltas.tipo.producto.fondo":
        parameters = result.get("parameters")
        tiposdeproducto = parameters.get("tiposdeproducto")

        if tiposdeproducto == "Cuenta.Sueldo":
            speech = ""
            return {
                "speech": "",
                "messages": [
                                {
                                "type": 0,
                                "platform": "facebook",
                                "speech": "Tal vez te referiste a lo siguiente: 🤔"
                                },
                                {
                                "type": 4,
                                "platform": "facebook",
                                "payload": {
                                    "facebook": {
                                    "attachment": {
                                        "type": "template",
                                        "payload": {
                                        "template_type": "list",
                                        "top_element_style": "compact",
                                        "elements": [
                                            {
                                            "title": "Disposición de fondos",
                                            "subtitle": "¿Puedo disponer de los fondos en cualquier momento?",                                            
                                            "buttons": [
                                                {
                                                "title": "Ver Respuesta",
                                                "type": "postback",
                                                "payload": "cs_from_lista_sucesiva_info_fondos"
                                                }
                                            ]
                                            },
                                            {
                                            "title": "¿Mi saldo está protegido?",
                                            "subtitle": "¿Mi saldo está cubierto por el Fondo de Seguros de Depósito?",                                            
                                            "buttons": [
                                                {
                                                "title": "Ver Respuesta",
                                                "type": "postback",
                                                "payload": "cs_from_lista_sucesiva_info_seguros"
                                                }
                                            ]
                                            }
                                        ]
                                        }
                                    }
                                    }
                                }
                                }
                            ]
            }
        else:
            speech = "Sí, siempre."
            return {
                "speech": speech,
                "messages": [
                                {
                                "type": 0,
                                "platform": "facebook",
                                "speech": "Tal vez te referiste a lo siguiente: 🤔"
                                },
                                {
                                "type": 4,
                                "platform": "facebook",
                                "payload": {
                                    "facebook": {
                                    "attachment": {
                                        "type": "template",
                                        "payload": {
                                        "template_type": "list",
                                        "top_element_style": "compact",
                                        "elements": [
                                            {
                                            "title": "Disposición de Fondos",
                                            "subtitle": "¿Puedo disponer de los fondos en cualquier momento?",                                            
                                            "buttons": [
                                                {
                                                "title": "Ver Respuesta",
                                                "type": "postback",
                                                "payload": "cg_from_lista_sucesiva_info_fondos"
                                                }
                                            ]
                                            },
                                            {
                                            "title": "¿Mi saldo está protegido?",
                                            "subtitle": "¿Mi saldo está cubierto por el Fondo de Seguros de Depósito?",                                            
                                            "buttons": [
                                                {
                                                "title": "Ver Respuesta",
                                                "type": "postback",
                                                "payload": "cg_from_lista_sucesiva_info_seguros"
                                                }
                                            ]
                                            }
                                        ]
                                        }
                                    }
                                    }
                                }
                                }
                            ]
            }
    
    if intentName == "c.palabras.sueltas.tarjeta-next" or intentName == "c.palabras.sueltas.context.tarjeta" or intentName == "c.palabras.sueltas.tipo.producto.tarjeta":
        parameters = result.get("parameters")
        tiposdeproducto = parameters.get("tiposdeproducto")

        if tiposdeproducto == "Cuenta.Sueldo":
            speech = ""
            return {
                "speech": "",
                "messages": [
                                {
                                "type": 0,
                                "platform": "facebook",
                                "speech": "Tal vez te referiste a lo siguiente: 🤔"
                                },
                                {
                                "type": 4,
                                "platform": "facebook",
                                "payload": {
                                    "facebook": {
                                    "attachment": {
                                        "type": "template",
                                        "payload": {
                                        "template_type": "list",
                                        "top_element_style": "compact",
                                        "elements": [
                                            {
                                            "title": "¿Uso de mi tarjeta de débito en terminales POS?",
                                            "subtitle": "¿Puedo usar mi tarjeta de débito en establecimientos comerciales que tengan terminales POS?",                                            
                                            "buttons": [
                                                {
                                                "title": "Ver Respuesta",
                                                "type": "postback",
                                                "payload": "cs_from_lista_sucesiva_operaciones_ec"
                                                }
                                            ]
                                            },
                                            {
                                            "title": "¿Costo del mantenimiento al mes?",
                                            "subtitle": "¿Cuánto pago al mes por mantenimiento de mi Cuenta y mi Tarjeta de Débito?",                                            
                                            "buttons": [
                                                {
                                                "title": "Ver Respuesta",
                                                "type": "postback",
                                                "payload": "cs_from_lista_sucesiva_info_mantenimiento"
                                                }
                                            ]
                                            }
                                        ]
                                        }
                                    }
                                    }
                                }
                                }
                            ]
            }
        else:
            speech = "Sí, siempre."
            return {
                "speech": speech,
                "messages": [
                                {
                                "type": 0,
                                "platform": "facebook",
                                "speech": "Tal vez te referiste a lo siguiente: 🤔"
                                },
                                {
                                "type": 4,
                                "platform": "facebook",
                                "payload": {
                                    "facebook": {
                                    "attachment": {
                                        "type": "template",
                                        "payload": {
                                        "template_type": "list",
                                        "top_element_style": "compact",
                                        "elements": [
                                            {
                                            "title": "¿Uso de mi tarjeta de débito en terminales POS?",
                                            "subtitle": "¿Puedo usar mi tarjeta de débito en establecimientos comerciales que tengan terminales POS?",                                            
                                            "buttons": [
                                                {
                                                "title": "Ver Respuesta",
                                                "type": "postback",
                                                "payload": "cg_from_lista_sucesiva_operaciones_ec"
                                                }
                                            ]
                                            },
                                            {
                                            "title": "¿Costo del mantenimiento al mes?",
                                            "subtitle": "¿Cuánto pago al mes por mantenimiento de mi Cuenta Ganadora",                                            
                                            "buttons": [
                                                {
                                                "title": "Ver Respuesta",
                                                "type": "postback",
                                                "payload": "cg_from_lista_sucesiva_info_mantenimiento"
                                                }
                                            ]
                                            }
                                        ]
                                        }
                                    }
                                    }
                                }
                                }
                            ]
            }
    
    if intentName == "c.palabras.sueltas.abrir-next" or intentName == "c.palabras.sueltas.context.abrir" or intentName == "c.palabras.sueltas.tipo.producto.abrir":
        parameters = result.get("parameters")
        tiposdeproducto = parameters.get("tiposdeproducto")

        if tiposdeproducto == "Cuenta.Sueldo":
            speech = ""
            return {
                "speech": "",
                "messages": [
                    {
                    "type": 0,
                    "platform": "facebook",
                    "speech": "Tal vez te referiste a lo siguiente: 🤔"
                    },
                    {
                    "type": 4,
                    "platform": "facebook",
                    "payload": {
                        "facebook": {
                        "attachment": {
                            "type": "template",
                            "payload": {
                            "template_type": "generic",
                            "elements": [
                                {
                                "title": "Costo de apertura de cuenta sueldo",
                                "subtitle": "¿Cuánto dinero necesito para abrir una Cuenta Sueldo?",
                                "buttons": [
                                    {
                                    "type": "postback",
                                    "title": "Ver respuesta",
                                    "payload": "cs_from_lista_sucesiva_info_costos"
                                    }
                                ]
                                }
                            ]
                            }
                        }
                        }
                    }
                    }
                ]
                
            }
        else:
            speech = "Sí, siempre."
            return {
                "speech": speech,
                "messages": [
                    {
                    "type": 0,
                    "platform": "facebook",
                    "speech": "Tal vez te referiste a lo siguiente: 🤔"
                    },
                    {
                    "type": 4,
                    "platform": "facebook",
                    "payload": {
                        "facebook": {
                        "attachment": {
                            "type": "template",
                            "payload": {
                            "template_type": "generic",
                            "elements": [
                                {
                                "title": "Costo de apertura de cuenta ganadora",
                                "subtitle": "¿Cuánto dinero necesito para abrir una Cuenta Ganadora?",
                                "buttons": [
                                    {
                                    "type": "postback",
                                    "title": "Ver respuesta",
                                    "payload": "cg_from_lista_sucesiva_info_costos"
                                    }
                                ]
                                }
                            ]
                            }
                        }
                        }
                    }
                    }
                ]
                
            }

    if intentName == "c.palabras.sueltas.franquicia-next" or intentName == "c.palabras.sueltas.context.franquicia" or intentName == "c.palabras.sueltas.tipo.producto.franquicia":
        parameters = result.get("parameters")
        tiposdeproducto = parameters.get("tiposdeproducto")

        if tiposdeproducto == "Cuenta.Sueldo":
            speech = ""
            return {
                "speech": "",
                "messages": [
                    {
                    "type": 0,
                    "platform": "facebook",
                    "speech": "Tal vez te referiste a lo siguiente: 🤔"
                    },
                    {
                    "type": 4,
                    "platform": "facebook",
                    "payload": {
                        "facebook": {
                        "attachment": {
                            "type": "template",
                            "payload": {
                            "template_type": "generic",
                            "elements": [
                                {
                                "title": "Franquicia en mi Cuenta Sueldo",
                                "subtitle": "¿Qué es una franquicia en mi cuenta Sueldo?",
                                "buttons": [
                                    {
                                    "type": "postback",
                                    "title": "Ver respuesta",
                                    "payload": "cs_from_lista_sucesiva_info_franquicias"
                                    }
                                ]
                                }
                            ]
                            }
                        }
                        }
                    }
                    }
                ]
                
            }
        else:
            speech = "Sí, siempre."
            return {
                "speech": speech,
                "messages": [
                    {
                    "type": 0,
                    "platform": "facebook",
                    "speech": "La franquicia solo corresponde a la cuenta sueldo :/"
                    }
                ]
                
            }

    if intentName == "c.palabras.sueltas.estados-next" or intentName == "c.palabras.sueltas.context.estados" or intentName == "c.palabras.sueltas.tipo.producto.estados":
        parameters = result.get("parameters")
        tiposdeproducto = parameters.get("tiposdeproducto")

        if tiposdeproducto == "Cuenta.Sueldo":
            speech = ""
            return {
                "speech": "",
                "messages": [
                    {
                    "type": 0,
                    "platform": "facebook",
                    "speech": "Tal vez te referiste a lo siguiente: 🤔"
                    },
                    {
                    "type": 4,
                    "platform": "facebook",
                    "payload": {
                        "facebook": {
                        "attachment": {
                            "type": "template",
                            "payload": {
                            "template_type": "generic",
                            "elements": [
                                {
                                "title": "¿Mensualmente recibo estados de cuenta?",
                                "buttons": [
                                    {
                                    "type": "postback",
                                    "title": "Ver respuesta",
                                    "payload": "cs_from_lista_sucesiva_info_estados"
                                    }
                                ]
                                }
                            ]
                            }
                        }
                        }
                    }
                    }
                ]
                
            }
        else:
            speech = "Sí, siempre."
            return {
                "speech": speech,
                "messages": [
                    {
                    "type": 0,
                    "platform": "facebook",
                    "speech": "Tal vez te referiste a lo siguiente: 🤔"
                    },
                    {
                    "type": 4,
                    "platform": "facebook",
                    "payload": {
                        "facebook": {
                        "attachment": {
                            "type": "template",
                            "payload": {
                            "template_type": "generic",
                            "elements": [
                                {
                                "title": "¿Mensualmente recibo estados de cuenta?",
                                "buttons": [
                                    {
                                    "type": "postback",
                                    "title": "Ver respuesta",
                                    "payload": "cg_from_lista_sucesiva_info_estados"
                                    }
                                ]
                                }
                            ]
                            }
                        }
                        }
                    }
                    }
                ]
                
            }
    if intentName == "c.palabras.sueltas.promociones-next" or intentName == "c.palabras.sueltas.context.promociones" or intentName == "c.palabras.sueltas.tipo.producto.promociones":
        parameters = result.get("parameters")
        tiposdeproducto = parameters.get("tiposdeproducto")

        if tiposdeproducto == "Cuenta.Ganadora":
            speech = ""
            return {
                "speech": "",
                "messages": [
                    {
                    "type": 0,
                    "platform": "facebook",
                    "speech": "Tal vez te referiste a lo siguiente: 🤔"
                    },
                    {
                    "type": 4,
                    "platform": "facebook",
                    "payload": {
                        "facebook": {
                        "attachment": {
                            "type": "template",
                            "payload": {
                            "template_type": "generic",
                            "elements": [
                                {
                                "title": "¿Cómo participo de los sorteos?",
                                "buttons": [
                                    {
                                    "type": "postback",
                                    "title": "Ver respuesta",
                                    "payload": "cg_from_lista_sucesiva_info_sorteos"
                                    }
                                ]
                                }
                            ]
                            }
                        }
                        }
                    }
                    }
                ]
                
            }
        else:
            speech = "Sí, siempre."
            return {
                "speech": speech,
                "messages": [
                    {
                    "type": 0,
                    "platform": "facebook",
                    "speech": "Los sorteos o ese tipo de promociones solo corresponden a la cuenta ganadora :/"
                    }
                ]
                
            }
    
    if intentName == "c.palabras.sueltas.depositos-next" or intentName == "c.palabras.sueltas.context.depositos" or intentName == "c.palabras.sueltas.tipo.producto.depositos":
        parameters = result.get("parameters")
        tiposdeproducto = parameters.get("tiposdeproducto")

        if tiposdeproducto == "Cuenta.Sueldo":
            speech = ""
            return {
                "speech": "",
                "messages": [
                    {
                    "type": 0,
                    "platform": "facebook",
                    "speech": "Tal vez te referiste a lo siguiente: 🤔"
                    },
                    {
                    "type": 4,
                    "platform": "facebook",
                    "payload": {
                        "facebook": {
                        "attachment": {
                            "type": "template",
                            "payload": {
                            "template_type": "generic",
                            "elements": [
                                {
                                "title": "¿Nuevos depósitos?",
                                "subtitle": "¿Puedo hacer nuevos depósitos en mi Cuenta una vez abierta?",
                                "buttons": [
                                    {
                                    "type": "postback",
                                    "title": "Ver respuesta",
                                    "payload": "cs_from_lista_sucesiva_operaciones_depositos"
                                    }
                                ]
                                }
                            ]
                            }
                        }
                        }
                    }
                    }
                ]
                
            }
        else:
            speech = "Sí, siempre."
            return {
                "speech": speech,
                "messages": [
                    {
                    "type": 0,
                    "platform": "facebook",
                    "speech": "Tal vez te referiste a lo siguiente: 🤔"
                    },
                    {
                    "type": 4,
                    "platform": "facebook",
                    "payload": {
                        "facebook": {
                        "attachment": {
                            "type": "template",
                            "payload": {
                            "template_type": "generic",
                            "elements": [
                                {
                                "title": "¿Nuevos depósitos?",
                                "subtitle": "¿Puedo hacer nuevos depósitos en mi Cuenta una vez abierta?",
                                "buttons": [
                                    {
                                    "type": "postback",
                                    "title": "Ver respuesta",
                                    "payload": "cg_from_lista_sucesiva_operaciones_depositos"
                                    }
                                ]
                                }
                            ]
                            }
                        }
                        }
                    }
                    }
                ]
                
            }
    if intentName == "c.palabras.sueltas.seguro-next" or intentName == "c.palabras.sueltas.context.seguro" or intentName == "c.palabras.sueltas.tipo.producto.seguro":
        parameters = result.get("parameters")
        tiposdeproducto = parameters.get("tiposdeproducto")

        if tiposdeproducto == "Cuenta.Sueldo":
            speech = ""
            return {
                "speech": "",
                "messages": [
                    {
                    "type": 0,
                    "platform": "facebook",
                    "speech": "Tal vez te referiste a lo siguiente: 🤔"
                    },
                    {
                    "type": 4,
                    "platform": "facebook",
                    "payload": {
                        "facebook": {
                        "attachment": {
                            "type": "template",
                            "payload": {
                            "template_type": "generic",
                            "elements": [
                                {
                                "title": "¿Mi saldo está protegido?",
                                "subtitle": "¿Los saldos de mi Cuenta están cubiertos por el Fondo de Seguros de Depósito?",
                                "buttons": [
                                    {
                                    "type": "postback",
                                    "title": "Ver respuesta",
                                    "payload": "cs_from_lista_sucesiva_info_seguros"
                                    }
                                ]
                                }
                            ]
                            }
                        }
                        }
                    }
                    }
                ]
                
            }
        else:
            speech = "Sí, siempre."
            return {
                "speech": speech,
                "messages": [
                    {
                    "type": 0,
                    "platform": "facebook",
                    "speech": "Tal vez te referiste a lo siguiente: 🤔"
                    },
                    {
                    "type": 4,
                    "platform": "facebook",
                    "payload": {
                        "facebook": {
                        "attachment": {
                            "type": "template",
                            "payload": {
                            "template_type": "generic",
                            "elements": [
                                {
                                "title": "¿Mi saldo está protegido?",
                                "subtitle": "¿Los saldos de mi Cuenta están cubiertos por el Fondo de Seguros de Depósito?",
                                "buttons": [
                                    {
                                    "type": "postback",
                                    "title": "Ver respuesta",
                                    "payload": "cg_from_lista_sucesiva_info_seguros"
                                    }
                                ]
                                }
                            ]
                            }
                        }
                        }
                    }
                    }
                ]
                
            }
    if intentName == "c.palabras.sueltas.gano-next" or intentName == "c.palabras.sueltas.context.gano" or intentName == "c.palabras.sueltas.tipo.producto.gano":
        parameters = result.get("parameters")
        tiposdeproducto = parameters.get("tiposdeproducto")

        if tiposdeproducto == "Cuenta.Ganadora":
            speech = ""
            return {
                "speech": "",
                "messages": [
                    {
                    "type": 0,
                    "platform": "facebook",
                    "speech": "Tal vez te referiste a lo siguiente: 🤔"
                    },
                    {
                    "type": 4,
                    "platform": "facebook",
                    "payload": {
                        "facebook": {
                        "attachment": {
                            "type": "template",
                            "payload": {
                            "template_type": "generic",
                            "elements": [
                                {
                                "title": "Ganancia de intereses",
                                "subtitle": "¿Cada cuánto tiempo gano intereses?",
                                "buttons": [
                                    {
                                    "type": "postback",
                                    "title": "Ver respuesta",
                                    "payload": "cg_from_lista_sucesiva_info_intereses"
                                    }
                                ]
                                }
                            ]
                            }
                        }
                        }
                    }
                    }
                ]
                
            }
        else:
            speech = "Sí, siempre."
            return {
                "speech": speech,
                "messages": [
                    {
                    "type": 0,
                    "platform": "facebook",
                    "speech": "Los sorteos o ese tipo de promociones solo corresponden a la cuenta ganadora :/"
                    }
                ]
                
            }
    
    if intentName == "c.palabras.sueltas.web-next" or intentName == "c.palabras.sueltas.context.web" or intentName == "c.palabras.sueltas.tipo.producto.web":
        parameters = result.get("parameters")
        tiposdeproducto = parameters.get("tiposdeproducto")

        if tiposdeproducto == "Cuenta.Sueldo":
            speech = ""
            return {
                "speech": "",
                "messages": [
                    {
                    "type": 0,
                    "platform": "facebook",
                    "speech": "Tal vez te referiste a lo siguiente: 🤔"
                    },
                    {
                    "type": 4,
                    "platform": "facebook",
                    "payload": {
                        "facebook": {
                        "attachment": {
                            "type": "template",
                            "payload": {
                            "template_type": "generic",
                            "elements": [
                                {
                                "title": "Operaciones en la web",
                                "subtitle": "Si abrí mi Cuenta por la web, ¿Cómo puedo realizar operaciones en ella?",
                                "buttons": [
                                    {
                                    "type": "postback",
                                    "title": "Ver respuesta",
                                    "payload": "cs_from_lista_sucesiva_info_guia"
                                    }
                                ]
                                }
                            ]
                            }
                        }
                        }
                    }
                    }
                ]
                
            }
        else:
            speech = "Sí, siempre."
            return {
                "speech": speech,
                "messages": [
                    {
                    "type": 0,
                    "platform": "facebook",
                    "speech": "Tal vez te referiste a lo siguiente: 🤔"
                    },
                    {
                    "type": 4,
                    "platform": "facebook",
                    "payload": {
                        "facebook": {
                        "attachment": {
                            "type": "template",
                            "payload": {
                            "template_type": "generic",
                            "elements": [
                                {
                                "title": "Operaciones en la web",
                                "subtitle": "Si abrí mi Cuenta por la web, ¿Cómo puedo realizar operaciones en ella?",
                                "buttons": [
                                    {
                                    "type": "postback",
                                    "title": "Ver respuesta",
                                    "payload": "cg_from_lista_sucesiva_info_guia"
                                    }
                                ]
                                }
                            ]
                            }
                        }
                        }
                    }
                    }
                ]
                
            }

    
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')

















