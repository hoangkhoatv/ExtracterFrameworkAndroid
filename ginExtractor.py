import ginlib
import sys
import zipfile
#from unrar import rarfile


def extractor(romfile):
    framework = 0
    mList = {}
    print 'Checking ROM type...'
    lena = len(romfile)
    extension = romfile[lena-3:lena]
    print 'ROM type:', extension
    stt = 'Unsupported'
    _type = ''
    if extension == 'ftf':
        stt = 'complete'
        _type = 'sin'
        framework = ginlib.sin(romfile)
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
            _type = 'raw'
            framework = ginlib.raw(romfile)
        elif dir2 in lst:
            _type = 'dat'
            framework = ginlib.dat(romfile)
        else:
            print "Unsupported ROM..."
            stt = 'Unsupported'

    mList['type'] = _type
    mList['extension'] = extension
    mList['status'] = stt
    mList['size'] = framework
    checkDone = int (framework)
    if checkDone < 1000000:
        mList['isDone'] = False
    else:
        mList['isDone'] = True

    return mList
