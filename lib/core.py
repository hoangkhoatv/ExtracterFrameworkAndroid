import os
import mmap
import platform
from prettytable import PrettyTable
from pymongo import MongoClient

import utility
import const
import db

rootDir = ''
spl = ''
scannedList = []
listDirs = []
out = []
haLst = []
existDbList = []

collection = db.conn_db()

def get_clearPath(params):
    spec_char = ['\a', '\b', '\f', '\n', '\r', '\t', '\v']
    clear_char = ['\\a', '\\b', '\\f', '\\n', '\\r', '\\t', '   \\v']
    path = params
    for i in range(0, len(spec_char)):
        if spec_char[i] in params:
            path = path.replace(spec_char[i], clear_char[i])

    return path

def scan_allFolder(params):

    global spl
    spl = '\\'
    if platform.system() != 'Windows':
        spl = '//'
    global rootDir
    rootDir = get_clearPath(params) + spl

    # Get list folder
    for dir in os.listdir(get_clearPath(params)):
        if not os.path.isfile(rootDir + dir):
            listDirs.append(dir)
    # print listDirs

def get_existdb():

    rmove = []
    global haLst
    global existDbList

    for dir in listDirs:
        hashdir = utility.GetHashofDirs(rootDir + dir)
        haLst.append(hashdir)

    # cursor = collection.find({})
    result = []
    # for item in cursor:
    #     haLst.append(item['hash'].strip().encode('utf-8'))

    # print listDirs
    # print haLst
    for hsh in range(0, len(haLst)):
        result = db.get_firmware_by_hash({
            'collection': collection,
            'hash': haLst[hsh]
        })
        if result:
            rmove.append({
                'hash': haLst[hsh],
                'name': listDirs[hsh]
            })
            existDbList.append({
                'name': result['name'].strip(),
                'hash': result['hash'].strip(),
                's01': result['s01'].strip(),
                's02': result['s02'].strip(),
                's03': result['s03'].strip(),
                's04': result['s04'].strip(),
                's05': result['s05'].strip(),
                's06': result['s06']
            })

    if rmove != []:
        for i in rmove:
            listDirs.remove(i['name'])
            haLst.remove(i['hash'])
    # print listDirs
    # print haLst

def check_sec():

    index = 0
    for dir in listDirs:
        scannedDict = {
            'S01': [],
            'S02': [],
            'S03': [],
            'S04': [],
            'S05': [],
            'S06': []
        }
        scannedList.append(scannedDict)
        for root, dirs, files in os.walk(rootDir + dir, topdown=False):
            #Get folder path
            for name in dirs:
                if name in const.SecurityCheck['S05'] and const.SecurityCheck['S05'] != []:
                    scannedList[index]['S05'].append(os.path.join(root,name))

            # Get path file
            for name in files:
                path = os.path.join(root, name)
                # print path
                if name in const.SecurityCheck['S01'] and const.SecurityCheck['S01'] != []:
                    scannedList[index]['S01'].append(path)
                if name in const.SecurityCheck['S02'] and const.SecurityCheck['S02'] != []:
                    scannedList[index]['S02'].append(path)
                if name in const.SecurityCheck['S03'] and const.SecurityCheck['S03'] != []:
                    scannedList[index]['S03'].append(path)
                if name in const.SecurityCheck['S04'] and const.SecurityCheck['S04'] != []:
                    scannedList[index]['S04'].append(path)
                if name in const.SecurityCheck['S06'] and const.SecurityCheck['S06'] != []:
                    scannedList[index]['S06'].append(path)
        index += 1
    # print scannedList

def gen_resultList():
    for i in range(0, len(listDirs)):
        out.append({
        'S01': 'UNKOWN',
        'S02': 'UNKOWN',
        'S03': 'UNKOWN',
        'S04': 'UNKOWN',
        'S05': 'OK',
        'S06': ['OK', '', '']
    })

def check_s04():

    index = 0
    for scanned in scannedList:
        pathToFile = scanned['S04']
        try:
            f = open(pathToFile[0])
            s = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)

            if s.find('ro.secure=0') != -1:
                out[index]['S04'] = 'WARNING'
            elif s.find('ro.secure=1') != -1:
                out[index].update({'S04': 'OK'})
            index += 1
        except IndexError:
            out[index]['S04'] = 'Missing file default.prop'
            index += 1
            continue

    # print out

def check_s03():

    index = 0
    for scanned in scannedList:
        pathToFile = scanned['S03']
        try:
            f = open(pathToFile[0])
            s = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)

            if s.find('ro.debuggable=1') != -1:
                out[index]['S03'] = 'WARNING'
            elif s.find('ro.debuggable=0') != -1:
                out[index].update({'S03': 'OK'})
            index += 1
        except IndexError:
            out[index]['S03'] = 'Missing file default.prop'
            index += 1
            continue

    # print out

def check_s02():

    index = 0
    for scanned in scannedList:
        pathToFile = scanned['S02']
        try:
            f = open(pathToFile[0])
            s = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)

            if s.find('service.adb.tcp.port=3355') != -1:
                out[index]['S02'] = 'WARNING'
            else:
                out[index].update({'S02': 'OK'})
            index += 1
        except IndexError:
            out[index]['S02'] = 'Missing file build.prop'
            index += 1
            continue

