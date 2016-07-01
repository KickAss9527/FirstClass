from urllib import request, parse
import os
import re
import time
import threading, queue


def saveImg(url, fileName):
    u = request.urlopen(url)
    data = u.read()
    f = open(fileName, 'wb')
    f.write(data)
    f.close()

def addWork():
    for i in range(0, 100):
        print('add work size :',works.qsize())
        works.put((saveImg, list((images[1], path + '/' + names[1] + '.jpg'))))
        time.sleep(1)


class Work(threading.Thread):
    def __init__(self, work_queue):
        self.work_queue = work_queue
        threading.Thread.__init__(self)
        self.start()

    def run(self):
        while True:
            try:
                if self.work_queue.empty():
                    time.sleep(1)
                    print('sleep over')
                    continue;
                dofun, args = self.work_queue.get(block=False)
                dofun(args[0], args[1])
                self.work_queue.task_done()
            except Exception as e:
                print('ex')
                break;

path = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(path, os.pardir, 'pic')
userAgent = "Mozilla/5.0"
headers = {'User-Agent': userAgent}
url = 'https://www.javbus.com/page/'
page = 10
htmlThreads = []
for i in range(1,page+1):
    tmpUrl = url+str(i)
    req = request.Request(tmpUrl, headers=headers)
    res = request.urlopen(req)
    content = res.read().decode('utf-8')
    f = open(path+'/'+str(i)+'_page.html', 'w')
    f.write(content)
    f.close()
exit()
req = request.Request(url, headers=headers)
res = request.urlopen(req)

content = res.read().decode('utf-8')




patternName = re.compile('<p class="name"><strong><a.*?>(.*?)</a')
patternImg = re.compile('<div class="album">\s*<div class="image">\s*<img src="(.*?)"')
names = re.findall(patternName, content)
images = re.findall(patternImg, content)

tmpTime = time.time()
threads = []
works = queue.Queue()

addWorkThread = threading.Thread(target=addWork)
threads.append(addWorkThread)
addWorkThread.start()

maxTCnt = 5
for i in range(0, maxTCnt):
    w = Work(works)
    threads.append(w)

for t in threads:
    t.join()

print(threading.active_count())
print('time delta:', time.time() - tmpTime)
