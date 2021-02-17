# Dynatrace Activegate TLS/SSL certificate expiration check Plugin

This plugin checks the TLS/SSL certificates expiration date of URLs entered using the GUI and creates a problem if the certificate expiration days meet the threshold. Also, ingest the metric of the days remaining to be able to create custom charts and custom alerts if it's required.

![problem](/images/problem.png)

imagen evento

imagen metricas

## Requirements
This plugin requires the following:

* Dynatrace Environment ActiveGate v1.199.101 or newer
* Sudo access to Dynatrace Environment ActiveGate Server
* Access to settings in Dynatrace Tenant

## Installation
ActiveGate Plugins need to get installed on the Environment ActiveGate Server that will execute it and in the Dynatrace Server using the UI. 




 ### Dynatrace Tenant
Upload the plugin to your Dynatrace tenant using the GUI: Settings --> Custom Extensions --> Upload extensions
 Complete the property fields:

 ![SSLCert](/images/plugin_conf.png)
 
 Complete the following fields:
 * Endpoint name: The name of the active gate endpoint
 * Poll Interval: How often a certificate should be checked in minutes
 * Custom Event Period Threshold: Threshold to raise a custom event before expiration in Days
 * Problem Alert Period Threshold: Threshold to raise a Problem event before expiration in Days*Hosts: Comma seperated list of the Host certificates to monitor eg. www.google.com443,www.example.com:443
 * Choose ActiveGate: The Windows or Linux Active Gate that the plugin is running on.

 ### Linux Environment ActiveGate Server
 1. Copy the plugin's zip file in the Environment ActiveGate Server.
 2. Unzip the plugin's zip file in **/opt/dynatrace/remotepluginmodule/plugin_deployment/** directory.
 3. Restart the remote plugin service using **service remotepluginmodule restart**
 
## Troubleshooting

### Linux Environment ActiveGate
Check the Remote plugin logs in : /var/lib/dynatrace/remotepluginmodule/log/remoteplugin

Also you will find a folder with the name of your extension eg. **custom.remote.python.ssl_cert_expiration_check**, inside you will find the log with the name of your main class **CertificatesCheckPlugin.log** that contains all the info that you are logging from python.

