#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  2 13:03:27 2018

@author: nuexb14
"""

from flask import Flask, request
from twilio import twiml
from twilio.twiml.messaging_response import Message, MessagingResponse
import numpy as np
import pandas as pd
import numpy as np


import http.client, urllib.request, urllib.parse, urllib.error
import json
from pymongo import MongoClient
import datetime
from bson.binary import Binary
import _pickle as pickle
import random



from elasticsearch import Elasticsearch, helpers

app = Flask(__name__)
"""on db.collection.update() send a text message to number extracted from the document
whose status is change and send a message to that number. 
"""


client = MongoClient('mongodb://localhost:27017')

db = client['hackathon']

complaints = db.complaints
new_status = 'Resolved'
ticket = 161191
complaints.find_one_and_update({"ticket": ticket}, 
                               {"$set": 
                                   {"status":
                                       {"timestamp": 
                                           {"currTime":datetime.datetime.now(),
                                            "currStatus": new_status}
                                           }
                                           }
                                           }
                                           )
    

message_body = 'Hello Customer. We are again sorry for the trouble caused. We are letting you inform that the status of your complaint ticket number: {} , has been changed to {}'.format(ticket,new_status )




from twilio.rest import Client


# Your Account Sid and Auth Token from twilio.com/console
account_sid = 'ACda40687eebfdfdb7110019ca2a38d95b'
auth_token = 'b3ae4e14ec9028aea588be0f1a55d82c'
client = Client(account_sid, auth_token)

message = client.messages \
                .create(
                     body=message_body,
                     from_='+17048793234',
                     to='+19803659169'
                 )

print(message.sid)




