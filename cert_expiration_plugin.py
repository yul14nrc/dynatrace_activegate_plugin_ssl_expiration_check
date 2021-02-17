import json, click
import requests
from ruxit.api.base_plugin import RemoteBasePlugin
import logging
import check_tls_certificate
import datetime 
from datetime import datetime as timedelta
import os
from ruxit.api.data import StatCounterDataPoint
import itertools

logger = logging.getLogger(__name__)

class CertificatesCheckPlugin(RemoteBasePlugin):

    def initialize(self, **kwargs):
        config = kwargs['config']
        logger.info("Config: %s", config)
        self.path = os.getcwd()
        self.poll_period = config["poll_interval"]
        #self.period = config["period"]
        self.alert_period = config["alert_period"]
        #self.event_type = config["event_type"]
        self.hosts = config["hosts"].split(",")
        #self.default_expiry_warn = self.period
        self.default_expiry_err = self.alert_period
        
        self.alert_iterations = 0
        self.event_iterations = 0
        self.absolute_iterations = 1
        self.initial_iteration = True
        
        self.current_entries = 1
        self.archived_entries = 0

        self.domains = None

    def query(self, **kwargs):
        # Create group - provide group id used to calculate unique entity id in dynatrace
        #   and display name for UI presentation

        if self.absolute_iterations==1 and self.initial_iteration == True:
            self.poll_hosts()

        if self.should_poll_cert():
            self.poll_hosts()
        else:
            logger.info("Hosts not being polled: current=%s <= frecuency=%s",self.absolute_iterations - 1,self.poll_period)

        for domainnames, msgs, expiration in self.checked_domains:
            if expiration:
                print("expiration: " + str(expiration))
                if self.earliest_expiration is None or expiration < self.earliest_expiration:
                   self.earliest_expiration = expiration
            warnings = 0
            errors = 0
            domain_msgs = [', '.join(domainnames)]
            for level, msg in msgs:
                if level == 'error':
                   color = 'red'
                   errors = errors + 1
                elif level == 'warning':
                   color = 'yellow'
                   warnings = warnings + 1
                else:
                   color = None
                if color:
                   msg = click.style(msg, fg=color)
                msg = "\n".join("    " + m for m in msg.split('\n'))
                domain_msgs.append(msg)
       
            if warnings or errors:
               click.echo('\n'.join(domain_msgs))

            self.total_errors = self.total_errors + errors
            msg = "%s error(s)" % (self.total_errors)
   
            if self.earliest_expiration:
               msg += "\nEarliest expiration on %s (%s)." % (
               self.earliest_expiration, self.earliest_expiration - self.utcnow)
            if len(self.exceptions) > (len(self.domain_certs.values()) / 2):
              click.echo(click.style(msg, fg="red"))
         
        if self.total_errors:
            click.echo(click.style(msg, fg="red"))
          
        #elif self.total_warnings:
        #    click.echo(click.style(msg, fg="yellow"))    
        
        group = self.topology_builder.create_group(identifier="CertGroup",
                                                   group_name="SSL/TLS Certificates Expiration Group")

        # Create device - provide device id used to calculate unique entity id in dynatrace
        #   and display name for UI presentation
        #device = group.create_device(identifier="SSLDevice",
        #                            display_name="SSL Device")

        def days_between(d2):
            #d1 = datetime.strptime(d1, "%Y-%m-%d")
            d1 = datetime.datetime.utcnow().date()
            d2 = datetime.datetime.strptime(d2, '%Y-%m-%d %H:%M:%S').date()
            return str(abs((d2 - d1).days))  
        

        # Push infrastructure info events and problems
        
        for domainnames, msgs, expiration in self.checked_domains:
            if expiration:
                print("expiration: " + str(expiration))
                if self.earliest_expiration is None or expiration < self.earliest_expiration:
                   self.earliest_expiration = expiration
            warnings = 0
            errors = 0
            domain_msgs = [', '.join(domainnames)]
            print("domainnames: ", domainnames)
            
            if (self.absolute_iterations ==1 and self.initial_iteration ==False):
                days = days_between(str(expiration))
                device = group.create_device(identifier=domainnames[0],
                                        display_name=domainnames[0])

                if int(days) > int(self.default_expiry_err):
                    logger.info("Logging for Domain: %s, Info: The certificate expires on %s, %s days", domainnames, expiration, days)
                    logger.info("Logging Topology: group name=%s, node name=%s", group.name, device.name)
                    #device.state_metric("certificate_state", "ExpirationOk")
                    device.absolute("certificate_days_remaining", days)
                
                if int(days) <= int(self.default_expiry_err):
                    logger.info("Logging Problem Alert for Domain: %s, Error: The certificate expires on %s, %s days", domainnames, expiration, days)
                    logger.info("Logging Topology: group name=%s, node name=%s", group.name, device.name)
                    #device.state_metric("certificate_state", "ExpirationSoon")
                    device.absolute("certificate_days_remaining", days)
                    device.report_error_event(title="SSL/TLS certificate expiration within the alert threshold set: " + str(self.default_expiry_err) + " days",
                                description="The SSL/TLS cerficate will expire in: "+ days +" days",
                                properties={"Certificate expiration date": str(expiration), "Certificate expiration days remaining": str(days)})

            else:
                self.initial_iteration = True
                logger.info("Skipping certificate check to prevent spam: %s",self.absolute_iterations - 1)
    
    def poll_hosts(self):
        if (self.hosts is not None):
            logger.info("Checking certificates expiration...")
            self.domains = list(check_tls_certificate.itertools.chain(
                check_tls_certificate.domain_definitions_from_cli(self.hosts)))
        else:
            logger.error("Host URL invalid: verify the host URL in the dynatrace UI")
            #self.domains = list(check_tls_certificate.itertools.chain(
                #check_tls_certificate.domain_definitions_from_filename(self.path + "/hosts.txt")))
        
        self.domain_certs = check_tls_certificate.get_domain_certs(self.domains)
        self.exceptions = list(x for x in self.domain_certs.values() if isinstance(x, Exception))
        #self.total_warnings = 0
        self.total_errors = 0
        self.earliest_expiration = None
        self.utcnow = datetime.datetime.utcnow()
        self.checked_domains = check_tls_certificate.check_domains(self.domains, self.domain_certs, self.utcnow, expiry_err=self.default_expiry_err)
           
        print("Checked Domains:", self.checked_domains)
    
    def should_poll_cert(self):
        
        if (self.absolute_iterations >= self.poll_period):
            self.absolute_iterations = 1
            self.initial_iteration = False
            return True

        self.absolute_iterations = self.absolute_iterations + 1

        return False

        #self.absolute_iterations = self.absolute_iterations + 1
        
        #if (self.absolute_iterations > self.poll_period):
        #    self.absolute_iterations = 0
        #    return True

        #if self.absolute_iterations ==1:
        #     return True   

        #return False 
