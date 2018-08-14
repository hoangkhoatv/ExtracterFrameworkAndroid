from ginExtractor import extractor
from ginlib import path_leaf
from ginlib import device
import config
import sys
import os
import shutil
import time
import json
from json import encoder
import io
import pdb
from collections import OrderedDict
from statictis import Statictis
from rom import Rom
import dbhelper
import config

json.encoder.c_make_encoder = None
encoder.FLOAT_REPR = lambda o: format(o, '.2f')


def getfilename(dir):
    k = []
    for root, directories, filenames in os.walk(dir):
        for filename in filenames:
            k.append(os.path.join(root, filename))
    return k

def splitfilename(files):
    files1 = []
    for i in range(len(files)):
        files1.append(files[i].split('/', 1)[1])
    return files1

def createFolder():
    if not os.path.exists(config.outFolder):
        os.makedirs(config.outFolder)
    if not os.path.exists(config.tempFolder):
        os.makedirs(config.tempFolder)
    if not os.path.exists(config.romFolder):
        os.makedirs(config.romFolder)

def set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError

def copyDirectory(src, dest):
    try:
        shutil.copytree(src, dest)
    # Directories are the same
    except shutil.Error as e:
        print('Directory not copied. Error: %s' % e)
    # Any error saying that the directory doesn't exist
    except OSError as e:
        print('Directory not copied. Error: %s' % e)

def getSizeFolder(start_path = '.'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

def processScanDevice(url,sdk,version,name,id):
    createFolder()
    rom = Rom()
    startTime = time.time()
    checkfile = ""
    nameFolder = str(path_leaf(url))
    print "....Extract.... " + nameFolder
    temp = config.tempFolder+nameFolder
    copyDirectory(url,temp)
    framework,apks,output = device(temp,sdk)
    rom.time = float('%.3f' % (time.time() - startTime ))
    rom.name = name
    rom.extention = 'device'
    rom.typeFile = 'folder'
    rom.stt = 'complete'
    rom.sdk = sdk
    rom.version= version
    rom.hash = id
    rom.listApk = apks
    rom.framework = framework.__dict__
    rom.outFile = output
    rom.size = getSizeFolder(url)
    conn = dbhelper.dbhelper(config.db_name,config.user,config.host,config.password)
    conn.insert_rom_extract(rom.getName(),rom.getHash(),rom.getExt(),rom.getStt(),str(rom.getOutFile()),rom.getVersion(),rom.getTime(),rom.sdk,int(rom.getSize()),rom.getType())
    conn.end_connection()
    return json.dumps(OrderedDict(rom.__dict__),indent=4,sort_keys=False)

def extractRom(url):
    createFolder()
    extract = Rom()
    start_time = time.time()
    
    try:
        checkfile = ""
        print "....Extract.... " + str(path_leaf(url))
        extract = extractor(url)
    except:
        pass
    end_time = float('%.3f' % (time.time() - start_time))
    if extract != None:
        extract.time = end_time
        extract.name = path_leaf(url)
    conn = dbhelper.dbhelper(config.db_name,config.user,config.host,config.password)
    try:
        sdk = int(extract.getSdk())
    except ValueError:
        sdk = 0
    conn.insert_rom_extract(extract.getName(),extract.getHash(),extract.getExt(),extract.getStt(),str(extract.getOutFile()),extract.getVersion(),extract.getTime(),sdk,int(extract.getSize()),extract.getType())
    configRom = extract.getConfig()
    conn.end_connection()
    conn = dbhelper.dbhelper(config.db_name,config.user,config.host,config.password)
    print configRom
    romId = conn.query_id_rom(extract.getHash())
    conn.insert_config(romId,configRom['name'],configRom['s01'],configRom['s02'],configRom['s03'],configRom['s04'],configRom['s05'],configRom['s06'])
    conn.end_connection()
    return json.dumps(OrderedDict(extract.__dict__),indent=4,sort_keys=False)

