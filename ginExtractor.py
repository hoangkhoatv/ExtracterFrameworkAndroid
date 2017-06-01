import ginlib
import sys
import zipfile
from unrar import rarfile
import tarfile
import pdb
import collections
#from unrar import rarfile


def extractor(romfile):
    framework = 0
    outFilename = None
    sdk = None
    version = None
    mList = collections.OrderedDict()
    print 'Checking ROM type...'
    lena = len(romfile)
    extension = romfile[lena-3:lena]
    print 'ROM type:', extension
    stt = 'Unsupported'
    _type = ''
    if extension == 'ftf':
        stt = 'complete'
        _type = 'ftf'
        framework,outFilename,sdk,version = ginlib.sin(romfile)
    elif extension == 'rar':
        file_rar = rarfile.RarFile(romfile)
        isData = ginlib.find_data_rar(file_rar,'system.img')
        if isData != None:
            _type = 'img'
            stt = 'complete'
            framework,outFilename,sdk,version = ginlib.image(romfile)
        else:
                print "Unsupported ROM..."
                stt = 'Unsupported'
    elif extension == 'zip':
        #pdb.set_trace()
        file_zip = zipfile.ZipFile(romfile)
        isData = ginlib.find_data_zip(file_zip,'system.img')
        if isData != None:
            stt = 'complete'
            _type = 'img'
            framework,outFilename,sdk,version = ginlib.image(romfile)
        else:
            if ginlib.find_data_zip(file_zip,'framework-res.apk') != None:
                _type = 'raw'
                stt = 'complete'
                framework,outFilename,sdk,version = ginlib.raw(romfile)
            elif ginlib.find_data_zip(file_zip,'system.new.dat') != None:
                _type = 'dat'
                stt = 'complete'
                framework,outFilename,sdk,version= ginlib.dat(romfile)
            else:
                print "Unsupported ROM..."
                stt = 'Unsupported'
    elif extension == 'gz':
        file_tar = tarfile.TarFile(romfile)
        isData = ginlib.find_data_tar(file_tar,'system.img')
        if isData != None:
            _type = 'img'
            stt = 'complete'
            framework,outFilename,sdk,version = ginlib.image(romfile)
        else:
                print "Unsupported ROM..."
                stt = 'Unsupported'

    mList['type'] = _type
    mList['extension'] = extension
    mList['status'] = stt
    mList['file name'] = outFilename
    mList['size'] = framework
    mList['sdk'] = sdk
    mList['android version']= version
    checkDone = int (framework)
    if checkDone < 1000000:
        mList['isDone'] = False
    else:
        mList['isDone'] = True

    return mList
