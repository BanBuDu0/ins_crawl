import pymongo
import db_control

if __name__ == '__main__':
    cn = db_control.connect(tableName='ysubini453231227')
    cn.delete_many({})

