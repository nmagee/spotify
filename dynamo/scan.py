#!/usr/bin/env python3

import boto3
import os


ddb = boto3.client('dynamodb')
table = "songs"

response = ddb.scan(
    TableName='songs',
#    IndexName='string',
    Select='ALL_ATTRIBUTES'
)

print(response['Items'])
