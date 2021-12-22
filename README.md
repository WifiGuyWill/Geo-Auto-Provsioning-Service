# Location Based Provisioning Service for Aruba Central
A service to auto provision devices in Aruba Central based on the Geo-IP location

![GAPS](https://github.com/WifiGuyWill/Geo-Auto-Provsioning-Service/blob/GAPS-Container/img/GAPS.jpg?raw=true "GAPS")

Geo-IP auto provisioning service (GAPS) will auto assign any new AP to a group in Central based on the location of the device.

# How it works:

* New AP is plugged in and automatically connects to Aruba Central. 
* Central via webhook posts a message to GAPS which then does a REST API call to central for AP details. 
* The details are parsed for the public IP. GAPS makes an API call to a public GEO IP service which return the physical location of the installed AP. 
* The location data parsed for the two letter state. This is checked against a local dictionary that maps the state to a location (IE East / West). 
* Based on the location, a group is selected and GAPS sends Central the AP provisioning command with the proper group.

# First Steps:

* Log into Aruba Central from the Account Home page:
  * API Gateway > System Apps & Tokens > Create a new key
  * Webhooks > Click the + sign > Enter the URL where the GAPS service will be posted "https://<gaps-url>/webhook
* Launch the Network Dashboard:
   * Global > Alerts & Events > Config
   * Under Access Point > Enable AP Detect > Select the Webhook for GAPS

# Install instructions:

  1. Copy the files to host
  2. Open location_mapping.py
     * Match the two letter state code to the Central Group  
     * Add a Group for the default for any Geo-IP locations that don't match 
  4. Open dockerfile and add the Aruba Central Credentials

    > ENV USERNAME=xxxxxxxxxx@email.com
    > ENV PASSWORD=xxxxxxxxxx
    > ENV CLIENT_ID=xxxxxxxxxx
    > ENV CLIENT_SECRET=xxxxxxxxxx
    > ENV CUSTOMER_ID=xxxxxxxxxx
    > ENV BASE_URL=https://apigw-prod2.central.arubanetworks.com
    > ENV WEBHOOK_TOKEN=xxxxxxxxxx
  4. Create the container "docker build -t gaps:latest ."
  5. Start the container "docker run -p 5000:5000 gaps"
  
- - - -

This container includes gunicorn web-server, modify the wsgi config as needed.


Question - Feel free to contact me:   
#(c) 2021 Will Smith - WILL@WIFI-GUYS.COM
