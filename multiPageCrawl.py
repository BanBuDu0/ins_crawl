import db_control
import run
from module import URLData


def getDeepPic(data):
    shortcode = data.shortcode
    url = "https://www.instagram.com/p/%s/" % shortcode
    data_json = run.getStartJson(url)
    try:
        edges = data_json['entry_data']['PostPage'][0]['graphql']['shortcode_media']['edge_sidecar_to_children']['edges']
        # print(len(edges))
        for i in range(1, len(edges)): 
            node = edges[i]['node']
            urldata = URLData()
            urldata.shortcode = node['shortcode']
            urldata.is_video = node['is_video']
            if node['is_video']:
                urldata.url = node['video_url']
            else:
                urldata.url = node['display_url']
            yield urldata
    except Exception as e:
        pass