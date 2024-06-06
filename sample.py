#!/usr/bin/python3

import requests
import subprocess

data = requests.get("https://datarepo.eng.ucsd.edu/mcauley_group/data/amazon_2023/raw/review_categories/Magazine_Subscriptions.jsonl.gz")

with open("Magazine_Subscriptionsjsonlgz.zip", 'wb') as file:
    file.write(data.content)
    print("File Downloaded successfully")

