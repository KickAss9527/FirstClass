from urllib import request, parse
import os
import re

def saveImg(url, fileName):
    u = request.urlopen(url)
    data = u.read()
    f = open(fileName,'wb')
    f.write(data)
    print('saving...'+fileName)

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

for i in range(0,len(names)):
    fileName = path+'/'+names[i]+'.jpg'
    saveImg(images[i], fileName)




