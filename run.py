import requests
import re
import json
from urllib import parse
import db_control
from module import URLData, UserInfo
from downloads import download_pic


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


def get_html_json(url):
    r = getHTML(url)
    p = re.compile(r'window._sharedData = (.*?);</script>')
    data = p.search(r).group(1)
    data_json = json.loads(data)
    return data_json


def multi_page_crawl(shortcode, tableName):
    url = "https://www.instagram.com/p/%s/" % shortcode
    data_json = get_html_json(url)
    try:
        edges = data_json['entry_data']['PostPage'][0]['graphql']['shortcode_media']['edge_sidecar_to_children']['edges'][1:]
        for i in edges:
            node = i['node']
            one_data = URLData()
            one_data.shortcode = node['shortcode']
            one_data.is_video = node['is_video']
            if node['is_video']:
                one_data.url = node['video_url']
            else:
                one_data.url = node['display_url']
            db_control.insert(one_data, tableName)
    except:
        pass


def myParse(edge_owner, param, tableName):
    page_info = edge_owner['page_info']
    has_next_page = page_info['has_next_page']
    end_cursor = page_info['end_cursor']
    edges = edge_owner['edges']

    for i in edges:
        node = i['node']
        one_data = URLData()
        one_data.shortcode = node['shortcode']
        one_data.is_video = node['is_video']
        if node['is_video']:
            one_data.url = node['video_url']
        else:
            one_data.url = node['display_url']
        db_control.insert(one_data, tableName)

        is_single_pic = node['media_preview']
        if not is_single_pic:
            multi_page_crawl(one_data.shortcode, tableName)

    if has_next_page:
        param['after'] = end_cursor
        text = json.dumps(param)
        url = "https://www.instagram.com/graphql/query/?query_hash=e6a78c2942f1370ea50e04c9a45ebc44&variables=" + parse.quote(text)
        r = getHTML(url)
        temp_json = json.loads(r)
        temp_owner = temp_json['data']['user']['edge_owner_to_timeline_media']
        myParse(temp_owner, param, tableName)


def get_user(url):
    data_json = get_html_json(url)
    user_data = data_json['entry_data']['ProfilePage'][0]['graphql']['user']
    user_info = UserInfo()

    user_info.id = user_data['id']
    user_info.name = user_data['username']
    return (user_info, user_data)


def get_user_data(user: UserInfo, user_data):
    table_name = user.name + user.id
    param = {
        'id': user.id,
        'first': 12,
        'after': None
    }
    edge_owner = user_data['edge_owner_to_timeline_media']
    myParse(edge_owner, param, table_name)


if __name__ == "__main__":
    start_url = "https://www.instagram.com/ysubini/"
    user_info, user_data = get_user(start_url)
    get_user_data(user_info, user_data)
    # download_pic(user)