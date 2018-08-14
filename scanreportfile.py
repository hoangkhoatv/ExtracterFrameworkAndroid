#!/usr/bin/python

import requests, sys, os.path, json, ast, re, hashlib
import pdb,time
import random

API_KEY = [
	'5ab337998029226c90b6a99ac42a48e09ba1b2f44d30ba35e67834f4c108e04b',
	'e5b4f1779f756992a5e10ba710e415c2f154c34dc76694bdf17ac03a0cccf83d',
	'eeef5bfb338a631dc0a7ff55a15d2c9f0d3b61a491e95188750a2bf982828252',
	'9e68bff1dc60384a01a81b6acebe0e5279cf4b29d24b3ae994afe01e0ab9fa21',
	'd5a3d2b4ca94ae61bb4592ca26385f91463a11cac4334e037c102dc6fe9018f6',
	'9e97ba9b215a20da80e8607bdb1cad97d498ac7be51568b2c38bcf7d1bbdaaae'
	]
URL_SCAN_FILE = 'https://www.virustotal.com/vtapi/v2/file/scan'
URL_RESCAN_FILE = 'https://www.virustotal.com/vtapi/v2/file/rescan'
URL_REPORT_SCAN_FILE = 'https://www.virustotal.com/vtapi/v2/file/report'
URL_APK='/mnt/c/Users/cnsc-/Downloads/APK'

class FileInformation(object):
	def __init__(self, scan_id, sha1, resource, response_code, scan_date, permalink, verbose_msg, sha256, positives, total, md5, scans, app_id):
		super(FileInformation, self).__init__()
		self.__scan_id = scan_id
		self.__sha1 = sha1
		self.__resource = resource
		self.__response_code = response_code
		self.__scan_date = scan_date
		self.__permalink = permalink
		self.__verbose_msg = verbose_msg
		self.__sha256 = sha256
		self.__positives = positives
		self.__total = total
		self.__md5 = md5
		self.__scans = scans
		self.__app_id = app_id

	def get_scan_id(self):
		return self.__scan_id

	def get_sha1(self):
		return self.__sha1

	def get_resource(self):
		return self.__resource

	def get_response_code(self):
		return self.__response_code

	def get_scan_date(self):
		return self.__scan_date

	def get_permalink(self):
		return self.__permalink

	def get_verbose_msg(self):
		return self.__verbose_msg

	def get_sha256(self):
		return self.__sha256

	def get_positives(self):
		return self.__positives

	def get_total(self):
		return self.__total

	def get_md5(self):
		return self.__md5

	def get_scans(self):
		return self.__scans

	def get_app_id(self):
		return self.__app_id


