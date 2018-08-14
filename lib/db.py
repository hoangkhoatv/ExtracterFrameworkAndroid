import pymongo
import const

# test_record = {
#     'name': 'abc',
#     'hash': 'aaaaaaa'
# }

def conn_db():
    try:
        client = pymongo.MongoClient(const.db_url)
        db = client['evaluate-security']
        collection = db['firmware-android']
        return collection
        print "Connected Database"

    except pymongo.errors.ConnectionFailure, e:
        print "Could not connect to server: %s" % e

# client = pymongo.MongoClient(const.db_url)

# db = client['evaluate-security']
#
# collection = db['test-collection']
#
# result = collection.insert_one(test_record)
# print result

def insert_record(params):
    collection = params[0]
    collection.insert_one(params[1])

def get_firmware_by_hash(params):
    collection = params['collection']
    return collection.find_one({'hash': params['hash']})

def get_all_hash(params):
    collection = params['collection']
    return collection.find({}).limit(5)
