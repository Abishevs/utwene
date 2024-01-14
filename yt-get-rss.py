import requests
import sys

url = sys.argv[1]

r = requests.get(url)
r.text
s_str = "channelId"
s_name = "/@"

start = r.text.find(s_str)
start += len(s_str) + 3
end = r.text.find('"', start)
channel_id = r.text[start:end]
yt_rss = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"

start = r.text.find(s_name)
start += len(s_name)
end = r.text.find('"', start)
channel_name = r.text[start:end]

print(f'# {channel_name} \n{yt_rss} "YT"')
