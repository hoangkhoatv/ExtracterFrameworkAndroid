import zipfile
import os.path
import os
import ntpath, pdb
import re
from subprocess import call
from time import gmtime, strftime
import rarfile
import tarfile
import platform
import subprocess
import hashlib
import config
from androidobject import AndroidObject
def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)
import capstone

def sin(rom):
    print 'Please wait...\nGetting system.sin from ROM...'
    foldersin = 'system.sin' + rom.replace('/','.')
    foldersin = re.sub( '\s+', '', foldersin ).strip()
    foldersin = config.tempFolder + foldersin
    if os.path.exists(foldersin):
        os.system('rm -rf ' + foldersin)
    with zipfile.ZipFile(rom,"r") as zip_ref:
        zip_ref.extract('system.sin', foldersin)
    print foldersin
    print 'GET system.sin SUCCESSFULLY.\nGetting system.ext4 from system.sin...'
    call(["java","-jar","sin2ext4.jar",foldersin+"/system.sin"])
    print 'GET system.ext4 SUCCESSFULLY.'
    print 'Mounting system.ext4...'
    tmp = 'system' + rom.replace('/','.')
    tmp = re.sub( '\s+', '', tmp ).strip()
    tmpMount = config.tempFolder + 'mount' +tmp
    tmp = config.tempFolder + tmp
    os.makedirs(tmpMount)
    call("sudo mount -t ext4 " + foldersin + "/system.ext4 " +tmpMount,shell=True)
    call('sudo cp -rf ' + tmpMount +' '+ tmp,shell=True)
    print 'MOUNT system.ext4 SUCCESSFULLY.\nGetting /system/framework...'
    print 'Deodex .jar .apk....'
     # process framework
    defaultConfiguation = capstone.getDefaultConfiguation(config.tempFolder)
    sdk, version = get_sdk_version_android(tmp)
    output = deodexJar(sdk,tmp,rom)
    copyFramework(tmp,output)
    # process apk
    deodexApk(tmp + '/app')
    listApk = getApk(tmp + '/app')
    copyApk(listApk,output)

    call(["sudo", "umount",tmpMount])
    # remove temp folder
    os.system('rm -rf ' + config.tempFolder +'/*')

    size = 0
    checkFile = os.path.isfile(output + '/framework.jar')
    if checkFile:
        size = os.path.getsize(output + '/framework.jar')
    return size,output,sdk,version,defaultConfiguation 


def dat(rom):
    print 'Please wait...\nGetting system.transfer.list and system.new.dat from ROM...'
    folderdat = 'system.dat' + rom.replace('/','.')
    folderdat = re.sub( '\s+', '', folderdat ).strip()
    folderdat = config.tempFolder + folderdat
    if os.path.exists(folderdat):
        os.system('rm -rf ' + folderdat)
    with zipfile.ZipFile(rom,"r") as zip_ref:
        zip_ref.extract('system.new.dat', folderdat)
        zip_ref.extract('system.transfer.list', folderdat)
    print 'GET system.transfer.list AND system.new.dat SUCCESSFULLY.\nGetting system.img...'
    call(["python", "./sdat2img.py", folderdat + "/system.transfer.list", folderdat + "/system.new.dat", folderdat + "/system.img"])
    print 'GET system.img SUCCESSFULLY.'
    print 'Mounting system.img...'
    tmp = 'system' + rom.replace('/','.')
    tmp = re.sub( '\s+', '', tmp ).strip()
    tmpMount = config.tempFolder + 'mount' +tmp
    tmp = config.tempFolder + tmp
    os.makedirs(tmpMount)
    linkMount = folderdat + '/system.img'
    call(["sudo","mount",linkMount,tmpMount])
    call('sudo cp -rf ' + tmpMount +' '+ tmp,shell=True)
    print 'MOUNT system.img SUCCESSFULLY.\nGetting /system/framework...'

    print 'Deodex .jar .apk....'
    # process framework
    defaultConfiguation  = capstone.getDefaultConfiguation(config.tempFolder)
    sdk, version = get_sdk_version_android(tmp)
    output = deodexJar(sdk,tmp,rom)
    framework = copyFramework(tmp,output)

    # process apk
    deodexApk(tmp + '/app')
    listApk = getApk(tmp + '/app')
    apks = copyApk(listApk,output)

    call(["sudo", "umount",tmpMount])
    # remove temp folder
    os.system('rm -rf ' + config.tempFolder +'/*')

    return framework,apks,output,sdk,version,defaultConfiguation 

