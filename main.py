import requests
import json
from requests.api import get
import sys
import base64

#If you're reading this, you're looking over the code. If you're trying to debug this, 
#I have commented out several print statements that might be helpful to you. Good luck.

#python3 ../main.py add $CERTBOT_DOMAIN "_acme-challenge" $CERTBOT_VALIDATION
method = sys.argv[1] #add
domain = sys.argv[2] #$CERTBOT_DOMAIN
zone = sys.argv[3] #"_acme-challenge"
cerbotKey = sys.argv[4] #$CERTBOT_VALIDATION

#if any of this fails, we want the program to exit
secretPath = "/dockerRoot/domains/" + domain.replace(".", "_") + ".json"
file = None
print("Loading file")
file = open(secretPath, mode='r')
print("file loaded")

file_raw = file.read()
file.close()
file_json = json.loads(file_raw)

username = file_json["username"]
apiKey_raw = file_json["apiKey"]
apikey = username + ":" + apiKey_raw
cpanelUrl = file_json["cpanelUrl"]
if (cpanelUrl):
    cpanelUrl = cpanelUrl.replace("https://", "").replace("http://","")

#region 
#In my case, namecheap does not support these api calls, so I'm referencing a different domain and using cname
#controllingDomain = domain
if("controllingDomain" in file_json):
    domain = file_json["controllingDomain"]

if(("ALIAS_" + zone) in file_json):
    zone = file_json[("ALIAS_" + zone)]
#endRegion


def addDnsRecord(serial, zone, type, data):
    #print("addDnsRecord")
    #print(str(serial) + " " + str(zone) + " " + str(type) + " " + str(data))
    url = f'https://{cpanelUrl}/execute/DNS/mass_edit_zone?zone={domain}&serial={serial}&add='
    if(not isinstance(data, list)):
        data = [data]
    add = {"dname":zone, "ttl":600, "record_type":type, "data":data}
    url += json.dumps(add)
    #print("url: " + str(url))
    headers = {}
    headers["Authorization"] = "cpanel " + apikey
    resp = requests.get(url, headers=headers)
    return resp.text

def removeDnsRecord(serial, zone, idx):
    #print("removeDnsRecord")
    if (idx == ""):
        return "idx error"
    url = f'https://{cpanelUrl}/execute/DNS/mass_edit_zone?zone={domain}&serial={serial}&zone={zone}&remove={idx}'
    #print(url)
    headers = {}
    headers["Authorization"] = "cpanel " + apikey
    resp = requests.get(url, headers=headers)
    return resp.text

def getSerial():
    print("getSerial")
    url = f'https://{cpanelUrl}/execute/DNS/parse_zone?zone={domain}'
    #print("url: " + str(url))
    headers = {}
    headers["Authorization"] = "cpanel " + apikey
    #print("auth: " + str(headers["Authorization"]))
    resp = requests.get(url, headers=headers)
    #print("resp: " + str(resp.text))
    resp_json = json.loads(resp.text)
    ret = 0
    for rec in resp_json["data"]:
        if ("record_type" in rec and rec["record_type"] == "SOA"):
            b64 = rec["data_b64"][2]
            return base64.b64decode(b64).decode("utf-8")
    return resp.text

def getData():
    #print("getData")
    url = f'https://{cpanelUrl}/execute/DNS/parse_zone?zone={domain}'
    #print("url: " + url)
    headers = {}
    headers["Authorization"] = "cpanel " + apikey
    resp = requests.get(url, headers=headers)
    return resp.text

def getLineIndex(zone, value=""):
    #print("getLineIndex")
    url = f'https://{cpanelUrl}/execute/DNS/parse_zone?zone={domain}'
    #print("url: " + url)
    headers = {}
    headers["Authorization"] = "cpanel " + apikey
    resp = requests.get(url, headers=headers)
    resp_json = json.loads(resp.text)
    for rec in resp_json["data"]:
        if (rec["type"] == "record" and "dname_b64" in rec and "data_b64" in rec):
            zn = base64.b64decode(rec["dname_b64"]).decode("utf-8").strip()
            val = base64.b64decode(rec["data_b64"][0]).decode("utf-8").strip()
            if (value != ""): #if we want to verify the data on the record as well. There will be seperate objects per record
                if (zone == zn and value == val):
                    return rec["line_index"]
            else:
                if(zone == zn):
                    return rec["line_index"]
    return resp.text

    
if (method == "serial"):
    msg = getSerial()
    print(msg)
if (method == "add"):
    #print("adding for " + domain)
    serial = getSerial()
    #print("serial: " + str(serial))
    msg = addDnsRecord(serial, zone, "TXT", cerbotKey)
    #print(msg)
if (method == "remove"):
    #print("removing for " + domain)
    serial = getSerial()
    idx = getLineIndex(zone, cerbotKey)
    #print("serial: " + str(serial))
    msg = removeDnsRecord(serial, zone, idx)
    #print(msg)
if(method == "test"):
    print(getData())
if(method == "idx"):
    #print("idx")
    tmp = getLineIndex(zone, cerbotKey)
    print(tmp)
