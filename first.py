from urllib import request, parse
import os
import re
import time
import threading,queue

def saveImg(url, fileName):
    print('saving...'+fileName)
    print('count',threading.active_count())
    u = request.urlopen(url)
    data = u.read()
    f = open(fileName,'wb')
    f.write(data)
    f.close()



userAgent = "Mozilla/5.0"
headers = {'User-Agent':userAgent}
url = 'http://www.xiami.com'
req = request.Request(url, headers=headers)
res = request.urlopen(req)

content = res.read().decode('utf-8')
patternName = re.compile('<p class="name"><strong><a.*?>(.*?)</a')
patternImg = re.compile('<div class="album">\s*<div class="image">\s*<img src="(.*?)"')
names = re.findall(patternName, content)
images = re.findall(patternImg, content)
path = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(path, os.pardir,'pic')
print(path)

tmpTime = time.time()
threads = []
works = []#images[i],fileName

tmpCnt = 1
for i in range(0,tmpCnt*len(images)):
    idx = int(i/tmpCnt)
    works.append((images[idx],path+'/'+names[idx]+'.jpg'))

maxThreadCnt = 15
for i in range(0,maxThreadCnt):
    fileName = path+'/'+names[i]+'.jpg'
    t = threading.Thread(target=saveImg, args=(works[i]))
    t.start()
    threads.append(t)
#for t in threads:
#    t.join()


print(threading.active_count())
print('time delta:',time.time()-tmpTime)



