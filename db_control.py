import pymongo

def connect():
	client = pymongo.MongoClient("localhost", 27017)
	db = client.inscrawl
	collection = db.inscrawl
	return collection


def insert(data):
	con = connect()
	try:
		con.insert_one(data.__dict__)
	except Exception as e:
		print("error{}".format(e))
	finally:
		pass
	    


def findall():
	con = connect()
	data = con.find({}, {'_id': 0})
	for i in data:
		yield i



def showall():
	datas = findall()
	count = 0
	for i in datas:
		count += 1
		print(i)
	print("num: %d" % count)