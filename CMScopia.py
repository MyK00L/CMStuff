import requests as rq
import getpass
import base64
import time
import sys
import os

def getspeed(idn,cookie):
    r=rq.post("https://training.olinfo.it/api/submission",cookies=cookie,json={'action':'details','id':idn})
    res=r.json()['score_details'][0]['testcases'][0]['time']
    for i in r.json()['score_details']:
        for j in i['testcases']:
            if j['time']==None:
                continue
            if j['time']>res:
                res=j['time']
    if res==None:
        return 0
    return res

#---input---
username1=input("username1: ")
password1=getpass.getpass("password1: ")
username2=input("username2: ")
password2=getpass.getpass("password2: ")

#---login---
payload={'action':'login','keep-signed':'false','password':password1,'username':username1}
r=rq.post("https://training.olinfo.it/api/user",json=payload)
if('error' in r.json()):
    print("Error: " + r.json()['error'])
    sys.exit(0)
if(r.status_code!=200):
    print("Status code: "+str(r.status_code));
    sys.exit(0)

cookie1 = {'token':r.cookies['token']}

payload={'action':'login','keep-signed':'false','password':password2,'username':username2}
r=rq.post("https://training.olinfo.it/api/user",json=payload)
if('error' in r.json()):
    print("Error: " + r.json()['error'])
    sys.exit(0)
if(r.status_code!=200):
    print("Status code: "+str(r.status_code));
    sys.exit(0)

cookie2 = {'token':r.cookies['token']}

#---get solved list--- 
payload={'action':'get','username':username1}
r=rq.post("https://training.olinfo.it/api/user",json=payload,cookies=cookie1)
if(r.status_code!=200):
    print("Status code: "+str(r.status_code));
    sys.exit(0)
solved=[]
for i in r.json()['scores']:
    if i['score']==100:
        solved.append(i['name'])

#---download solutions---
print("About to copy " + str(len(solved)) + " solutions.")
for i in solved:
    print("copying " + i + "...")
    payload={'action':'list','task_name':i}
    r=rq.post("https://training.olinfo.it/api/submission",json=payload,cookies=cookie1)
    if r.json()['success']==0:
        continue
    maxspeed=20000
    todown=[]
    for j in r.json()['submissions']:
        if j['score']==100.0:
            t=getspeed(j['id'],cookie1)
            if t<maxspeed:
                maxspeed=t
                todown=j['files']
    if len(todown)>1:
        #for k in todown:
            #if not os.path.exists(folder+i+'/'):
                #os.makedirs(folder+i+'/')
            #r=rq.get("https://training.olinfo.it/api/files/"+k['digest']+"/"+k['name'],cookies=cookie1)
            #f=open(folder+i+'/'+k['name'],'w')
            #f.write(r.text)
            #f.close()
        print(i+" not copied")
    else:
        r=rq.get("https://training.olinfo.it/api/files/"+todown[0]['digest']+"/"+todown[0]['name'],cookies=cookie1)
        payload={"files":{todown[0]['name'].split('.')[0]+".%l":{"filename":"ace.cpp","data":base64.b64encode(bytes(r.text,'utf-8')).decode('utf-8')}},"action":"new","task_name":i}
        r=rq.post("https://training.olinfo.it/api/submission",json=payload,cookies=cookie2)
        while r.json().get('success',1)==0 and r.json().get('error','not')=='Too frequent submissions!':
            print("retrying in 22 seconds")
            time.sleep(22)
            r=rq.post("https://training.olinfo.it/api/submission",json=payload,cookies=cookie2)
sys.exit(0)
