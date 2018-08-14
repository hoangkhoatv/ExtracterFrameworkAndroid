import os
from flask import Flask, request, redirect, url_for,jsonify,Response
from werkzeug import secure_filename
from werkzeug.datastructures import ImmutableMultiDict

import gintool
import scanreportfile
import json
import postApk
import config
import dbhelper
import time
import thread
import json
import ginlib
from rom import Rom
from androidobject import AndroidObject
from collections import OrderedDict
import pdb
UPLOAD_FOLDER = '/home/androidscan/ExtracterRomToFrameworkAndroid/rom'
# UPLOAD_FOLDER = '/mnt/c/Users/CNSC/Documents/ExtracterRomToFrameworkAndroid/rom'

ALLOWED_EXTENSIONS = set(['rar', 'zip', 'tar', 'ftf'])
app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
    
def workerAvailable(hashRom,hashApk,url,isFramework,name,size):
    conn = dbhelper.dbhelper(config.db_name,config.user,config.host,config.password)
    idRom = conn.query_id_rom(hashRom)
    if isFramework==True:
        conn.insert_rom_details_framework(idRom,False,False,hashApk,name,size)
    else:
        conn.insert_rom_details(idRom,False,False,hashApk,name,size)
    appid = conn.query_id_app(hashApk)
    conn.insert_xrom(appid,hashApk,False)
    req = postApk.postApk(url)
    scan = req.available_apk(hashApk)
    checkVirtt = 0
    if scan == None:
        analyze = req.analyze_apk()
        while analyze == None:
            analyze = req.analyze_apk()
            time.sleep(20)
        analyze = json.loads(analyze)
        conn.update_xrom(hashApk,True)
        isSource,isSink = isSensitiveSourceCriticalSink(analyze)
        conn.update_xrom_soure_sink(hashApk,isSource,isSink)
        while checkVirtt !=1:
            virtt = scanreportfile.postVirustotal(url)
            if virtt!=None:
                try:
                    checkVirtt = virtt['response_code']
                except:
                    checkVirtt = 0
            else:
                checkVirtt = 0
            if checkVirtt == 0:
                time.sleep(20)
        
        conn.insert_virustotal(
            appid,virtt['scanid'],
            virtt['response_code'],
            virtt['scan_date'],
            virtt['sha256'],
            virtt['total'],
            virtt['positives'],
            virtt['permalink'],
            str(virtt)
            )
        conn.update_rom_details(hashApk)
    else:
        conn.update_xrom(hashApk,True)
        scan = json.loads(scan)
        conn.update_xrom(hashApk,True)
        isSource,isSink = isSensitiveSourceCriticalSink(scan)
        conn.update_xrom_soure_sink(hashApk,isSource,isSink)
        while checkVirtt !=1:
            virtt = scanreportfile.postVirustotal(url)
            if virtt!=None:
                try:
                    checkVirtt = virtt['response_code']
                except:
                    checkVirtt = 0
            else:
                checkVirtt = 0
            if checkVirtt == 0:
                time.sleep(20)
        
        conn.insert_virustotal(
            appid,virtt['scan_id'],
            virtt['response_code'],
            virtt['scan_date'],
            virtt['sha256'],
            virtt['total'],
            virtt['positives'],
            virtt['permalink'],
            str(virtt)
            )
        conn.update_rom_details(hashApk)
            
def processApk(result):
    data = json.loads(result)
    for apk in data['listApk']:
        try:
            thread.start_new_thread( workerAvailable, (data['hash'],apk['hash'],data['outFile']+ "/" + apk['name'],False,apk['name'],apk['size'],) )
            time.sleep(1)
        except:
            print "Error Scan APK"
    try:
        thread.start_new_thread( workerAvailable, (data['hash'],data['framework']['hash'],data['outFile']+ "/" + data['framework']['name'],True,data['framework']['name'],data['framework']['size'],) )
    except:
        print "Error Scan Framework"

def isSensitiveSourceCriticalSink(data):
    isSource = False
    isSink = False
    if len(data['flows']) != 0:
        for flow in data['flows']:
            if flow['criticalSink'] == True:
                isSink = True
            elif flow['sensitiveSource'] == True:
                isSource = True
            if isSink == True and isSource == True:
                return isSource,isSink
    return isSource,isSink

