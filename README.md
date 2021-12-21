# Geo-IP Auto Provsioning Service for Aruba Central
A service to auto provison devices in Aruba Central based on the Geo-IP location

![GAPS](https://github.com/WifiGuyWill/Geo-Auto-Provsioning-Service/blob/main/GAPS.jpg?raw=true "GAPS")

Geo-IP auto provisioning service (GAPS) will auto assign any new AP to a group in Central based on the location of the device.

#How it works:

* New AP is added into Aruba Central. 
* Central via webhook posts a message to GAPS which then does a REST API call to central for AP details. 
* The details are parsed for the public IP. GAPS makes an API call to a public GEO IP service which return the physical location of the installed AP. 
* The location data parsed for the two letter state. This is checked against a local dictionary that maps the state to a location (IE East / West). 
* Based on the location, a group is selected and GAPS sends Central the AP provisioning command with the proper group.
