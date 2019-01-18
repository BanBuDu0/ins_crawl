import pymongo
import db_control

if __name__ == '__main__':
    cn = db_control.connect()
    cn.delete_many({})

