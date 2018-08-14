import os
import mmap
pathTo =  'D:\FUN_GAME\NAM_4\capstone_project\capstone-project\\testFolder\\text.txt'
#
# for root, dirs, files in os.walk(pathTo):
#     for dir in dirs:
#         print pathTo + dir
#
# def GetHashofDirs(directory, verbose=0):
#   import hashlib, os
#   SHAhash = hashlib.sha1()
#   if not os.path.exists (directory):
#     return -1
#
#   try:
#     for root, dirs, files in os.walk(directory):
#       for names in files:
#         if verbose == 1:
#           print 'Hashing', names
#         filepath = os.path.join(root,names)
#         try:
#           f1 = open(filepath, 'rb')
#         except:
#           # You can't open the file for some reason
#           f1.close()
#           continue
#
# 	while 1:
# 	  # Read file in as little chunks
#   	  buf = f1.read(4096)
# 	  if not buf : break
# 	  SHAhash.update(hashlib.sha1(buf).hexdigest())
#         f1.close()
#
#   except:
#     import traceback
#     # Print the stack traceback
#     traceback.print_exc()
#     return -2
#
#   return SHAhash.hexdigest()
#
# print GetHashofDirs('D:\FUN_GAME\NAM_4\capstone_project\capstone-project\\testFolder', 1)
# spec_char = ['\a', '\b', '\f', '\n', '\r', '\t', '\v']
# clear_char = ['\\a', '\\b', '\\f', '\\n', '\\r', '\\t', '   \\v']
# path = pathTo
# for i in range(0, len(spec_char)):
#     if spec_char[i] in params.path:
#         path = path(spec_char[i], clear_char[i])
#
# path = path + '\\'
#
# print path
#
# for dir in os.listdir(get_clearPath(params)):
#     if not os.path.isfile(rootDir + dir):
#         listDirs.append(dir)


# f = open(pathTo)
# s = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
# if s.find('service.adb.tcp.port=3355') != -1:
#     print 'WARNING'
# else:
#     print 'OK'
with open(pathTo) as f:
    content = f.readlines()
    # print content
# you may also want to remove whitespace characters like `\n` at the end of each line
print content
result = []
for x in content:
    print x.strip().split(' ')
    result.append(x.strip().split(' '))
print result[0][0].split('\t')[0]
print result[0][len(result[0]) - 1]
# result[0].s
