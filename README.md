# Dynatrace Activegate TLS/SSL certificate expiration check Plugin

This plugin checks the TLS/SSL certificates expiration date of URLs entered using the GUI and creates a problem if the certificate expiration days meet the threshold. Also, ingest the metric of the days remaining to be able to create custom charts and custom alerts if it's required.

![problem](https://github.com/yul14nrc/dynatrace_activegate_plugin_ssl_expiration_check/blob/master/images/problem.PNG)

![event](https://github.com/yul14nrc/dynatrace_activegate_plugin_ssl_expiration_check/blob/master/images/event.PNG)

![metrics](https://github.com/yul14nrc/dynatrace_activegate_plugin_ssl_expiration_check/blob/master/images/metrics.PNG)

## Requirements
This plugin requires the following:

* Dynatrace Environment ActiveGate v1.199.101 or newer.
* Sudo access to Dynatrace Environment ActiveGate Server.
* Access to settings in Dynatrace Tenant.

## Installation
ActiveGate Plugins need to get installed on the Environment ActiveGate Server that will execute it and in the Dynatrace Tenant using the UI. 

### Dynatrace Tenant
Upload the plugin's zip file to your Dynatrace tenant using the following path: **Settings** --> **Monitoring** --> **Monitored technologies** --> **Custom extensions** --> **Upload extension**

![settings_path](https://github.com/yul14nrc/dynatrace_activegate_plugin_ssl_expiration_check/blob/master/images/settings_path.PNG)

The Dynatrace tenant will check the plugin's zip content (it must contain the JSON and python files).

### Linux Environment ActiveGate Server
1. Copy the plugin's zip file in the Environment ActiveGate Server.
2. Unzip the plugin's zip file in **/opt/dynatrace/remotepluginmodule/plugin_deployment/** directory.
3. Restart the remote plugin service using **service remotepluginmodule restart**

## Plugin Configuration

To start the plugin configuration go to **Settings** --> **Monitoring** --> **Monitored technologies** --> **Custom extensions** and click in the plugin 

![extension_name](https://github.com/yul14nrc/dynatrace_activegate_plugin_ssl_expiration_check/blob/master/images/extension_name.PNG)

### Endpoint configuration tab

1. Click in **Add new endpoint** to configure a endpoint.
2. Complete the property fields:

![endpoint](https://github.com/yul14nrc/dynatrace_activegate_plugin_ssl_expiration_check/blob/master/images/endpoint.PNG)

* Endpoint name: The name of the endpoint.
* Frecuency: How often a certificate should be checked in minutes.
* Problem Alert Threshold: Threshold to raise a Problem before expiration in Days.
* Hosts: Comma seperated list of the Hosts certificates to monitor eg. www.dynatrace.com:443,www.google.com
* Choose ActiveGate: Windows or Linux Environment ActiveGate that the plugin is running on.

### Metrics tab
You can check the metrics sent by the plugin.

You can use this metrics to create Custom Charts and Custom Alerts if it's required.

![custom_chart](https://github.com/yul14nrc/dynatrace_activegate_plugin_ssl_expiration_check/blob/master/images/custom_chart.PNG)

### Changelog tab

Version history for the plugin.

## Troubleshooting

### Linux Environment ActiveGate
Check the Remote plugin logs in : /var/lib/dynatrace/remotepluginmodule/log/remoteplugin.

Also you will find a folder with the name of your extension eg. **custom.remote.python.ssl_cert_expiration_check**, inside you will find the log with the name of your main class **CertificatesCheckPlugin.log** that contains all the info that you are logging from python.

