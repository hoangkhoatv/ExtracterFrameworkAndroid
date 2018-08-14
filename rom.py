
from androidobject import AndroidObject
class Rom:
    def __init__(self):
        self.name = ''
        self.typeFile = ''
        self.extention = ''
        self.stt = ''
        self.outFile = ''
        self.size = 0
        self.sdk = ''
        self.version = ''
        self.time = ''
        self.hash = ''
        self.listApk = []
        self.config = {}
        self.framework = AndroidObject()
    def getName(self):
        return self.name
    def getListApk(self):
        return self.listApk
    def getConfig(self):
        return self.config
    def getFramework(self):
        return self.framework
    def getHash(self):
        return self.hash
    def getType(self):
        return self.typeFile
    def getExt(self):
        return self.extention
    def getStt(self):
        return self.stt
    def getOutFile(self):
        return self.outFile
    def getSize(self):
        return self.size
    def getSdk(self):
        return self.sdk
    def getVersion(self):
        return self.version
    def getTime(self):
        return self.time