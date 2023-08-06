#!/usr/bin/env python

import boto3
import os
import time
from os import system, path
from ec2 import describe_instances, start_instances, stop_instances
from route53 import check_domain_availability

# Set our default profile and region
session = boto3.Session(profile_name="default")
aws_region = "us-east-1"


class AWSProfile(object):
    """
    Method to change AWS profile and region.
    Multiple regions must be configured first in
    ~/.aws/{congig, credentails} files.
    """
    def __init__(self):
        global session
        global aws_region
        system("clear")
        data_folder = os.path.expanduser("~/.aws/")
        aws_file = os.path.join(data_folder, "config")
        aws_config = open(aws_file)
        print(aws_config.read())
        aws_profile = input("Type profile name: ")
        session = boto3.Session(profile_name=aws_profile)
        system("clear")
        print("Select region:")
        print("1. Cape Town (af-south-1)")
        print("2. London (eu-west-2)")
        choice = input("> ")
        if choice == "1":
            aws_region = "af-south-1"
        elif choice == "2":
            aws_region = "eu-west-2"
        else:
            print("Invalid option")
            time.sleep(2)
            aws_menu()
        aws_menu()
        


class EC2(object):
    """
    Menu options to manage EC2 methods imported
    from ec2.py
    Allows for listing, starting and stopping instances.
    """
    def __init__(self):
        self.client = session.client("ec2", region_name = aws_region)
    
    def ec2_menu(self):
        system("clear")
        print("AWS EC2")
        print(f"Profile: {session.profile_name} <> Region: {aws_region}")
        print("")
        print("1. List instances + status")
        print("2. Start instance")
        print("3. Stop instance")
        print("8. Back")
        print("9. Exit")
        choice = input("> ")
        if choice == "1":
            describe_instances(self.client)
            EC2.ec2_menu(self)
        elif choice == "2":
            start_instances(self.client)
            EC2.ec2_menu(self)
        elif choice == "3":
            stop_instances(self.client)
            EC2.ec2_menu(self)
        elif choice == "8":
            aws_menu()
        elif choice == "9":
            system("exit")
        else:
            print("Invalid option")
            time.sleep(2)
            EC2().ec2_menu()


class Route53(object):
    """
    Menu options to manage Route53 methods imported
    from route53.py
    Allows for searching domain registration availability.
    """
    def __init__(self):
        self.client = session.client("route53domains", region_name = "us-east-1")

    def route53_menu(self):
        system("clear")
        print("AWS Route53")
        print(f"Profile: {session.profile_name} <> Region: {aws_region}")
        print("")
        print("1. Domain Availability")
        print("8. Back")
        print("9. Exit")
        choice = input("> ")
        if choice == "1":
            check_domain_availability(self.client)
            Route53.route53_menu(self)
        elif choice == "8":
            aws_menu()
        elif choice == "9":
            system("exit")
        else:
            print("Invalid option")
            time.sleep(2)
            Route53().route53_menu()

    
def aws_menu():
    """
    Main menu.
    """
    system("clear")
    print("AWS CLI")
    print(f"Profile: {session.profile_name} <> Region: {aws_region}")
    print("")
    print("1. Change Profile & Region")
    print("2. Route53")
    print("3. EC2")
    print("9. Exit")
    choice = input("> ")
    if choice == "1":
        AWSProfile()
    elif choice == "2":
        Route53().route53_menu()
    elif choice == "3":
        EC2().ec2_menu()
    elif choice == "9":
        system("exit")
    else:
        print("Invalid option")
        time.sleep(2)
        aws_menu()



if __name__ == "__main__":
    aws_menu()