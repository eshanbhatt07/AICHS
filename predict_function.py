# -*- coding: utf-8 -*-
"""
Created on Sat Oct 20 00:31:04 2018

@author: dhwan
"""
# These reviews are now correctly identified
import nltk
nltk.download('punkt')
from nltk import word_tokenize
import re
from nltk.tokenize import word_tokenize 
from nltk.corpus import stopwords 
from sklearn.feature_extraction.text import CountVectorizer
import  pickle


def predict_sample(text):
    text = str(text)
    print(text)
    
    vect = pickle.load( open( "vectorizer.pk", "rb" ) )   
    model = pickle.load( open( "model.sav", "rb" ) ) 
    pattern = re.compile("xx*")
    nums = re.compile('[0-9]')
    porter = nltk.PorterStemmer()
    stop_words = set(stopwords.words('english')) 
    stop_words = list(stop_words)
    ss = ['.',',','!','?',':','+','-','(',')',':',';','1','2','3','4','5','6','7','8','9','{','}','#','$','%','&','*','=','[',']','1.','2.','3.','4.','5.','6.','7.','8.','9.','0','0.']
    for i in ss:
        stop_words.append(i)
    try:
        comp_str = ''
        narrative = word_tokenize(text.lower())
    #     filtered_sentence = []
        for w in narrative:
            if len(w) >= 3:
                if pattern.match(w) or nums.match(w) :
                    continue

                if w not in stop_words:
                    stemmed = porter.stem(w)
                    comp_str += stemmed + ' '
    #                 filtered_sentence.append(stemmed)
        print(model.predict(vect.transform([comp_str]))[0])

        return model.predict(vect.transform([comp_str]))[0]
        
    except:
        
        return 'Credit reporting'


text = 'I have attempted to get a loan modification from GMAC, nka OCWEN for 4 years. I have sent in XXXX modification packages with over XXXX documents in each one with delivery confirmation, have mailed the documents using delivery confirmation, have faxed them in and have emailed them. Every time they start to process, something is missing on their end. In total, I have faxed over XXXX pages of documents trying to facilitate their processing. Now the servicing agent, OCWEN, has started a foreclosure action, even though there is a modification package on file that is, again, in process. I thought GMAC scammed us all but the real scammer here is OCWEN. They now claim I owe {$74000.00} more than my original amount owed due to late fees, interest, penalties, real estate taxes and home owner '+'s insurance. I owe more since they have nothing but give me the run around about needing more and more documents. All in an effort to make more money.'

