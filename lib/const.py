SecurityCheck = {
    'S01': ['Superuser.apk', 'Superuser_Pro.apk', 'bootanimation.zip', 'bootanimation'],
    'S02': ['build.prop'],
    'S03': ['default.prop'],
    'S04': ['default.prop'],
    'S05': ['system'],
    'S06': ['hosts']
}

# ro.secure=0: root mode
# ro.debuggable=0: usb debugging disable

VariableCheck = {
    'S01': [],
    'S02': 'service.adb.tcp.port=3355',
    'S03': 'ro.debuggable=1',
    'S04': 'ro.secure=0',
    'S06': '127.0.0.1'
}

ReverseCode = {
    'S01': 'Su access',
    'S02': 'ADB shell over wifi',
    'S03': 'USB Debugging enabled',
    'S04': 'ADB shell root mode',
    'S05': 'System folder Read Only',
    'S06': 'Suspicious  IP'
}

db_url = 'mongodb://localhost:27017'
