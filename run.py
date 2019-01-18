# -*- coding: UTF-8 -*-
import requests
import re
import json
from urllib import parse
import db_control
from module import URLData
import multiPageCrawl


def getHTML(url):
    headers = {
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) \
                    Chrome/66.0.3359.139 Safari/537.36',
        'referer': 'https://www.instagram.com/',
        'cookie': 'mid=XDsZmAALAAGuNAVARO2QAmuBpnWc; mcd=3; shbid=17529; shbts=1547377187.7138195; rur=FRC; csrftoken=8Gy2564OVtbtrmZY6Nc7mfQkr2eK3oxq; \
                 ds_user_id=7406815247; sessionid=7406815247%3AqEy4jFQqKpkcRr%3A27; urlgen="{"144.34.158.47": 25820}:1gjhmK:x-DtroZ39rLHV4Ouad7QZVR0baY"'
    }
    r = requests.get(url, headers=headers)
    r.encoding = r.apparent_encoding
    status_code = r.status_code
    print(status_code)
    r = r.text
    return r


def myParse(edge_owner, param):
    #edge_owner = data_json['data']['user']['edge_owner_to_timeline_media']
    page_info = edge_owner['page_info']
    has_next_page = page_info['has_next_page']
    end_cursor = page_info['end_cursor']
    edges = edge_owner['edges']

    for i in range(len(edges)):
        node = edges[i]['node']
        one_data = URLData()
        one_data.shortcode = node['shortcode']
        one_data.url = node['display_url']
        is_single_pic = node['media_preview']
        is_video = node['is_video']
        db_control.insert(one_data)
            
        if not is_single_pic:
            datas = multiPageCrawl.getDeepPic(one_data)
            if datas:
                for i in datas:
                    db_control.insert(i)

    if has_next_page:
        param['after'] = page_info['end_cursor']
        text = json.dumps(param)
        url = "https://www.instagram.com/graphql/query/?query_hash=e6a78c2942f1370ea50e04c9a45ebc44&variables="+parse.quote(text)
        r = getHTML(url)
        temp_json = json.loads(r)
        temp_owner = temp_json['data']['user']['edge_owner_to_timeline_media']
        myParse(temp_owner, param)


def getStartJson(url):
    r = getHTML(url)
    p = re.compile(r'<script type="text/javascript">window._sharedData =(.*?);</script>')
    # p = re.compile(r'<script type="text/javascript">window._sharedData = (.*?);</script>')
    data = p.search(r).group(1)
    data_json = json.loads(data)
    return data_json



if __name__ == '__main__':
    start_url = "https://www.instagram.com/ysubini/"
    data_json = getStartJson(start_url)
    user = data_json['entry_data']['ProfilePage'][0]['graphql']['user']
    
    USERID = user['id']
    USERNAME = user['username']

    edge_owner = user['edge_owner_to_timeline_media']
    param = {
        'id': USERID,
        'first': 12,
        'after': None
    }
    myParse(edge_owner, param)
