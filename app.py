#!/usr/bin/python3
#(c) 2021 Will Smith - WILL@WIFI-GUYS.COM

from flask import Flask, request, abort
from pycentral.base import ArubaCentralBase
import json
import creds
import urllib.request
import base64
import hashlib
import hmac

# Dict to map state to East or West
location = {"MI":"EAST", "IN":"EAST", "KY":"EAST", "TN":"EAST", "AL":"EAST", "OH":"EAST", 
            "GA":"EAST", "FL":"EAST", "SC":"EAST", "NC":"EAST", "VA":"EAST", "WV":"EAST", 
            "DE":"EAST", "MD":"EAST", "NJ":"EAST", "PA":"EAST", "NY":"EAST", "CT":"EAST", 
            "RI":"EAST", "MA":"EAST", "VT":"EAST", "NH":"EAST", "ME":"EAST", "LA":"EAST", 
            "WI":"EAST", "IL":"EAST", "MS":"EAST", "MN":"EAST", "IA":"EAST", "MO":"EAST", 
            "AR":"EAST", "CA":"WEST", "OR":"WEST", "WA":"WEST", "NV":"WEST", "ID":"WEST", 
            "UT":"WEST", "AZ":"WEST", "MT":"WEST", "AK":"WEST", "HW":"WEST", "WY":"WEST", 
            "CO":"WEST", "NM":"WEST", "ND":"WEST", "SD":"WEST", "NE":"WEST", "KS":"WEST", 
            "OK":"WEST", "TX":"WEST", "HI":"WEST"}

# Variables
central_info = creds.central_info
webhooktoken = creds.webhook
ssl_verify = True
central = ArubaCentralBase(central_info=central_info, ssl_verify=ssl_verify)
geoipurl = "http://ip-api.com/json/"

app = Flask(__name__)
#app.secret_key = 'S3cretK3y3'

# Validate message integrity
def verifyHeaderAuth(fullheaders, webhookData):
    # Token obtained from Aruba Central Webhooks page as provided in the input
    token = json.dumps((webhooktoken)["token"]).strip('"')
    token = token.encode('utf-8')

    # Capture data - needs cleanup
    data = webhookData.decode('utf-8')
    service = fullheaders['X-Central-Service']
    delivery =fullheaders['X-Central-Delivery-Id']
    timestamp = fullheaders['X-Central-Delivery-Timestamp']
    header = service+delivery+timestamp
    hash = fullheaders['X-Central-Signature']

    # Construct HMAC digest message
    sign_data = str(data) + str(header)
    sign_data = sign_data.encode('utf-8')

    # Find Message signature using HMAC algorithm and SHA256 digest mod
    dig = hmac.new(token, msg=sign_data, digestmod=hashlib.sha256).digest()
    signature = base64.b64encode(dig).decode()
    if hash == signature:
        return True
    return False

@app.route('/webhook', methods=['POST'])
def webhook():
    
    #Validate HMAC that is a valid webhook from Aruba Central
    webhookData = request.get_data()
    fullheaders = request.headers
    verified = verifyHeaderAuth(fullheaders, webhookData)
    
    if verified != True:
        abort(401)
    
    # Incoming webhook data from Central
    if request.method == 'POST':
        data = request.get_json()
        # Process new AP incoming webook - can add others in the future
        if (data['alert_type'] == 'New AP detected'):
            serial = (data['details']['serial'])
            print(serial)

            # Lookup public IP from AP serial      
            apdetails = central.command(apiMethod="GET", apiPath="/monitoring/v1/aps/" + serial)
            publicip = (apdetails['public_ip_address'])
            print(publicip)

            # GeoIP Lookup fitler to 2 letter state code
            req = urllib.request.Request(geoipurl + publicip)
            response = urllib.request.urlopen(req).read()
            json_response   = json.loads(response.decode('utf-8'))
            state = (json_response['region'])
            print(state)

            # Determine the group based on state
            region = location[state]
            print(region)
            if region == "WEST":
                centralgroup = "WEST-AP-GROUP"
            if region == "EAST":
                centralgroup = "EAST-AP-GROUP"
            else:
                centralgroup == "default"
            print(centralgroup)

            # Move AP into group based on State
            apmove = central.command(apiMethod="POST", apiPath="/configuration/v1/devices/move", 
                apiData = {"group": centralgroup, "serials": [serial]})
            
            print(apmove)
            return 'AP Sucessfully Provisioned', 200

        else:
            return 'Webhook Not Yet Supported', 405

    else:
        abort(400)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
