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

# Install instructions
* Copy the files to host
* Open dockerfile and add the Aruba Central Credentials

  > ENV USERNAME=xxxxxxxxxx@email.com
  > 
  > ENV PASSWORD=xxxxxxxxxx
  > 
  > ENV CLIENT_ID=xxxxxxxxxx
  > 
  > ENV CLIENT_SECRET=xxxxxxxxxx
  > 
  > ENV CUSTOMER_ID=xxxxxxxxxx
  > 
  > ENV BASE_URL=https://apigw-prod2.central.arubanetworks.com
  > 
  > ENV WEBHOOK_TOKEN=xxxxxxxxxx

* Create the container "docker build -t gaps:latest ."
* Start the container "docker run -p 5000:5000 gaps"

This container includes gunicorn web-server
Modify the wsgi config as needed


Question - Feel free to contact me:   
#(c) 2021 Will Smith - WILL@WIFI-GUYS.COM
