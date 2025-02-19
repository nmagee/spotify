#!/bin/bash

aws s3 cp vsnfeqwr.json s3://$1-dp1-spotify/
aws s3 cp vsnfeqwr.mp3 s3://$1-dp1-spotify/
aws s3 cp vsnfeqwr.jpg s3://$1-dp1-spotify/
