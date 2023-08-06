#!/usr/bin/env python
from os import system


def describe_instances(client):
    """
    List instances for AWS profile in chosen region.
    """
    response = client.describe_instances()
    for key in response["Reservations"]:
        for key1 in key["Instances"]:
            InstanceId = key1["InstanceId"]
            ImageId = key1["ImageId"]
            State = key1["State"]["Name"]
            try:
                for key2 in key["Instances"][0]["Tags"]:
                    Tags = key2["Value"]
            except:
                Tags = None

        print(Tags, InstanceId, State)
    print("")
    input("Press Enter to continue")
    return


def start_instances(client):
    """
    Start an AWS instance with instance ID.
    """
    print("Start an instance")
    instanceId = input("Enter instance ID: ")
    response = client.start_instances(InstanceIds=[instanceId])
    print(response)
    input("Press Enter to continue")
    return


def stop_instances(client):
    """
    Stop an AWS instance with instance ID.
    """
    print("Stop an instance")
    instanceId = input("Enter instance ID: ")
    response = client.stop_instances(InstanceIds=[instanceId])
    print(response)
    input("Press Enter to continue")
    return
