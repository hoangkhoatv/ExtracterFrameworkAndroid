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
json.encoder.c_make_encoder = None

encoder.FLOAT_REPR = lambda o: format(o, '.2f')


def getfilename(dir):
    k=[]
    for root, directories, filenames in os.walk(dir):
        for filename in filenames:
            k.append(os.path.join(root,filename))
    return k

def splitfilename(files):
    files1 = []
    for i in range(len(files)):
        files1.append(files[i].split('/', 1)[1])
    return files1



def dump2(jarfile):
    tmp = 'apktool d ' + jarfile
    os.system(tmp)
    directory = jarfile.split('/')[len(jarfile.split('/'))-1]
    if os.path.exists('codedump/' + directory):
        os.system('rm -rf ' + 'codedump/' + directory)
    os.makedirs('codedump/' + directory)
    out = directory + '.out'
    if directory[len(directory)-4:len(directory)] == '.apk':
        out = directory[0:len(directory)-4]    
    files = getfilename(out + '/smali')
    files1 = splitfilename(splitfilename(files))
    for i in range(len(files1)):
        k = files1[i].replace('/','.')
        shutil.copy2(files[i], 'codedump/' + directory + '/' + k)
    os.system('mv -f ' + out + ' smali')




def main(argv):
    data={}
    countImg = 0
    countDat = 0
    countRaw = 0
    countSin = 0
    countIsDone = 0
    countComplete = 0
    countTotal = 0
    for dirname, dirnames, filenames in os.walk('./'+argv[1]):
        for filename in filenames:
            start_time = time.time() 
            try:
                countTotal += 1 
                a={}
                checkfile = ""
                print "....Extract.... " + str(os.path.join(dirname, filename))
                a = extractor(os.path.join(dirname, filename))
                checkComplete = a['status']
                if checkComplete == 'complete':
                    countComplete += 1
                checkDone = a['isDone']
                if checkDone == True:
                    countIsDone += 1
                    checkType = a['type']
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
            if a != None:
                a['time'] = end_time
            else:
                a == 'null'
            data[path_leaf(filename)] = a

    listData = collections.OrderedDict()
    listStatictis = collections.OrderedDict()
    #pdb.set_trace()
    percentDat = float(countDat) / float (countIsDone) * 100.0
    percentSin = float(countSin) / float (countIsDone) * 100.0
    percentRaw = float(countRaw) / float (countIsDone) * 100.0
    percentImg = 100.0 - percentDat - percentSin - percentRaw
    percentDone = float(countIsDone) / float (countComplete) * 100.0
    percentComplete = float(countComplete) / float (countTotal) * 100.0
    listStatictis['total'] = countTotal
    listStatictis['complete'] = {'total':countComplete, 'percent': percentComplete}
    listStatictis['done'] = {'total':countIsDone, 'percent': percentDone}
    listStatictis['dat'] = {'total':countDat, 'percent': percentDat}
    listStatictis['ftf'] = {'total':countSin, 'percent': percentSin}
    listStatictis['raw'] = {'total':countRaw, 'percent': percentRaw}
    listStatictis['image'] = {'total':countImg, 'percent': percentImg}
    listData['statictis'] = listStatictis
    listData['data'] = data

    with io.open('report.json', 'w',encoding="utf-8") as outfile:
        outfile.write(unicode((json.dumps(listData, sort_keys=False))))
    os.system('mkdir -p root')
    for dirname, dirnames, filenames in os.walk('./'):
        # print path to all filenames.
        for filename in filenames:
            checkfile = 'framework.jar'
            if(checkfile == filename):
                tmp = './root' + dirname[1:] + '.jar'
                os.system('cp -r '+ os.path.join(dirname, filename)+ ' ' + tmp)
            
    
    """
    b = extractor(argv[2])

    #a='framework_2016-12-19_18-37-51' ############
    #b='framework_2016-12-19_18-38-00'###########
    aa = getfilename(a)
    bb = getfilename(b)
    aaa = []
    bbb = []
    #print aa,'\n\n',bb############
    a1 = aa[0].split('/',1)[0] + '/'
    #print a1#################
    for i in range(len(aa)):
        tmp = aa[i].split('/',1)[1]
        aaa.append(tmp)
    b1 = bb[0].split('/',1)[0] + '/'
    #print b1################
    for i in range(len(bb)):
        tmp = bb[i].split('/',1)[1]
        bbb.append(tmp)
    #print aaa,'\n\n',bbb###############

    file_to_compare = []
    file_to_check = []
    for i in range(len(bbb)):
        try:
            aaa.index(bbb[i])
            file_to_compare.append(bbb[i])
        except:
            file_to_check.append(bbb[i])
    #print file_to_compare,'\n\n',file_to_check##############
    #print len(file_to_check), len(file_to_compare)
    #return 0


    for i in range(len(file_to_compare)):
        try:
            tmp2 = 'python androsim.py -i ' + a1 + file_to_compare[i] + ' ' + b1 + file_to_compare[i] + ' -c ZLIB -p'
            os.system(tmp2)
        except:
            print 'Error: ' + file_to_compare[i]

    for i in range(len(file_to_check)):
        try:
            dump2(b1 + file_to_check[i])
        except:
            print 'Error: ' + file_to_check[i]            
    """




if __name__ == '__main__':
    main(sys.argv)
