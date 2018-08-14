import requests
import config
class postApk (object):
    urlFile = ""

    def __init__(self, urlFile):
        self.urlFile = urlFile
        
    def analyze_apk(self):
        files = {'file': open(self.urlFile,'rb')}
        r = requests.post(config.API_URL+"/analyze", files=files)
        if r.status_code == 200:
            return r.text
        else:
            return None
        
    def available_apk(self,hash):
        url = config.API_URL + "/get-result/" + hash 
        r = requests.get(url)
        if r.status_code == 200:
            return r.text
        else:
            return None