#import sqlite3
#import socket
#import urllib.request, urllib.parse, urllib.error
import json
import requests
import base64
import datetime

out_filename = 'counter.json'
out_json = {}
token = ""

def get_token():
    apiKey = "627n3iclwzi6fopdplmxtvx33hmm97lq"
    secret = "WDWFpGihFaYO"
    message = apiKey + ':' + secret
    auth = "Basic " + base64.b64encode(message.encode("ascii")).decode("ascii")
  
    headers_dic = {"Authorization":auth,
                   "Content-Type" : "application/x-www-form-urlencoded;charset=UTF-8"}
    params_dic = {"grant_type" : "client_credentials",
                  "scope" : "read"}
    
    r = requests.post("https://api.idealista.com/oauth/token",
                      headers = headers_dic,
                      params = params_dic)
    bearer_token = json.loads(r.text)['access_token']
    print('Response text: ',r.text)
    print('Json Load: ',json.loads(r.text))
    return bearer_token

def get_resquest():
    '''
    method = "POST"
    url = "https://api.idealista.com/3.5/es/search"

    session = requests.session()
    response = session.request(method=method, url=url, auth=auth, client_secret=secret)

    data = json.load(response.content)
    print(data)
    '''
    return 0

def inc_counter():
    #increment the counter inside the file
    #this must save in every iteration of this code
    #json.
    return True
    
def check_limit():
    #first checks how long was the first call
    # if it was a month ago, se new time to now and reset timer
    # else, output the amount of time the API has been requested
    #   if it has been request more than 100 times don't let the code run further

    return 0

def init_json():
    ficheiro = open(out_filename, 'r')
    if ficheiro.read() == '':
        with open(out_filename, 'w') as f:
            json.dump({
            'first_entry':'',
            'last_entry':'',
            'counter':0
        }, f, indent=1)
        ficheiro = open(out_filename, 'r')
    print(ficheiro.read() == '')
    return '' #json.load(ficheiro)

def run():
    out_json = init_json()
    if check_limit() >= 35:
        raise Exception('Enough criminal scum, you violated the law!')
    #token = get_token()
    else:
        print(out_json)

    print(token)