def raw(rom):
    print 'Please wait...\nExtracting ROM RAW'
    folderraw = 'system.raw' + rom.replace('/','.')
    folderraw = re.sub( '\s+', '', folderraw ).strip()
    folderraw = config.tempFolder + folderraw
    if os.path.exists(folderraw):
        os.system('rm -rf ' + folderraw)
   
    with zipfile.ZipFile(rom,"r") as zip_ref:
        zip_ref.extractall(folderraw)
    print 'EXTRACT ROM SUCCESSFULLY'
    print 'Deodex .jar .apk....'
    # process framework
    tmp = folderraw + "/system"
    print tmp
    defaultConfiguation  = capstone.getDefaultConfiguation(config.tempFolder)
    sdk, version = get_sdk_version_android(tmp)
    output = deodexJar(sdk,tmp,rom)
    framework = copyFramework(tmp,output)
    # process apk
    deodexApk(tmp + '/app')
    listApk = getApk(tmp + '/app')
    apks = copyApk(listApk,output)
    # remove temp folder
    os.system('rm -rf ' + config.tempFolder +'/*')
    return framework,apks,output,sdk,version,defaultConfiguation 

def image(rom):
    print 'Please wait...\nExtracting ROM...'
    folderimage = 'system.img' + rom.replace('/','.')
    folderimage = re.sub( '\s+', '', folderimage ).strip()
    folderimage = config.tempFolder + folderimage
    if os.path.exists(folderimage):
            os.system('rm -rf ' + folderimage)
    tmp = 'ROM' + rom.replace('/','.')
    tmp = re.sub( '\s+', '', tmp ).strip()
    tmp = config.tempFolder + tmp
    file_name, file_extension = os.path.splitext(rom)
    if file_extension == '.zip':
        with zipfile.ZipFile(rom,'r') as zip_ref:
            file_data = find_data_zip(zip_ref,'system.img')
            zip_ref.extract(file_data, folderimage)
    elif file_extension == '.rar':
        rar = rarfile.RarFile(rom,'r')
        file_data = find_data_rar(rar,'system.img')
        rar.extract(file_data, folderimage)
    elif file_extension == '.gz':
        with tarfile.TarFile(rom,'r') as tar_ref:
            tar_ref.extract(find_data_tar(tar_ref,'system.img'), folderimage)
    print 'GET system.img SUCCESSFULLY.\nGetting system.img...'
    #Convert img format android to ext4
    call(["simg2img",folderimage+'/'+file_data,folderimage+'/system.raw.img'])
    print 'CONVERTED system.img SUCCESSFULLY.\nGetting system.raw.img...'
    print 'Mounting system.raw.img...'
    tmp = 'system' + rom.replace('/','.')
    tmp = re.sub( '\s+', '', tmp ).strip()
    tmpMount = config.tempFolder + 'mount' +tmp
    tmp = config.tempFolder + tmp
    os.makedirs(tmpMount)
    linkMount = folderimage + '/system.raw.img'
    call(["sudo","mount",linkMount,tmpMount])
    call('sudo cp -rf ' + tmpMount +' '+ tmp,shell=True)

    print 'MOUNT system.raw.img SUCCESSFULLY.\nGetting /system/framework...'
    print 'Deodex .jar .apk....'
    # process framework
    defaultConfiguation = capstone.getDefaultConfiguation(config.tempFolder)
    sdk, version = get_sdk_version_android(tmp)
    output = deodexJar(sdk,tmp,rom)
    copyFramework(tmp,output)

    # process apk
    deodexApk(tmp + '/app')
    listApk = getApk(tmp + '/app')
    copyApk(listApk,output)

    call(["sudo", "umount",tmpMount])
    # remove temp folder
    os.system('rm -rf ' + config.tempFolder +'/*')

    size = 0
    checkFile = os.path.isfile(output + '/framework.jar')
    if checkFile:
        size = os.path.getsize(output + '/framework.jar')
    return size,output,sdk,version,defaultConfiguation

def device(rom,sdk):
    print 'Deodex .jar .apk....'
    # process framework
    tmp = rom+ "/system"
    output = deodexJar(sdk,tmp,rom)
    framework = copyFramework(tmp,output)
    # process apk
    deodexApk(tmp + '/app')
    listApk = getApk(tmp + '/app')
    apks = copyApk(listApk,output)
    # remove temp folder
    os.system('rm -rf ' + config.tempFolder +'/*')
    return framework,apks,output

