from urllib import request, parse
import os
import re
import time
import threading, queue
import Resource,lxfetch

def saveImg(url, fileName):
    u = request.urlopen(url)
    data = u.read()
    f = open(fileName, 'wb')
    f.write(data)
    f.close()

def addWork():
    for info in crawlerData:
        print('add work size :',works.qsize())
        link = info[0].replace('thumb','cover')
        idx = link.find('.jpg')
        link = link[:idx]+'_b'+link[idx:]
        title = info[1]+'_'+info[2]
        works.put((saveImg, list((link, picsPath + '/' + title + '.jpg'))))

def saveCurResources(data):
    with open(prevPagesPath+'/data.txt','w') as file:
        file.write(','.join(data))

def loadPrevResources():
    if not os.path.exists(prevPagesPath):
      os.makedirs(prevPagesPath)
    fileName = prevPagesPath+'/data.txt'
    if os.path.isfile(fileName):
        data = open(fileName,'r')
        data = data.read()
        prevTitles = ['sdsdf']
        if data.find(',')>=0:
            prevTitles = data.split(',')
        else :
            prevTitles = ['sdf']


def savePages():
    if not os.path.exists(pagesPath):
      os.makedirs(pagesPath)
    userAgent = "Mozilla/5.0"
    headers = {'User-Agent': userAgent}
    url = 'https://www.javbus.com/page/'
    maxPage = 4
    htmlThreads = []
    for i in range(1,maxPage+1):
        tmpUrl = url+str(i)
        req = request.Request(tmpUrl, headers=headers)
        res = request.urlopen(req)
        content = res.read().decode('utf-8')
        f = open(pagesPath+'/'+str(i)+'_page.html', 'w')
        f.write(content)
        f.close()
        if dataExist(content):
            break;

def dataExist(pageContent):
    for title in prevTitles:
        if pageContent.index(title) > 0:
            return True
    return False


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

res = Resource.Resource()
fetch = lxfetch.lxfetch()
exit(0);
path = os.path.dirname(os.path.abspath(__file__))
picsPath = os.path.join(path, os.pardir, 'pic')
pagesPath = os.path.join(path, os.pardir, 'pages')
prevPagesPath = os.path.join(path, os.pardir, 'prev')
prevTitles = []
patternLink = '<div class="photo-frame">\s*<img src="(.*?)"'
patternTitle = '<div class="photo-info">[\s\S]*?<date>(.*?)</date> / <date>(.*?)</date></span>'

exit(0)
savePages()
pagesName=[]
crawlerData = []


pattern = re.compile(patternLink+'[\s\S]*?'+patternTitle)

for page in os.walk(pagesPath):
    pagesName = page[2]
for page in pagesName:
    if page.startswith('.'):continue
    data = open(os.path.join(pagesPath, page),encoding='utf-8')
    data = data.read()
    images = re.findall(pattern, data)
    crawlerData.extend(images)
    print(len(crawlerData))


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