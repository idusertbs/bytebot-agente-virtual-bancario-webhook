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
    
    if intentName == "verificacion":        
        parameters = result.get("parameters")
        documento = parameters.get("number")
        r=requests.get('http://181.177.228.114:5001/clientes/' + str(documento))
        json_object = r.json()
        error = 0
        try:
            json_object["error"]
        except KeyError as e:
            error = 1

        if error == 1:
            speech = "Eres nuestro cliente"
        else:
            speech = "No eres nuestro cliente"

        return {
            "speech": speech,
            "displayText": speech,
            "source": "bytebot-virtual-agent-webhook"

        }


        
    
    
    
    
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')

















