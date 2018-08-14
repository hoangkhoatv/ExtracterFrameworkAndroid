#!/usr/bin/python
#Evaluate Security: Firmware Android
#This tool will check:
# Su access
# Usb debugging
# USB Debugging enabled
# ADB shell root mode
# ADB shell over wif

__version__ = "0.1"
__author__ = "Trinh Le - Si Tuan"

from lib import core

from optparse import OptionParser
import sys
import json
def getDefaultConfiguation(params):
    core.scan_allFolder(params)
    core.get_existdb()
    core.check_sec()
    core.gen_resultList()
    core.check_s03()
    core.check_s04()
    core.check_s02()
    core.check_s01()
    core.check_s05()
    core.check_s06()
    return core.getJson(params)
    # core.printResult(params)

# def parse_args():

#     parser = OptionParser(usage="usage: %prog [options] filename", version='{0}: v.{1}'.format('%prog', __version__))
#     parser.add_option("-p", "--path", dest="path", help="Specify path to folder", type="string", default="E:\android\android")
#     parser.add_option("-o", "--output", dest="output", help="Specify path to output folder", type="string", default="E:\android\android")
#     (options, args) = parser.parse_args(sys.argv)

#     if len(args) != 1:
#         parser.error("Wrong number of arguments")

#     return options, args