def get_sdk_version_android(members):
    checkfile = 'build.prop'
    for dirname, dirnames, filenames in os.walk(members):
        for filename in filenames:
            if(checkfile == filename):
                path = os.path.join(dirname, filename)
                command = "cat " + path
                all_info = subprocess.check_output(command, shell=True).strip()
                for line1 in all_info.split("\n"):
                    if "ro.build.version.sdk" in line1:
                        sdk = re.sub("ro.build.version.sdk=", "",line1,1)
                        for line2 in all_info.split("\n"):
                            if "ro.build.version.release" in line2:
                                version = re.sub("ro.build.version.release=", "",line2,1)
                                return sdk,version
    return None,None

def get_sdk_version_brand_android(members):
    checkfile = 'build.prop'
    for dirname, dirnames, filenames in os.walk(members):
        for filename in filenames:
            if(checkfile == filename):
                path = os.path.join(dirname, filename)
                command = "cat " + path
                all_info = subprocess.check_output(command, shell=True).strip()
                for line1 in all_info.split("\n"):
                    if "ro.build.version.sdk" in line1:
                        sdk = re.sub("ro.build.version.sdk=", "",line1,1)
                        for line2 in all_info.split("\n"):
                            if "ro.build.version.release" in line2:
                                version = re.sub("ro.build.version.release=", "",line2,1)
                                for line3 in all_info.split("\n"):
                                    if "ro.product.brand" in line3:
                                        brand = re.sub("ro.product.brand=", "",line3,1)
                                        return sdk,version,brand
    return None,None,None

def find_data_tar(members,path):
    for member in members.getnames():
        if (path_leaf(str(member)) == path):
           return str(member)
    return None

def find_data_zip(members,path):
    for member in members.namelist():
        if (path_leaf(str(member)) == path):
           return str(member)
    return None

def find_data_rar(members,path):
    for member in members.namelist():
        if (path_leaf(str(member)) == path):
           return str(member)
    return None

def getHash(url):
    BLOCKSIZE = 65536
    hasher = hashlib.sha256()
    with open(url, 'rb') as afile:
        buf = afile.read(BLOCKSIZE)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(BLOCKSIZE)
    return hasher.hexdigest()
def deodexApk(path):
    listApk = getApk(path)
    command = "python odex2apk.py"
    for url in listApk:
         command = "python odex2apk.py " + url
         call(command,shell=True)

def deodexJar(sdk,path,rom):
    sdk = int (sdk)
    if sdk == 21 or sdk == 22 :
            call('sudo java -jar oat2dex_v0.86.jar -o '+ config.tempFolder + ' devfw '+ path + '/framework/',shell=True)
    elif sdk >= 23:
            call('sudo java -jar oat2dex.jar -o '+ config.tempFolder + ' devfw '+ path + '/framework/',shell=True)
    output = 'framework_' + path_leaf(rom)  + '_' +  strftime('%Y-%m-%d_%H-%M-%S', gmtime())
    output = re.sub( '\s+', '', output ).strip()
    output = config.outFolder + output
    os.makedirs(output)
    return output

def getApk(path):
    listApk = []
    for root, dirs, files in os.walk(path):
        for filename in files:
            extension = os.path.splitext(filename)[1]
            if extension == '.apk':
                url = os.path.join(root, filename)
                listApk.append(url)
    return listApk

def copyApk(listApk,output):
    listObjApk = []
    for apk in listApk:
        objApk = AndroidObject()
        call('cp -r '+apk+' ' + output, shell=True)
        objApk.name = path_leaf(apk)
        objApk.size =  os.path.getsize(apk)
        objApk.hash = getHash(apk)
        listObjApk.append(objApk.__dict__)
    print 'GET /system/app SUCCESSFULLY.'
    return listObjApk

def copyFramework(tmp,output):
    checkFile = os.path.isfile(config.tempFolder + 'boot-jar-result/framework.jar')
    if checkFile:
            tmp1 = config.tempFolder + 'boot-jar-result/framework.jar'
    else:
        tmp1 = tmp + '/framework/framework.jar'
        if (os.path.isfile(config.tempFolder + 'boot-jar-with-dex/framework.jar')):
            tmp1 = config.tempFolder + 'boot-jar-with-dex/framework.jar'
    call('cp -r '+tmp1+' ' +output+'/framework.jar', shell=True)
    size = 0
    checkFile = os.path.isfile(output + '/framework.jar')
    framework = AndroidObject()
    if checkFile:
        size = os.path.getsize(output + '/framework.jar')
        framework.name = 'framework.jar'
        framework.size = size
        framework.hash = getHash(output + '/framework.jar')
    print 'GET /system/framework SUCCESSFULLY.'
    return framework


