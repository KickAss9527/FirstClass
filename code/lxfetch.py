from urllib import request, parse
import re,os,Resource

class lxfetch():
    def __init__(self, resourse):
        self.ptnLink='<div class="photo-frame">\s*<img src="(.*?)"'
        self.ptnTitle='<div class="photo-info">[\s\S]*?<date>(.*?)</date> / <date>(.*?)</date></span>'
        self.iFetchMaxPage = 4
        self.resourse = resourse


    def fetchData(self):
        headers = {'User-Agent': "Mozilla/5.0"}
        url = 'https://www.xxxxx.com/page/'
        htmlThreads = []
        for i in range(1,self.iFetchMaxPage+1):
            tmpUrl = url+str(i)
            req = request.Request(tmpUrl, headers=headers)
            res = request.urlopen(req)
            content = res.read().decode('utf-8')#.encode('GBK').decode('GBK')
            f = open(self.resourse.pathPage+'/'+str(i)+'_page.html', 'w')
            f.write(content)
            f.close()
            if i==1:
                self.__saveFirstData(content)
            if self.__checkDataExist(content, self.resourse.lastData):
                break;


    def __saveFirstData(self,html):
        data = re.findall(self.ptnTitle, html)
        self.resourse.saveLastData([data[0][0]])

    def __checkDataExist(self,html, prevData):
        for title in prevData:
            if html.index(title) > 0:
                return True
        return False


    def getFetchData(self):
        pattern = re.compile(self.ptnLink+'[\s\S]*?'+self.ptnTitle)
        res = []
        for page in os.walk(self.resourse.pathPage):
            pagesName = page[2]
        for page in pagesName:
            if page.startswith('.'):continue
            data = open(os.path.join(self.resourse.pathPage, page),encoding='utf-8')
            res.extend(re.findall(pattern, data.read()))
            print(len(res))
        return res
