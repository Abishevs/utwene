#!/usr/bin/env python3

import sqlite3
import os
import subprocess
import random
import sys
import tomllib
import time

VIDEO_EXTENSIONS = ['.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm', '.3gp', '.mpeg', '.mpg', '.vob']

def get_unread_articles(feed_urls, database_path):
    con = sqlite3.connect(database_path)
    cur = con.cursor()
    
    placeholders = ','.join('?' for _ in feed_urls)
# fetch only non hashtag titles! as why tf you need yt shorts?
    query = f"""
        SELECT id, title, url 
        FROM rss_item 
        WHERE unread = '1' 
        AND feedurl IN ({placeholders}) 
        AND title NOT LIKE '%#%'
        ORDER BY pubDate DESC
        LIMIT 10
        """
    
    cur.execute(query, feed_urls)
    
    articles = cur.fetchall()
    con.close()
    return articles

def mark_as_read(article_id, database_path):
    con = sqlite3.connect(database_path)
    cur = con.cursor()

    query = f"UPDATE rss_item SET unread = 0 WHERE id = ?"
    cur.execute(query, (article_id,))

    con.commit()
    con.close()

def get_urls(urls_config_path:str, tag:str) -> list[str]:
    urls = []
    with open(urls_config_path, 'r') as file:
        for line in file:
            fields = line.split()
            if len(fields) >= 2 and f'"{tag}"' in fields[1:]:
                urls.append(fields[0])
    
    return urls

def run_yt_from_newsboat(config):
    database_path = os.path.expanduser(config['newsboat']['db'])
    urls_config_path = os.path.expanduser(config['newsboat']['urls']) 
    tag = config['newsboat']['tag']

    subprocess.run(['newsboat', '-x', 'reload'])  # Refresh. Get latest feeds

    # Fetch articles
    feed_urls = get_urls(urls_config_path, tag)
    unread_articles = get_unread_articles(feed_urls, database_path)
    max_index = len(unread_articles) - 1

    selected_article_index = 0
    if len(sys.argv) >= 2 and sys.argv[1] == "-r":
        # Get random article
        selected_article_index = random.randint(0, max_index)

    article_id = unread_articles[selected_article_index][0]
    get_url = unread_articles[selected_article_index][2]  # Get URL of the first article
    mark_as_read(article_id, database_path)

    # Open with mpv player
    subprocess.run(['mpv', '--cache=yes', '--cache-secs=1', '--no-terminal', get_url])

def run_local_tv(config):
    print('Hello')
    tv_paths = config['tv']['paths']
    video_files = []
    for path in tv_paths:
        path = os.path.expanduser(path)
        for filename in os.listdir(path):
            if any(filename.endswith(ext) for ext in VIDEO_EXTENSIONS):
                full_path = os.path.join(path, filename)
                video_files.append(full_path)
    
    random_index = random.randint(0, len(video_files) - 1)
    subprocess.run(['mpv', '--no-terminal', video_files[random_index]])

def yt_is_boring(tmp_file_path, time_threshold=300):
    current_time = time.time()
    try:
        with open(tmp_file_path, 'r') as file:
            timestamps = [float(line.strip()) for line in file.readlines()]

        # Filter out timestamps older than the threshold
        timestamps = [t for t in timestamps if current_time - t < time_threshold]

        if len(timestamps) >= 2:  # Check if 2 previous runs were within the threshold
            return True

    except FileNotFoundError:
        pass  # File doesn't exist yet, so it's the first run

    # Write the current timestamp to the file
    with open(tmp_file_path, 'a') as file:
        file.write(f"{current_time}\n")

    return False

def main():
    config_path = os.path.expanduser('~/.config/utwene/config.toml')
    tmp_file_path = '/tmp/utwene.log'

    try:
        with open(config_path, 'rb') as file:
            config = tomllib.load(file)
        if yt_is_boring(tmp_file_path):
            run_local_tv(config)
        else:
            run_yt_from_newsboat(config)
    except FileNotFoundError:
        print(f"Config file not found at {config_path}")

    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()

    
