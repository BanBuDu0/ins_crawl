import db_control
import os
import requests
from module import UserInfo

def download_pic(user: UserInfo):
    j = 0
    path = "./" + (user.name + user.id)
    os.mkdir(path)
    table_name = user.name + user.id
    for i in db_control.findall(table_name):
        pic_html = requests.get(i['url'])
        with open("{}/{}.jpg".format(path, j), "wb") as f:
            f.write(pic_html.content)
        j = j + 1
