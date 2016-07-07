import os
class Resource():
    def __init__(self):
        path = os.path.dirname(os.path.abspath(__file__))
        self.pathPic = os.path.join(path, os.pardir, 'pic')
        self.pathPage = os.path.join(path, os.pardir, 'pages')
        self.pathLastData = os.path.join(path, os.pardir, 'prev')
        self.checkFolder(self.pathPic)
        self.checkFolder(self.pathPage)
        self.checkFolder(self.pathLastData)

        self.lastData = []


    def checkFolder(path):
        if not os.path.exists(path):
            os.makedirs(path)


    def save(data):
        print('s')


    def getLastData(self,data):
        fileName = self.pathLastData+'/data.txt'
        if os.path.isfile(fileName):
            data = open(fileName,'r')
            data = data.read()
            if data.find(',')>=0:
                self.lastData = data.split(',')
            else:
                self.lastData = [data]