def check_s01():

    index = 0
    for scanned in scannedList:
        pathToFile = scanned['S01']
        if pathToFile != []:
            out[index]['S01'] = 'WARNING'
        else:
            out[index].update({'S01': 'OK'})
        index += 1

def check_s05():

    index = 0
    for scanned in scannedList:
        pathToFile = scanned['S05']
        if pathToFile != []:
            for i in range(0,len(pathToFile))   :
                if os.access(pathToFile[i], os.W_OK):
                    if i == 0:
                        if 'ramdisk' in pathToFile[i]:
                            out[index]['S05'] = 'WARNING - ramdisk'
                        else:
                            out[index]['S05'] = 'WARNING - system'
                    else:
                        if 'ramdisk' in pathToFile[i]:
                            out[index]['S05'] += ', WARNING - ramdisk'
                        else:
                            out[index]['S05'] += ', WARNING - system'

            index += 1
        else:
            out[index]['S05'] = 'Missing folder system'
            index += 1
            continue

def check_s06():

    index = 0
    for scanned in scannedList:
        hosts = []
        pathToFile = scanned['S06']
        try:
            with open(pathToFile[0]) as f:
                content = f.readlines()
            for x in content:
                # print x.strip().split(' ')
                hosts.append(x.strip().split(' '))

            for host in hosts:
                if '127.0.0.1' not in host[0] and '::1' not in host[0] and '#' not in host[0] and host[0] != '':
                    domain = host[len(host) - 1]
                    ip = host[0]
                    if '\t' in host:
                        ip = host[0].split('\t')[0]

                    out[index]['S06'][1] += ip + ' '
                    out[index]['S06'][2] += domain + ' '
                    out[index]['S06'][0] = '\x1b[31mWARNING\x1b[0m'

            index += 1
        except IndexError:
            out[index]['S06'][0] = 'Missing file hosts'
            index += 1
            continue
        finally:
            f.close()

def asign_color():
    for result in out:
        for code in result:
            if result[code] == 'OK':
                result[code] = '\x1b[32mOK\x1b[0m'
            if 'WARNING' in result[code]:
                result[code] = '\x1b[31m' + result[code] + '\x1b[0m'

def write_result_file(params):
    path = params[0] + spl
    try:
        with open (path + params[1]['name'] + '.txt', 'wb') as f:
            f.write('------EVALUATE SECURITY FIRMWARE ANDROID-----\n')
            f.write('------------------DETAIL---------------------\n')
            f.write('Name: ' + params[1]['name'] + '\n')
            f.write('Su Access: ' + params[1]['s01'] + '\n')
            f.write('ADB shell over wifi: ' + params[1]['s02'] + '\n')
            f.write('USB Debugging: ' + params[1]['s03'] + '\n')
            f.write('ADB shell root mode: ' + params[1]['s04'] + '\n')
            f.write('System folder RO: ' + params[1]['s05'] + '\n')
            f.write('Suspicious IP: ' + params[1]['s06'][0] + '\n')
            f.write(params[1]['s06'][1].strip() + '\t' + params[1]['s06'][2].strip() + '\n')
    except (IOError, OSError) as e:
        print "Cant write output"

def get_all_hash():
    output = db.get_all_hash({
        'collection': collection
    })
    # print output
def getJson(params):
    res = {}
    if listDirs != []:
        i = 0
        for dir in listDirs:
            record = {
                'name':dir,
                'hash':haLst[i],
                's01':out[i]['S01'],
                's02':out[i]['S02'],
                's03':out[i]['S03'],
                's04':out[i]['S04'],
                's05':out[i]['S05'],
                's06':out[i]['S06']
            }
            db.insert_record([collection, record])
            temp = {}
            temp['name'] = dir
            temp['s01'] = out[i]['S01']
            temp['s02'] = out[i]['S02']
            temp['s03'] = out[i]['S03']
            temp['s04'] = out[i]['S04']
            temp['s05'] = out[i]['S05']
            temp['s06'] = out[i]['S06'][0]
            res = temp 
            i += 1
    if existDbList != []:
        for esdb in existDbList:
            temp = {}
            temp['name'] = esdb['name']
            temp['s01'] = esdb['s01']
            temp['s02'] = esdb['s02']
            temp['s03'] = esdb['s03']
            temp['s04'] = esdb['s04']
            temp['s05'] = esdb['s05']
            temp['s06'] = esdb['s06'][0]
            res = temp 
    return res

def printResult(params):


    t = PrettyTable(['Name', 'Su Access','ADB shell over wifi', 'USB Debugging', 'ADB shell root mode', 'System folder RO', 'Suspicious IP'])

    if listDirs != []:
        i = 0
        for dir in listDirs:
            record = {
                'name':dir,
                'hash':haLst[i],
                's01':out[i]['S01'],
                's02':out[i]['S02'],
                's03':out[i]['S03'],
                's04':out[i]['S04'],
                's05':out[i]['S05'],
                's06':out[i]['S06']
            }
            db.insert_record([collection, record])
            t.add_row([dir, out[i]['S01'], out[i]['S02'], out[i]['S03'], out[i]['S04'], out[i]['S05'], out[i]['S06'][0]])
            write_result_file([params.output, record])
            i += 1

    if existDbList != []:

        for esdb in existDbList:
            t.add_row([esdb['name'], esdb['s01'], esdb['s02'], esdb['s03'], esdb['s04'], esdb['s05'], esdb['s06'][0].strip()])
            write_result_file([params.output, esdb])

    print t


