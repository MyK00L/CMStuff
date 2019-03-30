import requests as rq
import sys

user1 = input("username1: ")
user2 = input("username2: ")

user1s=[]
user2s=[]

user1n2 = []
user2n1 = []

taskscore={}

r=rq.post("https://training.olinfo.it/api/task",json={'action':'list','first':0,'last':2000000000})
for i in r.json()['tasks']:
    taskscore[i['name']]=int(0.5+100.0*i['score_multiplier'])

r = rq.post("https://training.olinfo.it/api/user",json={'action':'get','username':user1})
print(user1 + "'s score = " + str(r.json()['score']))
for i in r.json()['scores']:
    if i['score']==100:
        user1s.append(i['name'])

r = rq.post("https://training.olinfo.it/api/user",json={'action':'get','username':user2})
print(user2 + "'s score = " + str(r.json()['score']))
for i in r.json()['scores']:
    if i['score']==100:
        user2s.append(i['name'])


for i in user1s:
    if not i in user2s:
        user1n2.append(i)
user1n2.sort(key=lambda prob: taskscore.get(prob,0), reverse = True)

for i in user2s:
    if not i in user1s:
        user2n1.append(i)
user2n1.sort(key=lambda prob: taskscore.get(prob,0), reverse = True)

print("Problems " + user1 + " solved and " + user2 + " didn't solve: ")
for i in user1n2:
    print(i+" "+str(taskscore.get(i,0)))

print("Problems " + user2 + " solved and " + user1 + " didn't solve: ")
for i in user2n1:
    print(i+" "+str(taskscore.get(i,0)))
input('Press ENTER to exit')
sys.exit(0)