class FileReport(object):
	"""docstring for FileReport"""
	def __init__(self, file_uploaded):
		super(FileReport, self).__init__()
		self.__file_uploaded = file_uploaded
		self.__resource_file = None
		self.__file_info = None
		self.__file_id = None
		self.__sha1 = None

	def get_file_info(self):
		return self.__file_info

	def get_resource_file(self):
		BLOCKSIZE = 65536
		hasher = hashlib.sha256()
		with open(self.__file_uploaded, 'rb') as afile:
			buf = afile.read(BLOCKSIZE)
			while len(buf) > 0:
				hasher.update(buf)
				buf = afile.read(BLOCKSIZE)
		self.__resource_file = hasher.hexdigest()
		return hasher.hexdigest()
	
	def scan_file(self):
		params = {'apikey': random.choice(API_KEY)}
		files = {'file': (os.path.basename(self.__file_uploaded), open(self.__file_uploaded, 'rb'))}
		response = requests.post(URL_SCAN_FILE, files=files, params=params)
		json_response = response.json()
		self.__resource_file = response.json().get('resource')

	def rescan_file(self):
		params = {'apikey' : random.choice(API_KEY), 'resource': self.__resource_file}
		headers = {
			"Accept-Encoding": "gzip, deflate",
			"User-Agent" : "gzip,  My Python requests library example client or username"
			}
		json_response = requests.post(URL_RESCAN_FILE, params=params)
		self.__resource_file = json_response.json().get('resource')

	def report_file(self):
		params = {'apikey': random.choice(API_KEY), 'resource': self.__resource_file}
		headers = {
		  "Accept-Encoding": "gzip, deflate",
		  "User-Agent" : "gzip,  My Python requests library example client or username"
		  }

		response_report = requests.get(URL_REPORT_SCAN_FILE,params=params, headers=headers)
		json_response = response_report.json()
		self.__file_info = json_response
		return 	response_report.status_code
		

	# def add_database(self):
	# 	global id_app
	# 	format_scans = ""
	# 	print self.__file_info.get('scans')
	# 	for key, value in self.__file_info.get('scans').iteritems():
	# 		format_scans += key + "|" + str(value).replace("u'", "'").replace(": False,", ": 'false',").replace(": True,"," : 'true',").replace(": None,", ": 'null',") + "-+-"
	# 	file_info = FileInformation(self.__file_info.get('scan_id'), self.__file_info.get('sha1'), self.__file_info.get('resource'), self.__file_info.get('response_code'), self.__file_info.get('scan_date'), self.__file_info.get('permalink'), self.__file_info.get('verbose_msg'), self.__file_info.get('sha256'), self.__file_info.get('positives'), self.__file_info.get('total'), self.__file_info.get('md5'), format_scans, id_app)
	# 	self.insert_json_databse(file_info)

	# def insert_json_databse(self, file_info):
	# 	db = MySQLdb.connect(host="localhost", user="root", passwd="Matkhaula123", db="ntcanalysis", charset='utf8', unix_socket = "/var/run/mysqld/mysqld.sock",use_unicode=True)
	# 	cursor = db.cursor()
	# 	sql = 'INSERT INTO virustotal(scanid, sha1, resource, responsecode, scandate, permalink, verbosemsg, sha256, positives, total, md5, scans, appid) VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")' 
	# 	% (file_info.get_scan_id(), file_info.get_sha1(), file_info.get_resource(), file_info.get_response_code(), file_info.get_scan_date(), file_info.get_permalink(), file_info.get_verbose_msg(), file_info.get_sha256(), file_info.get_positives(), file_info.get_total(), file_info.get_md5(), file_info.get_scans(), file_info.get_app_id())
	# 	try:
	# 		cursor.execute(sql)
	# 		self.__file_id = cursor.lastrowid
	# 		db.commit()
	# 	except Exception, ex:
	# 		print "Exception Dao: ", ex
	#    		db.rollback()
	# 	finally:
	# 		db.close()

	

	def save_json_file(self,hash):
		with open(hash, 'wb') as handle:
			json.dump(self.get_file_info(), handle,indent=4, sort_keys=True)
	def return_json_file(self):
		data = self.get_file_info()
		return data
	def get_file_id(self):
		return self.__file_idimort
def get_list_apk():
		apks = []
		for root, dirs, files in os.walk(URL_APK):
			for file in files:
				if file.endswith('.apk'):
					apks.append(os.path.join(root, file))
		return apks
def postVirustotal(url):
	try:
		file_uploaded = str(url)
		file_report = FileReport(file_uploaded)
		hash = file_report.get_resource_file()
		file_report.report_file()
		print file_report.get_file_info().get('response_code')
		while file_report.get_file_info().get('response_code') <= 0:
			file_report.scan_file()
			file_report.report_file()
			time.sleep(5)
		return file_report.return_json_file()
	except Exception, ex:
		print ex
		return None
# if __name__ == '__main__':
# 	listApk = get_list_apk()
# 	for url in listApk:
# 		print url
# 		try:
# 			file_uploaded = url
# 			file_report = FileReport(file_uploaded)
# 			hash = file_report.get_resource_file()
# 			file_report.report_file()
# 			print file_report.get_file_info().get('response_code')
# 			while file_report.get_file_info().get('response_code') <= 0:
# 				file_report.scan_file()
# 				file_report.report_file()
# 				time.sleep(5)
# 			file_report.save_json_file(hash)
# 		except Exception, ex:
# 			print ex
		
