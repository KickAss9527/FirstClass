from urllib import request, parse
import os
import re
import time
import threading, queue


def saveImg(url, fileName):
    print('saving...' + fileName)
    print('count', threading.active_count())
    u = request.urlopen(url)
    data = u.read()
    f = open(fileName, 'wb')
    f.write(data)
    f.close()


class Work(threading.Thread):
    def __init__(self, work_queue):
        self.work_queue = work_queue
        threading.Thread.__init__(self)
        self.start()


    def run(self):
        while True:
            try:
                dofun, args = self.work_queue.get(block=False)
                dofun(args[0], args[1])
                self.work_queue.task_done()
            except Exception as e:
                print('ex')
                break;


userAgent = "Mozilla/5.0"
headers = {'User-Agent': userAgent}
url = 'http://www.xiami.com'
req = request.Request(url, headers=headers)
res = request.urlopen(req)

content = res.read().decode('utf-8')
patternName = re.compile('<p class="name"><strong><a.*?>(.*?)</a')
patternImg = re.compile('<div class="album">\s*<div class="image">\s*<img src="(.*?)"')
names = re.findall(patternName, content)
images = re.findall(patternImg, content)
path = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(path, os.pardir, 'pic')

tmpTime = time.time()
threads = []
works = queue.Queue()

tmpCnt = 1
for i in range(0, tmpCnt * len(images)):
    idx = int(i / tmpCnt)
    works.put((saveImg, list((images[idx], path + '/' + names[idx] + '.jpg'))))

maxTCnt = works.qsize()
for i in range(0, maxTCnt):
    w = Work(works)
    threads.append(w)

for t in threads:
    t.join()

print(threading.active_count())
print('time delta:', time.time() - tmpTime)
