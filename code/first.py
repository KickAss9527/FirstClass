from urllib import request, parse
import os
import re
import time
import threading, queue
import Resource,lxfetch, work

def saveImg(url, fileName):
    u = request.urlopen(url)
    data = u.read()
    f = open(fileName, 'wb')
    f.write(data)
    f.close()

def addWork():
    for info in fetchData:
        print('add work size :',works.qsize())
        link = info[0].replace('thumb','cover')
        idx = link.find('.jpg')
        link = link[:idx]+'_b'+link[idx:]
        title = info[1]+'_'+info[2]
        works.put((saveImg, list((link, res.pathPic + '/' + title + '.jpg'))))

res = Resource.Resource()
fetch = lxfetch.lxfetch(res)
fetch.fetchData()
fetchData = fetch.getFetchData()

threads = []
works = queue.Queue()

addWorkThread = threading.Thread(target=addWork)
threads.append(addWorkThread)
addWorkThread.start()
tmpTime = time.time()
maxTCnt = 5
for i in range(0, maxTCnt):
    w = work.Work(works)
    threads.append(w)

for t in threads:
    t.join()

print('time : ',(time.time()-tmpTime))