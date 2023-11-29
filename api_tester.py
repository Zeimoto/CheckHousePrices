import json
import requests
import base64
import datetime
import re
from dateutil.relativedelta import relativedelta

max_limit = 40
out_filename = 'request_cont.json'
out_json = {
            'first_entry': '',
            'last_entry': '',
            'counter': 0
        }
token = ""

def get_keys():
    apikey = ''
    secret = ''
    api_auth_f = 'api_auth.json'
    with open (api_auth_f, 'r') as f:
        apikey = json.loads(f.read()['apikey'])
        secret = json.loads(f.read()['secret'])
    return apikey, secret

def get_token():
    apiKey, secret = get_keys()
    
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
    #print('Response text: ',r.text)
    #print('Json Load: ',json.loads(r.text))
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
    out_json = get_out_file()
    out_json['last entry'] = get_cur_date_str()
    out_json['counter'] += 1
    save_out_file(out_json)
    
def check_limit():
    #first checks how long was the first call
    out_json = get_out_file()
    print(out_json['first_entry'])

    if a_month_ago(out_json['first_entry']):
        #if it was a month ago, then set the first entry date to the current time and reset the counter
        print('First entry is past a month now!')
        curr_datetime = get_cur_date_str()
        print('This will become the set first entry date',curr_datetime)
        out_json['first_entry'] = curr_datetime #set to current time
        out_json['counter'] = 0 #reset timer
        print(out_json)
        save_out_file(out_json)
        
    return out_json['counter']

def next_call():
    out_json = get_out_file()
    delta = relativedelta(datetime.datetime.now(), out_json['last entry'].strftime('%d/%m/%Y %H:%M'))
    hours_difference = int(delta.hours)
    if hours_difference > 12:
        inc_counter()
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

    out_json = get_out_file()
    #print('after file load:',out_json)
    if out_json == '':
        #print('WARNING: file is empty')
        out_json = {
            'first_entry':'',
            'last_entry':'',
            'counter':0
            }
        save_out_file(out_json)

    return out_json
    
def run():

    #print('start:',out_json)
    init_json()
    #print('second:',get_out_file())
    if check_limit() >= max_limit:
        raise Exception('Enough criminal scum, you violated the law!\nLimit (35 service requests) reached!')
    else:
        print(get_out_file())

def get_out_file():
    json_out = {}
    with open(out_filename, 'r') as f:
        json_out = json.loads(f.read())
    return json_out

def save_out_file(json_file):
    with open(out_filename, 'w') as f:
        json.dump(json_file,f,indent=1)

run()