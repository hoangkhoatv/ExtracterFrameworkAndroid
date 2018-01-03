from ginExtractor import extractor
from ginlib import path_leaf
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



    # listStatictis = collections.OrderedDict()
    # percentDat = float(countDat) / float(countIsDone) * 100.0
    # percentSin = float(countSin) / float(countIsDone) * 100.0
    # percentRaw = float(countRaw) / float(countIsDone) * 100.0
    # percentImg = 100.0 - percentDat - percentSin - percentRaw
    # percentDone = float(countIsDone) / float(countComplete) * 100.0
    # percentComplete = float(countComplete) / float(countTotal) * 100.0
    # statictis = Statictis()
    # statictis.total= countTotal
    # statictis.complete = {'total': countComplete, 'percent': percentComplete}
    # statictis.done = {'total': countIsDone, 'percent': percentDone}
    # statictis.dat= {'total': countDat, 'percent': percentDat}
    # statictis.ftf = {'total': countSin, 'percent': percentSin}
    # statictis.raw = {'total': countRaw, 'percent': percentRaw}
    # statictis.image = {'total': countImg, 'percent': percentImg}
    # listData['statictis'] = json.dumps(statictis.__dict__)


    # with io.open('report.json', 'w', encoding="utf-8") as outfile:
    #     outfile.write(unicode(json.dumps(OrderedDict(extract.__dict__), ensure_ascii=False,indent=4)))
    return json.dumps(OrderedDict(extract.__dict__),indent=4,sort_keys=False)

