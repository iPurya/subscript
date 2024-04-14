import requests
import re
import subprocess
import json
import concurrent.futures
from telebot import TeleBot

bot = TeleBot("6568272192:AAHvZqvDadJCsRgmZuodGwNy5DMgWO7-flw")
CHANNEL = -1002110734507

TARGET = "starbucks.com"
CHR = 3

all_subs = set()
executor = concurrent.futures.ThreadPoolExecutor(max_workers=100)

def split_list(lst, c):
    return [lst[i:i+c] for i in range(0, len(lst), c)]

def readlines(file_name):
    tmp_set = set()
    with open(file_name,"r") as f:
        for line in f.readlines():
            tmp_set.add(line.strip())
    return tmp_set

def writelines(filename, lines):
    with open(filename, "w") as f:
        for line in lines:
            f.write(line + "\n")

def subfinder(target):
    global all_subs
    subprocess.call(['subfinder','-d',target,'-all','-o','subfinder.txt'])
    [all_subs.add(x) for x in readlines("subfinder.txt")]

def findomain(target):
    global all_subs
    subprocess.call(['findomain','-t',target,'-u','findomain.txt'])
    [all_subs.add(x) for x in readlines("findomain.txt")]

def shuffledns(target):
    global all_subs
    subprocess.call(['shuffledns','-w',f'{CHR}char.txt','-d',target,'-r','resolvers','-m','/usr/local/bin/massdns', '-o','shuffle.txt'])
    [all_subs.add(x) for x in readlines("shuffle.txt")]

def httpx(filename):
    cmd = ['httpx', '-list', filename ,'-silent','-t','100', '-follow-host-redirects', '-title', '-status-code', '-cdn', '-tech-detect', '-H', "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:108.0) Gecko/20100101 Firefox/108.0",'-j','-o','httpx.json']
    subprocess.call(cmd)

tasks = []
#tasks.append(executor.submit(subfinder, TARGET))
#tasks.append(executor.submit(findomain, TARGET))


for future in concurrent.futures.as_completed(tasks):
    print(future.result(), len(all_subs))

#writelines("allsubs.txt", all_subs)
httpx("allsubs.txt")

alldata=[]
with open("httpx.json","r", encoding="utf-8") as f:
    for line in f.readlines():
        data = json.loads(line.strip())
        alldata.append(data)

status_200 = [x for x in alldata if x.get("status_code") == 200]

i = 0
for x in split_list(status_200, 50):
    txt = "STATUS 200 :\n\n"
    for res in x:
        i += 1
        txt += f"{i}. {res['url']} — {res['status_code']}\n"
    bot.send_message(CHANNEL, txt)