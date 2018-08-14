import psycopg2
import os
import re

class dbhelper(object):

    def __init__(self, db, user, host, password):
        self.conn = psycopg2.connect(dbname=db, user=user, host=host, password=password)
        self.cur = self.conn.cursor()
        self.db = db
        self.user = user
        self.host = host
        print 'Connection Open'
    def getStatus(self):
        return self.conn.status()

    def drop_table(self, table_name):
        drop_query = 'DROP TABLE IF EXISTS {0};'
        self.cur.execute(drop_query.format(table_name))
        self.conn.commit()
        print 'Table {0} dropped.'.format(table_name)

    def end_connection(self):
        self.conn.close()
        print 'Connection Closed'

    def insert_rom_extract(self, name, hash, extension, status, output_file, version, time, sdk, size,type):
        query =  "INSERT INTO public.rom(name, hash, extension, status, output_file, version, time, sdk, size,type) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
        self.cur.execute(query,(name,hash,extension,status,output_file,version,time,sdk,size,type))
        self.conn.commit()
        print 'Inserted rom'

    def insert_rom_details(self, romid, virustotal ,xrom,hash_app,name_app,size_app):
        query =  "INSERT INTO public.rom_details(romid,virustotal,xrom,hash_app,is_framework,name_app,size_app) VALUES (%s, %s, %s, %s, %s, %s, %s);"
        self.cur.execute(query,(romid,virustotal,xrom,hash_app,False,name_app,size_app))
        self.conn.commit()
        print 'Inserted rom details'
    def insert_rom_details_framework(self, romid, virustotal ,xrom,hash_app,name_app,size_app):
        query =  "INSERT INTO public.rom_details(romid,virustotal,xrom,hash_app,is_framework,name_app,size_app) VALUES (%s, %s, %s, %s, %s, %s, %s);"
        self.cur.execute(query,(romid,virustotal,xrom,hash_app,True,name_app,size_app))
        self.conn.commit()
        print 'Inserted rom details framework'
    def insert_virustotal(self, appid, scanid, response_code, scan_date, hash, total, positives, permalink,raw):
        query =  "INSERT INTO public.virustotal(appid,scan_id,response_code,scan_date,hash,total,positives,permalink,raw) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);"
        self.cur.execute(query,(appid,scanid,response_code,scan_date,hash,total,positives,permalink,raw))
        self.conn.commit()
        print 'Inserted virustotal'
    
    def insert_xrom(self, appid, hash, status):
        query =  "INSERT INTO public.xrom(appid,hash,status) VALUES (%s, %s, %s);"
        self.cur.execute(query,(appid,hash,status))
        self.conn.commit()
        print 'Inserted xrom'
    
    def insert_config(self,romid,name,s01,s02,s03,s04,s05,s06):
        query =  "INSERT INTO public.config(romid,name,s01,s02,s03,s04,s05,s06) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
        self.cur.execute(query,(romid,name,s01,s02,s03,s04,s05,s06))
        self.conn.commit()
        print 'Inserted rom config'

    def update_xrom_soure_sink(self,hash,isSource,isSink):
        query = "UPDATE public.xrom SET critical_sink=%s,sensitive_source=%s WHERE hash=%s;"
        self.cur.execute(query,(isSink,isSource,hash))
        self.conn.commit()
        print "Updated xrom Soure Sink"
        
    def update_xrom(self,hash,status):
        query = "UPDATE public.xrom SET status=%s WHERE hash=%s;"
        self.cur.execute(query,(status,hash))
        self.conn.commit()
        print "Updated xrom"

    def update_rom_details(self,hash):
        query = "UPDATE public.rom_details SET virustotal=%s,xrom=%s WHERE hash_app=%s;"
        self.cur.execute(query,(True,True,hash))
        self.conn.commit()
        print "Updated Rom Details"
    
    def is_rom(self, hash):
        query = "SELECT appid FROM public.rom WHERE hash='"+hash +"'"
        self.cur.execute(query)
        rows = self.cur.fetchall()
        return len(rows)
      
    def query_id_rom(self, hash):
        query = "SELECT id FROM public.rom WHERE hash='"+hash +"'"
        self.cur.execute(query)
        rows = self.cur.fetchone()
        if rows != None:
            return rows[0]
        else:
            return None

    def check_rom(self,hash):
        query = "SELECT * FROM public.rom WHERE hash='"+hash +"'"
        self.cur.execute(query)
        rows = self.cur.fetchone()
        if rows != None:
            return rows[0]
        else:
            return None
    

    def query_id_app(self, hash):
        query = "SELECT appid FROM public.rom_details WHERE hash_app='"+hash +"'"
        self.cur.execute(query)
        rows = self.cur.fetchone()
        if rows != None:
            return rows[0]
        else:
            return None
    
    def get_data_rom(self,romid):
        query = "SELECT t1.name, t1.hash, t1.extension, t1.output_file, t1.version, t1.time, t1.sdk,  t1.size, t1.status, t1.type, t2.hash_app, t2.name_app, t2.size_app, t2.is_framework, t3.name, t3.s01, t3.s02, t3.s03, t3.s04, t3.s05, t3.s06 FROM rom as t1 LEFT JOIN rom_details as t2 ON t1.id=t2.romid LEFT JOIN config as t3 ON t1.id=t3.romid WHERE t1.id=" + str(romid)
        self.cur.execute(query) 
        rows = self.cur.fetchall()
        if rows != None:
            return rows
        else:
            return None

    

            