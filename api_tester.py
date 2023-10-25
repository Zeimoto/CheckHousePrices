import sqlite3
# import socket
import urllib.request, urllib.parse, urllib.error
import json
import oath
import requests
from requests.auth import HTTPBasicAuth

method = "POST"
url = "https://api.idealista.com/3.5/es/search"
apiKey = "627n3iclwzi6fopdplmxtvx33hmm97lq"
secret = "WDWFpGihFaYO"
auth = HTTPBasicAuth(apiKey,secret)
rsp = requests.request(method, url, headers=None, auth=auth)


# mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# mysocket.connect(('data.pr4e.org', 80))
# cmd = 'GET http://data.pr4e.org/romeo.txt HTTP/1.0\r\n\n'.encode()
# mysocket.send(cmd)

# while True:
#     data = mysocket.recv(512)
#     if len(data) < 1:
#         break
#     print(data.decode())
# mysocket.close()


# fhand = urllib.request.urlopen('http://data.pr4e.org/romeo.txt')
# for line in fhand:
#     print(line.decode().strip())

# serviceurl = "https://api.idealista.com/3.5/es/search"

# while True:
#     address = input('Enter location: ')
    
#     url = serviceurl + urllib.parse.urlencode({'address':address})

#     print('Retrieving',url)
#     uh = urllib.request.urlopen(url)
#     data = uh.read().decode()
#     print('Retrieved',len(data), 'characteres')

#     try:
#         js = json.loads(data)
#     except:
#         js = None

# # Check if we got a good status
#     if not js or 'status' not in js or js['status'] != 'OK':
#         print('=== Failure to Retrieve ===')
#         print(data)
#         continue

#     print(json.dumps(js, indent=4))

    