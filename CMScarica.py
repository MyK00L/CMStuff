import requests as rq
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
username=input("username: ")
password=input("password: ")
folder=input("destination folder: ")

if folder[len(folder)-1]!='/':
    folder+='/'

if not os.path.exists(folder):
    os.makedirs(folder)

#---login---
payload={'action':'login','keep-signed':'false','password':password,'username':username}
r=rq.post("https://training.olinfo.it/api/user",json=payload)
if('error' in r.json()):
    print("Error: " + r.json()['error'])
    sys.exit(0)
if(r.status_code!=200):
    print("Status code: "+str(r.status_code));
    sys.exit(0)

#---get solved list--- 
cookie = {'token':r.cookies['token']}
payload={'action':'get','username':username}
r=rq.post("https://training.olinfo.it/api/user",json=payload,cookies=cookie)
if(r.status_code!=200):
    print("Status code: "+str(r.status_code));
    sys.exit(0)
solved=[]
for i in r.json()['scores']:
    if i['score']==100:
        solved.append(i['name'])

#---download solutions---
print("About to download " + str(len(solved)) + " solutions.")
for i in solved:
    print("downloading " + i + "...")
    payload={'action':'list','task_name':i}
    r=rq.post("https://training.olinfo.it/api/submission",json=payload,cookies=cookie)
    maxspeed=20000
    todown=[]
    for j in r.json()['submissions']:
        if j['score']==100.0:
            t=getspeed(j['id'],cookie)
            if t<maxspeed:
                maxspeed=t
                todown=j['files']
    if len(todown)>1:
        for k in todown:
            if not os.path.exists(folder+i+'/'):
                os.makedirs(folder+i+'/')
            r=rq.get("https://training.olinfo.it/api/files/"+k['digest']+"/"+k['name'],cookies=cookie)
            f=open(folder+i+'/'+k['name'],'w')
            f.write(r.text)
            f.close()
    else:
        r=rq.get("https://training.olinfo.it/api/files/"+todown[0]['digest']+"/"+todown[0]['name'],cookies=cookie)
        f=open(folder+todown[0]['name'],'w')
        f.write(r.text)
        f.close()
sys.exit(0)
