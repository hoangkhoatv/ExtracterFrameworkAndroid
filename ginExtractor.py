import ginlib
import sys
import zipfile
import rarfile
import tarfile
import os
import collections
from rom import Rom
from androidobject import AndroidObject
def extractor(romfile):
    iRom = Rom()
    framework = AndroidObject()
    apks = []
    print 'Checking ROM type...'
    lena = len(romfile)
    iRom.extention = romfile[lena-3:lena]
    print 'ROM type:', iRom.getExt()
    iRom.stt = 'Unsupported'

    if iRom.extention == 'ftf':
        iRom.stt = 'complete'
        iRom.typeFile = 'ftf'
        framework,apks,iRom.outFile,iRom.sdk,iRom.version = ginlib.sin(romfile)
    elif iRom.extention == 'rar':
        file_rar = rarfile.RarFile(romfile)
        isData = ginlib.find_data_rar(file_rar,'system.img')
        if isData != None:
            iRom.typeFile = 'img'
            iRom.stt  = 'complete'
            framework,apks,iRom.outFile,iRom.sdk,iRom.version  = ginlib.image(romfile)
        else:
                print "Unsupported ROM..."
                iRom.stt  = 'Unsupported'
    elif iRom.extention == 'zip':
        #pdb.set_trace()
        file_zip = zipfile.ZipFile(romfile)
        isData = ginlib.find_data_zip(file_zip,'system.img')
        if isData != None:
            iRom.stt = 'complete'
            iRom.typeFile = 'img'
            framework,apks,iRom.outFile,iRom.sdk,iRom.version  = ginlib.image(romfile)
        else:
            if ginlib.find_data_zip(file_zip,'framework-res.apk') != None:
                iRom.typeFile = 'raw'
                iRom.stt = 'complete'
                framework,apks,iRom.outFile,iRom.sdk,iRom.version = ginlib.raw(romfile)
            elif ginlib.find_data_zip(file_zip,'system.new.dat') != None:
                iRom.typeFile= 'dat'
                iRom.stt = 'complete'
                framework,apks,iRom.outFile,iRom.sdk,iRom.version = ginlib.dat(romfile)
            else:
                print "Unsupported ROM..."
                iRom.stt = 'Unsupported'
    elif iRom.extention == 'gz':
        file_tar = tarfile.TarFile(romfile)
        isData = ginlib.find_data_tar(file_tar,'system.img')
        if isData != None:
            iRom.typeFile = 'img'
            iRom.stt = 'complete'
            framework,apks,iRom.outFile,iRom.sdk,iRom.version  = ginlib.image(romfile)
        else:
                print "Unsupported ROM..."
                iRom.stt = 'Unsupported'


    iRom.size= os.path.getsize(romfile)
    iRom.hash = ginlib.getHash(romfile)
    iRom.framework = framework.__dict__
    iRom.listApk = apks
    return iRom
