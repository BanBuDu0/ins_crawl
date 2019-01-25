import pymongo

def connect(tableName):
    client = pymongo.MongoClient("localhost", 27017)
    db = client.inscrawl
    collection = db[tableName]
    return collection


def insert(data, tableName):
    con = connect(tableName)
    try:
        con.insert_one(data.__dict__)
    except Exception as e:
        print("error{}".format(e))
    finally:
        pass


def findall(tableName):
    con = connect(tableName)
    data = con.find({}, {'_id': 0})
    for i in data:
        yield i


def showall(tableName):
    datas = findall(tableName)
    count = 0
    for i in datas:
        count += 1
        print(i)
    print("num: %d" % count)