#!/usr/bin/env python
from os import system

def check_domain_availability(client):
    """
    Search for domain registration availability
    """
    domainName = input("Enter domain name: ")
    response = client.check_domain_availability(DomainName=domainName)
    print(response["Availability"])
    print("")
    input("Press Enter to continue")
    return
