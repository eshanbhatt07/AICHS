#import necessary packages
from flask import Flask, request
from twilio import twiml
from twilio.twiml.messaging_response import Message, MessagingResponse
import numpy as np
import pandas as pd
import numpy as np
import predict_function

import http.client, urllib.request, urllib.parse, urllib.error
import json
from pymongo import MongoClient
import datetime
from bson.binary import Binary
import _pickle as pickle
import random

import codecs
from elasticsearch import Elasticsearch
import time

from summa.summarizer import summarize

mapping = {
"my-map-consumer": {
"properties": {
"Complaint": {"type": "keyword"},
"Number": {"type": "keyword"},
"Summa": {"type": "keyword"},
"Customer_Score": {"type":"integer"},
"timestamp": {"type":"date"},
"Category": {"type":"keyword"},
"Status": {"type":"keyword"},
"Age": {"type": "integer"},
"Salary": {"type": "integer"},
"CS": {"type": "integer"}
}
}
}


from elasticsearch import Elasticsearch, helpers
from elasticsearch import helpers








text = 'I have attempted to get a loan modification from GMAC, nka OCWEN for 4 years. I have sent in XXXX modification packages with over XXXX documents in each one with delivery confirmation, have mailed the documents using delivery confirmation, have faxed them in and have emailed them. Every time they start to process, something is missing on their end. In total, I have faxed over XXXX pages of documents trying to facilitate their processing. Now the servicing agent, OCWEN, has started a foreclosure action, even though there is a modification package on file that is, again, in process. I thought GMAC scammed us all but the real scammer here is OCWEN. They now claim I owe {$74000.00} more than my original amount owed due to late fees, interest, penalties, real estate taxes and home owner '+'s insurance. I owe more since they have nothing but give me the run around about needing more and more documents. All in an effort to make more money.'
app = Flask(__name__)
#extract the optimal customer data for the bank to evaluate current consumer score
retention_data = pd.read_csv("/Users/nuexb14/Desktop/Personal/UNCC/x2.csv")


client = MongoClient('mongodb://localhost:27017')

db = client['hackathon']

complaints = db.complaints



addresses = retention_data['Address']
addresses = list(addresses)

global customer_score
status = ['Resolved', 'In Process'] 
#Pushing Coupons based on complaint category
complaint_cat = ['Mortgage','Credit reporting', 'Debt collection']




global counter
counter = 1

#API Route to scrap SMS data
@app.route('/sms', methods=['POST'])
def sms():
    

    number = request.form['From']
    number = number[2:]
    text = request.form['Body']
#    print(number)
#    print(type(number))

    
    if 'Status' in text:
        complaint_no = int(text[7:])
        print(complaint_no)
        my_status = complaints.find_one({"ticket":complaint_no})
        my_status = my_status['status']['timestamp']['currStatus']
        print(my_status)
        
        message_body = 'Hello {}, Thank you for contacting Data Spartans Inc. The Status of complaint number {} is {}'.format(number, complaint_no, my_status)
        resp = MessagingResponse()
        resp.message(message_body)
        print("True in Status")
        
        
    else:

        print("False")
        es = Elasticsearch('http://localhost:9200/')
        if not es.indices.exists("fintech-hackathon-consumer13"):
            es.indices.create("fintech-hackathon-consumer13")
    
        es.indices.put_mapping(index="fintech-hackathon-consumer13",doc_type="my-map-consumer",body=mapping)
        summary = summarize(text, ratio=0.8)

        
        
        json_data ={}
        
        #Storing text as document in mongoDB
        
        
        
                    
        #Calling predict_sample() to classify the category of the  complaint
        category = predict_function.predict_sample(text)
        
        
        my_score = list()
        
        address = retention_data.loc[retention_data['PhoneNumber'] == int(number)]

        address = address['Address']
        
        address = address.iloc[0]
#        x = retention_data.loc[retention_data['PhoneNumber'] == number, 'Address']
#        print(type(x))
#        print(address)
#        print(len(address))
#        
        if address in addresses:
            subset_data = retention_data.loc[retention_data['Address']==address]
            #Calculating mean values if multiple occurences exists of the same address
            u_bal = int(np.mean(subset_data['Balance']))
            u_sal = int(np.mean(subset_data['EstimatedSalary']))
            u_age= int(np.mean(subset_data['Age']))
            u_noprods = int(np.mean(subset_data['NumOfProducts']))
            u_cs= int(np.mean(subset_data['CreditScore']))
            
            print(u_sal)
            print(u_age)
            print(u_sal)
            
            
            
            #Calculating values based on single occurence of address. 
            bal,sal,age,noprods,cs = retention_data['Balance'][0],retention_data['EstimatedSalary'][0],retention_data['Age'][0],retention_data['NumOfProducts'][0],retention_data['CreditScore'][0]
        else:
            print("Nothing")
    
        #Calculating customer scores based on top features
        if(u_age >37 or age > 37):
            my_score.append(2)
        else:
            my_score.append(-2)
            
        if(u_sal > 99000 or sal > 99000):
            my_score.append(1.5)
        else:
            my_score.append(-1.5)
            
        if(u_cs > 650 or cs > 650):
            my_score.append(1)
        else:
            my_score.append(-1)
        
        if(u_bal > 72000 or bal > 72000):
            my_score.append(0.5)
        else:
            my_score.append(-0.5)
        
        if(u_noprods > 1) or noprods > 1:
            my_score.append(0.2)
        else:
            my_score.append(-0.2)
            
        #Using mean value as the threshold, to evaluate the category of the customer.
        if(sum(my_score) >= 5.2):
            print(my_score)
            index_comp = complaint_cat.index(category)
            
            print("Coupon")
            print(text)
            
        else:
            message_body = "Sorry for the incovenience. We have forwarded your complaint to the suppport staff"
            print("Invalid")
            print(my_score)
        
        json_data['custNumber'] = number
        ticket_no = random.randint(1000,1000000)
        json_data['ticket'] = ticket_no
        json_data['complaintData'] = text
        json_data['category'] = category
        json_data['customer_score'] = sum(my_score)
        
        
        
        json_status = status[random.randint(0,1)]
        json_data['status'] = {'timestamp': {'currTime': datetime.datetime.now(), 'currStatus': json_status}}
        
    
        result_complaint = complaints.insert_one(json_data)
        
        content = {
                "Complaint": json_data['complaintData'],
                "Number": json_data['custNumber'],
                "Summa": summary,
                "Customer_Score":json_data['customer_score'],
                "timestamp": datetime.datetime.now(),
                "Category": category,
                "Status": json_status,
                "Age": u_age,
                "Salary": u_sal,
                "CS": u_cs
                
                }
        
        es.index(index="fintech-hackathon-consumer13",doc_type="my-map-consumer",body=content)
        del u_age, u_bal, u_cs
        json_data.clear()
    
        
        resp = MessagingResponse()
        #replyText = getReply(message_body)
        message_body = 'Hello {}. Sorry for the inconvenience caused. We have forwarded your complaint to the Support Staff of {} Department. We have also generated a ticket for your complaint and the ticket number is {}. You can always check the status of your complaint by sending a message ; Status <ticket number> on +17048793234'.format(number,category,ticket_no)
        
        resp.message(message_body)
    return str(resp)

if __name__ == '__main__':
    app.run()
    
    
    
#text1 = 'I have been divorced since XX/XX/2007 and it appears on my credit report that my ex husband is my spouse or my co-applicant. I have attach my divorce decree.'
#predict_function.predict_sample(text)