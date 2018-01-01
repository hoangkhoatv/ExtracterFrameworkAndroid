class Rom:
    def __init__(self):
        self.typeFile = ''
        self.extention = ''
        self.stt = ''
        self.outFile = ''
        self.size = 0
        self.sdk = ''
        self.version = ''
        self.done = False
        self.time = ''
        self.hash = ''
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
    def isDone(self):
        return self.done
    def getTime(self):
        return self.time