def avaliable_rom(rom):
    extract = Rom()
    listApk = []
    config = {}
    framework = AndroidObject()
    extract.name = rom[0][0]
    extract.hash = rom[0][1]
    extract.extention = rom[0][2]
    extract.outFile = rom[0][3]
    extract.version = rom[0][4]
    extract.time = rom[0][5]
    extract.sdk = rom[0][6]
    extract.size = rom[0][7]
    extract.stt = rom[0][8]
    extract.typeFile = rom[0][9]

    config['name']=rom[0][14]
    config['s01']=rom[0][15]
    config['s02']=rom[0][16]
    config['s03']=rom[0][17]
    config['s04']=rom[0][18]
    config['s05']=rom[0][19]
    config['s06']=rom[0][20]

    for temp in rom:
        if temp[13] == True:
            framework.hash = temp[10]
            framework.name = temp[11]
            framework.size = temp[12]
        else:
            apk = AndroidObject()
            apk.hash = temp[10]
            apk.name = temp[11]
            apk.size = temp[12]
            listApk.append(apk.__dict__)
    extract.framework = framework.__dict__
    extract.config = config
    extract.listApk = listApk
    return extract
   
@app.route("/rom", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            hashRom = ginlib.getHash(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            conn = dbhelper.dbhelper(config.db_name,config.user,config.host,config.password)
            rom = conn.check_rom(hashRom)
            if (rom!=None):
                romid = conn.query_id_rom(hashRom)
                data = conn.get_data_rom(romid)
                extract = avaliable_rom(data)
                result = json.dumps(OrderedDict(extract.__dict__),indent=4,sort_keys=False)       
            else:
                result = gintool.extractRom(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                try: 
                    thread.start_new_thread(processApk, (result,))
                except:
                    print "Error Post APK"
            return Response(response=result, status=200, mimetype='application/json')
    return {"message":"File Not Support"}

@app.route("/isscan", methods=['POST'])
def get_isscan():
    if request.method == 'POST':
        deviceID = request.form['id'].strip( '"' )
        print "Scan...." 
        conn = dbhelper.dbhelper(config.db_name,config.user,config.host,config.password)
        rom = conn.check_rom(deviceID)
        if rom != None:
            romid = conn.query_id_rom(deviceID)
            data = conn.get_data_rom(romid)
            extract = avaliable_rom(data)
            result = json.dumps(OrderedDict(extract.__dict__),indent=4,sort_keys=False) 
            return Response(response=result, status=200, mimetype='application/json')
        else:
            return Response(response=json.dumps({'message':'Not Found'}), status=500, mimetype='application/json')
    return Response(response=json.dumps({'message':'Error'}), status=401, mimetype='application/json')

@app.route("/scan", methods=['POST'])
def api_scan():
    if request.method == 'POST':
        print 'Processing...'
        start = time.time()
        deviceID = request.form['id'].strip( '"' )
        conn = dbhelper.dbhelper(config.db_name,config.user,config.host,config.password)
        rom = conn.check_rom(deviceID)
        if rom != None:
            romid = conn.query_id_rom(deviceID)
            data = conn.get_data_rom(romid)
            extract = avaliable_rom(data)
            result = json.dumps(OrderedDict(extract.__dict__),indent=4,sort_keys=False)       
        else:
            uploaded_files = request.files.getlist("file")
            uri = json.loads(request.form['uri'])
            version = (request.form['version']).strip( '"' )
            sdk = (request.form['sdk']).strip( '"' )
            name = request.form['name'].strip( '"' )
            folderDevice = UPLOAD_FOLDER + '/' + deviceID
            i = 0 
            for file in uploaded_files:
                url = uri[i]['path']
                path, mFile = os.path.split(url)
                folderTemp = folderDevice  + path
                if not os.path.exists(folderTemp):
                    os.makedirs(folderTemp)
                file.save(os.path.join(folderTemp , file.filename))
                i = i + 1
            result = gintool.processScanDevice(folderDevice,sdk,version,name,deviceID)

            try: 
                    thread.start_new_thread(processApk, (result,))
            except:
                    print "Error Post APK"
        finish = (time.time() - start)/60
        print (finish)
        return Response(response=result,  status=200, mimetype='application/json')
    return Response(response=json.dumps({"message":"Error"}),  status=400, mimetype='application/json')

@app.route('/virustotal', methods = ['GET'])
def api_virustotal():
    if request.method == 'GET':
        if 'url' in request.args:
            print request.args['url']
            data =  scanreportfile.postVirustotal(request.args['url'])
            js = jsonify(data)
            resp = js
            return resp
    return "Pending"

if __name__ == '__main__':
     app.run(host='0.0.0.0',port=5050)
