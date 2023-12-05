import json
import requests
import base64
import datetime
import re
from dateutil.relativedelta import relativedelta

max_limit = 40
cont_filename = 'request_cont.json'
api_response_filename = 'api_out.json'
out_json = {
            'first_entry': '',
            'last_entry': '',
            'counter': 0
        }

def get_keys():
    apikey = ''
    secret = ''
    api_auth_f = 'api_auth.json'
    auth_json = read_file(api_auth_f)
    #print('Auth json output:',auth_json)
    apikey = auth_json['apikey']
    secret = auth_json['secret']
    return apikey, secret

def get_token():
    apiKey, secret = get_keys()
    
    message = apiKey + ':' + secret
    #print('Message not encoded',message)
    auth = "Basic " + base64.b64encode(message.encode("ascii")).decode("ascii")
    #print('Encoded auth:',auth)
    headers_dic = {"Authorization":auth,
                   "Content-Type" : "application/x-www-form-urlencoded;charset=UTF-8"}
    params_dic = {"grant_type" : "client_credentials",
                  "scope" : "read"}
    
    r = requests.post("https://api.idealista.com/oauth/token",
                      headers = headers_dic,
                      params = params_dic)
    bearer_token = json.loads(r.text)['access_token']
    #print('Response text: ',r.text)
    #print('Json Load: ',json.loads(r.text))
    return bearer_token

def get_request():

    #curl -X POST -H "Authorization: Bearer {{OAUTH_BEARER}}" -H "Content-Type: multipart/form-data;" 
    #-F "center=40.430,-3.702" -F "propertyType=homes" -F "distance=15000" -F "operation=sale"

    #https://api.idealista.com/3/es/search?locale=es&maxItems=20&numPage=1&operation=sale
    # &order=publicationDate&propertyType=garages&sort=desc
    # &apikey={api_key}&t=1&language=es&bankOffer=true&locationId=0-EU-ES-28
    success = bool
    token = get_token()
    apiKey, secret = get_keys()

    url = "https://api.idealista.com/3.5/pt/search"
    data = {'locale':'pt',
            'propertyType':'homes',
            'sort':'desc',
            'order':'publicationDate',
            'operation':'sale',
            'apikey':apiKey,
            'language':'pt',
            't':'1',
            'center':'38.72197742266314,-9.139480518540617',
            'distance':20000}
    
    #session = requests.session()
    headers = {'Authorization': 'Bearer '+token
        }
    print('token:'+headers['Authorization'])
    
    #response = session.request(method=method, url=url, headers=headers, data=data, auth=auth, client_secret=secret)

    response = requests.post(url=url, headers=headers, data=data)
    data = json.loads(response.text) #response.content
    save_to_file(api_response_filename, data) 
    if response.status_code == 200:
        success = True
    else:
        success = False
    print(data)
    return success 

def inc_counter():
    #increment the counter inside the file
    #this must save in every iteration of this code
    out_json = read_file(cont_filename)
    out_json['last_entry'] = get_cur_date_str()
    out_json['counter'] += 1
    save_to_file(cont_filename, out_json)
    
def check_limit():
    #first checks how long was the first call
    out_json = read_file(cont_filename)

    if a_month_ago(out_json['first_entry']):
        #if it was a month ago, then set the first entry date to the current time and reset the counter
        curr_datetime = get_cur_date_str()
        out_json['first_entry'] = curr_datetime #set to current time
        out_json['counter'] = 0 #reset timer
        save_to_file(cont_filename, out_json)
        
    return out_json['counter']

def next_call():
    out_json = read_file(cont_filename)
    delta = relativedelta(datetime.datetime.now(), out_json['last_entry'].strftime('%d/%m/%Y %H:%M'))
    hours_difference = int(delta.hours)
    if hours_difference > 12:
        return True
    else:
        return False
    
def a_month_ago(date_text):
    #Returns true if the time between the first call and the current time is equal to at least one month
    #meaning, if it's at least one month, then we can reassign the first entry to the current date
    
    #print('Entry:',date_text)
    cur_datetime = datetime.datetime.now()
    
    date_txt_f = re.search(r'\d{2}/\d{2}/\d{4}',date_text).group(0)
    date_obj = datetime.datetime.strptime(date_txt_f, "%d/%m/%Y")
    delta = relativedelta(cur_datetime, date_obj)
    months_difference = int(delta.months)
    
    return months_difference >= 1

def get_cur_date_str():

    return datetime.datetime.now().strftime("%d/%m/%Y %H:%M")

def init_json():

    out_json = read_file(cont_filename)
    
    if out_json == '':
        
        out_json = {
            'first_entry':'',
            'last_entry':'',
            'counter':0
            }
        save_to_file(cont_filename, out_json)

    return out_json

def read_file(filename):
    json_out = {}
    with open(filename, 'r') as f:
        json_out = json.loads(f.read())
    return json_out

def save_to_file(filename, json_content):
    with open(filename, 'w') as f:
        json.dump(json_content,f,indent=1)
    
def run():

    #print('start:',out_json)
    init_json()
    #print('second:',get_out_file())
    if check_limit() >= max_limit:
        raise Exception('Enough criminal scum, you violated the law!\nLimit (35 service requests) reached!')
    else:
        success = bool
        #while success:
        #    if next_call():
        #        success = get_request()
        #       if success:
        #           inc_counter() #increments counter and updates the last request datetime
        #           print(read_file(cont_filename))

        success = get_request()
        print('Success?',success)
        if success != True:
            raise Exception('Request not completed succesfully')
        else:
            inc_counter()