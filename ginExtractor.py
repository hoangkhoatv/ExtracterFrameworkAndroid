import ginlib
import sys
import zipfile
from unrar import rarfile


def extractor(romfile):
    framework = 0
    list = {}
    print 'Checking ROM type...'
    lena = len(romfile)
    extension = romfile[lena-3:lena]
    print 'ROM type:', extension
    stt = ''
    _type = ''
    if extension == 'ftf':
        framework = ginlib.sin(romfile)
        stt = 'complete'
        _type = 'sin'
    elif extension == 'zip':
        stt = 'complete'
        z = zipfile.ZipFile(romfile)
        dir1 = 'system/framework/framework-res.apk'
        dir2 = 'system.new.dat'
        lst = []
        for i in range(len(z.namelist())):
            t = str(z.namelist()[i])
            lst.append(t)
        if dir1 in lst:
            framework = ginlib.raw(romfile)
            _type = 'raw'
        elif dir2 in lst:
            framework = ginlib.dat(romfile)
            _type = 'dat'
        else:
            print "Unsupported ROM..."
            stt = 'Unsupported'
    elif extension == 'rar':
        stt = 'complete'
        z = rarfile.RarFile(romfile)
        dir1 = 'system/framework/framework-res.apk'
        dir2 = 'system.new.dat'
        lst = []
        for i in range(len(z.namelist())):
            t = str(z.namelist()[i])
            lst.append(t)
        if dir1 in lst:
            print "RAW ROM..."
            framework = ginlib.raw(romfile)
            _type = 'raw'
        elif dir2 in lst:
            print "DAT ROM..."
            framework = ginlib.dat(romfile)
            _type = 'dat'
        else:
            print "Unsupported ROM..."
            stt = 'Unsupported'
    else:
        print 'Unsupported ROM.'
        stt = 'Unsupported'

    list['type'] = _type
    list['extension'] = extension
    list['status'] = stt
    list['size'] = framework

    return list
