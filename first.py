from urllib import request, parse
import re
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

for i in range(0,len(names)):
    u = request.urlopen(images[i])
    data = u.read()
    fileName = names[i]+'.jpg'
    f = open(fileName,'wb')
    f.write(data)
    print(images[i],'*saving...',i)
    f.close()

# def saveImg(self, url, fileName):
#     u = request.urlopen(url)
#     data = u.read()
#     f = open(fileName,'wb')
#     f.write(data)
#     print('saving...')
#     f.close()


