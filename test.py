from run import getHTML, get_html_json
# import io
# import sys
import json
from urllib import parse


# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')

param = {
    "id":"7406815247",
    "include_reel": True,
    "fetch_mutual": False,
    "first":24
}

text = json.dumps(param)
this_url = "https://www.instagram.com/graphql/query/?query_hash=c56ee0ae1f89cdbd1c89e2bc6b8f3d18&variables=" + parse.quote(text)
data = get_html_json(this_url)
edges = data['entry_data']['ProfilePage']['graphql']['user']['edge_owner_to_timeline_media']['edges']
for i in edges:
    print(i[''])