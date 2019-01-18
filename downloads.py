import db_control
import os
import requests

if __name__ == '__main__':
    j = 0
    path = "./{}{}".format('ysubini', '453231227')
    os.mkdir(path)
    for i in db_control.findall():
        pic_html = requests.get(i['url'])
        with open("{}/{}.jpg".format(path, j), "wb") as f:
            f.write(pic_html.content)
        j = j + 1