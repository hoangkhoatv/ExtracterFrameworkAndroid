from ginExtractor import extractor
from ginlib import path_leaf
import sys
import os
import shutil
import time
import json
from json import encoder
import io
import collections, pdb
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





def main(argv):
    data = {}
    extract = Rom()
    countImg = 0
    countDat = 0
    countRaw = 0
    countSin = 0
    countIsDone = 0
    countComplete = 0
    countTotal = 0
    for dirname, dirnames, filenames in os.walk('./' + argv[1]):
        for filename in filenames:
            start_time = time.time()
            try:
                countTotal += 1
                checkfile = ""
                print "....Extract.... " + str(os.path.join(dirname, filename))
                extract = extractor(os.path.join(dirname, filename))
                checkComplete = a['status']
                if checkComplete == 'complete':
                    countComplete += 1
                checkDone = extract.done
                if checkDone == True:
                    countIsDone += 1
                    checkType = extract.typeFile
                    if checkType == "ftf":
                        countSin += 1
                    elif checkType == "dat":
                        countDat += 1
                    elif checkType == "raw":
                        countRaw += 1
                    elif checkType == "img":
                        countImg += 1
            except:
                pass
            end_time = float('%.3f' % (time.time() - start_time))
            if extract != None:
                extract.time = end_time
            data['framework'] = extract.__dict__

    listData = collections.OrderedDict()
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
    listData[path_leaf(filename)] = data

    with io.open('report.json', 'w', encoding="utf-8") as outfile:
        outfile.write(unicode(json.dumps(listData, ensure_ascii=False,indent=4)))
    os.system('mkdir -p root')
    for dirname, dirnames, filenames in os.walk('./'):
        # print path to all filenames.
        for filename in filenames:
            checkfile = 'framework.jar'
            if (checkfile == filename):
                tmp = './root' + dirname[1:] + '.jar'
                os.system('cp -r ' + os.path.join(dirname, filename) + ' ' + tmp)


if __name__ == '__main__':
    main(sys.argv)
