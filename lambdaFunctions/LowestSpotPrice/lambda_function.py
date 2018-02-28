# lowestSpotPrice.py - Returns the region with the lowest spot price for a selected instance type

import boto3
import json
from datetime import datetime

listOfSpotPrices= {}
sortedListOfSpotPrices= ()

#Main function called
def lambda_handler(event, context):
    listPrices()
    sortSpotPrices()

    respBodyString = ("Lowest Spot Price for instance type: <strong> i3.large </strong> </br> Availability Zone: <strong>" + sortedListOfSpotPrices[0][0] + "</strong> Price per hour: <strong>$"
        + sortedListOfSpotPrices[0][1] + "</strong></br>" + " Complete list of Availability Zone spot prices for instance type: i3.large </br>")

    for i in sortedListOfSpotPrices:
        respBodyString += (i[0] + " per hour: $" + i[1] + "</br>")

    resp = {
      "statusCode": 200,
       "headers": {
       "Access-Control-Allow-Origin": "*",
        },
        "body" : respBodyString
    }

    return resp


# Iterate through each region and get spot price
def listPrices():
    regionClient = boto3.client('ec2')

    for region in regionClient.describe_regions()['Regions']:
        client = boto3.client('ec2',region_name=region['RegionName'])
        prices=client.describe_spot_price_history(
            EndTime=datetime.now(),
            InstanceTypes=['i3.large'],
            ProductDescriptions=['Linux/UNIX (Amazon VPC)'],
            StartTime=datetime.now()
            )

        az = str((prices['SpotPriceHistory'][0]['AvailabilityZone']))
        spotPrice = str((prices['SpotPriceHistory'][0]['SpotPrice']))

        listOfSpotPrices[az]=spotPrice

# Sort spot prices in ascending order by price
def sortSpotPrices():
    global sortedListOfSpotPrices

    # Converts the dict listOfSpotPrices into a sorted tuple
    sortedListOfSpotPrices = sorted(listOfSpotPrices.items(), key=lambda x:x[1])
