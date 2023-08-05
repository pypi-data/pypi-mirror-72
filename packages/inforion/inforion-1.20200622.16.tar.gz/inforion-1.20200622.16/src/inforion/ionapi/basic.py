import requests
import base64
import sys
import os 
import json


from requests_oauthlib import OAuth2Session
from requests.auth import HTTPBasicAuth
from oauthlib.oauth2 import BackendApplicationClient


from inforion.helper.dynamic import url_change
from inforion.helper.urlsplit import spliturl

def load_config(IONFile):
    with open(IONFile) as json_file:
        data = json.load(json_file)
    return data 

    

def login(url,config):
    
    result = spliturl(url)

    #print (result)
    base_url = url_change(url) 
    #base_url = "https://mingle-sso.eu1.inforcloudsuite.com/"
   
    #base_url = base_url + "/" + result['Company']

        #'https://mingle-sso.eu1.inforcloudsuite.com:443/BVB_DEV'

    url = base_url + "/as/token.oauth2"
    

    data = {
                'grant_type' : 'password',
                'username' : config['saak'],
                'password' : config['sask'],
                'client_id' : config['ci'],
                'client_secret' : config['cs'],
                'scope' : '',
                'redirect_uri' : 'https://localhost/'
    }

    #print (data)
    r = requests.post(url, data=data)
    
    #print (r.status_code)
    #print ("TEST")
    #print (r.json())


    return r.json()






def header(config,token):
    '''
        headers = {
        'Content-Type': 'application/json',
        'X-TenantId': 'FELLOWCONSULTING_DEV',
        'X-ClientId': 'FELLOWCONSULTING_DEV~t1YYSUtR23J-h92WoUUQVPEOJQJZf7l5qjzZkbCrq8I',
        'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IkluZm9yQWNjZXNzVG9rZW5TaWduaW5nQ2VydGlmaWNhdGUtMTU3NjM2MzI3NyJ9.eyJzY29wZSI6Im51bGwiLCJjbGllbnRfaWQiOiJGRUxMT1dDT05TVUxUSU5HX0RFVn50MVlZU1V0UjIzSi1oOTJXb1VVUVZQRU9KUUpaZjdsNXFqelprYkNycThJIiwianRpIjoiM2NiYlVyVEx4ZERvbEFOUVM4aGs3MVlSRUpEd3UyWjBzZ3dxIiwiU2VydmljZUFjY291bnQiOiJGRUxMT1dDT05TVUxUSU5HX0RFViN4dGQ3QVZjeGFSVXlnQkRxVXBLdkJab0dXd08wZ2NHZ0U5UTNDaHdnSlREZ1VXUWNHZ2ptZjBGd1poZW9wSHI1ZmZrUVBmejFBOHZLYjExTEh0QkstdyIsIklkZW50aXR5MiI6IjQ2YjYwMmE0LWIxNTgtNGQ2My05YjJlLTZiMjJkYmEwNjU0YyIsIlRlbmFudCI6IkZFTExPV0NPTlNVTFRJTkdfREVWIiwiRW5mb3JjZVNjb3Blc0ZvckNsaWVudCI6IjAiLCJleHAiOjE1ODIyMTM3MjB9.FMBtAWQVh-S81kEDRjZnN3rujAGyX0UIj5SKLvEhlTLOu0jT92JRB5VuHKRHtKg-ODcDgSMd2i1YMcALFcQvxiTRyvo3oW3m5GAaELv_TUWcr7r-Qd952WIQUAtfTY66CUclWYIkHa3HuEF2t9m7Doglw88RakcqHAK8-SnONJTF9UreVD6ZO3sVFu7UDB5DKOr6iwfZPFJtTJGaiTpLydXqTto6vGaZ3csC0zx6IfPqSKQg7yfz9u1I_mJbdG6PnmrksBVWkCF6lG30ibdM2jCjhELuzWlXHjTD47n4K84O9OvuylYG2wuT8DDHlL255oOLzFkySdqtMAbdXKveyQ',
        'User-Agent': 'PostmanRuntime/7.22.0',
        'Accept': '*/*',
        'Cache-Control': 'no-cache',
        'Postman-Token': '5ebf61ab-bb78-4b14-9161-bf5ee714c210',
        'Host': 'mingle-ionapi.eu1.inforcloudsuite.com',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Length': '359',
        'Cookie': 'useractivity_cookie_mingle=1582207527',
        'Connection': 'keep-alive'
        }
    '''

    headers = {
        'Content-Type':         'application/json',
        'X-TenantId':           config['ti'],
        'Connection':           'keep-alive',
        'Host':                 'mingle-ionapi.eu1.inforcloudsuite.com',
        'Accept-Encoding':      'gzip, deflate, br',
        'Cache-Control':        'no-cache',
        'User-Agent':           'FellowConsultingAGRuntime/7.22.0',
        'X-ClientId':           config['ci'],
        'Accept':               '*/*',
        'Authorization':        'Bearer ' +token['access_token'],

    }
    return headers