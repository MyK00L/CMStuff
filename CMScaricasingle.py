import requests as rq
import getpass
import sys

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

username = input("username: ")
password = getpass.getpass("password: ")
problem = input("problem name: ")

r = rq.post("https://training.olinfo.it/api/user",json={'action':'login','keep_signed':'false','password':password,'username':username})
cookie = {'token':r.cookies['token']}

r=rq.post("https://training.olinfo.it/api/submission",json={'action':'list','task_name':problem},cookies=cookie)
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
        if not os.path.exists(problem+'/'):
            os.makedirs(problem+'/')
        r=rq.get("https://training.olinfo.it/api/files/"+k['digest']+"/"+k['name'],cookies=cookie)
        f=open(i+'/'+k['name'],'w')
        f.write(r.text)
        f.close()
else:
    r=rq.get("https://training.olinfo.it/api/files/"+todown[0]['digest']+"/"+todown[0]['name'],cookies=cookie)
    f=open(todown[0]['name'],'w')
    f.write(r.text)
    f.close()

