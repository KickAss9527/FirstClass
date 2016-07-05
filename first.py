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
    for info in infos:
        print('add work size :',works.qsize())
        link = info[0].replace('thumb','cover')
        idx = link.find('.jpg')
        link = link[:idx]+'_b'+link[idx:]
        title = info[1]+'_'+info[2]
        works.put((saveImg, list((link, picsPath + '/' + title + '.jpg'))))
def savePages():

    pagesPath = os.path.join(path, os.pardir, 'pages')
    if not os.path.exists(pagesPath):
      os.makedirs(pagesPath)
    userAgent = "Mozilla/5.0"
    headers = {'User-Agent': userAgent}
    url = 'https://www.javbus.com/page/'
    page = 4
    htmlThreads = []
    for i in range(1,page+1):
        tmpUrl = url+str(i)
        req = request.Request(tmpUrl, headers=headers)
        res = request.urlopen(req)
        content = res.read().decode('utf-8')
        f = open(pagesPath+'/'+str(i)+'_page.html', 'w')
        f.write(content)
        f.close()


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
                print('left work count : ', self.work_queue.qsize())
            except Exception as e:
                print('ex:',e)
                break;

path = os.path.dirname(os.path.abspath(__file__))
picsPath = os.path.join(path, os.pardir, 'pic')
pagesPath = os.path.join(path, os.pardir, 'pages')
savePages()
pagesName = []
strLinkPtn = '<div class="photo-frame">\s*<img src="(.*?)"'
strTitlePtn = '<div class="photo-info">[\s\S]*?<date>(.*?)</date> / <date>(.*?)</date></span>'
pattern = re.compile(strLinkPtn+'[\s\S]*?'+strTitlePtn)
infos = []
for page in os.walk(pagesPath):
    pagesName = page[2]
for page in pagesName:
    if page.startswith('.'):continue
    data = open(os.path.join(pagesPath, page),encoding='utf-8')
    data = data.read()
    images = re.findall(pattern, data)
    infos.extend(images)
    print(len(infos))

# req = request.Request(url, headers=headers)
# res = request.urlopen(req)
#
# content = res.read().decode('utf-8')
#
#
#
#
# patternName = re.compile('<div class="photo-frame"><strong><a.*?>(.*?)</a')
# patternImg = re.compile('<div class="album">\s*<div class="image">\s*<img src="(.*?)"')
# names = re.findall(patternName, content)
# images = re.findall(patternImg, content)
#
threads = []
works = queue.Queue()

addWorkThread = threading.Thread(target=addWork)
threads.append(addWorkThread)
addWorkThread.start()
tmpTime = time.time()
maxTCnt = 5
for i in range(0, maxTCnt):
    w = Work(works)
    threads.append(w)

for t in threads:
    t.join()

print('time : ',(time.time()-tmpTime))