# UTWENE (pronounced "you-twain").
![Status](https://img.shields.io/badge/Status-Under_Development-red)

"Useless Time Waster but Entertaining Newsboat Extractor".
Is an small program to start the newest video from chosen channels
extracted from newsboat feeds db, each video gonna be auto marked as
read in your newsboat program.
If after couple of tries you can't seem to find the right video.
Then it starts an localy downloaed video (5 minute threshold, then it
restarts). For me I chose to play a randomly chosen episode of Suits (my favororite
tv show).

* There are still bugs, this is not finnished thus not all errors are
  handled gracefully. If launched from dmenu you won't see any erros of
  course nor are they logged.
* It's noticibly slow when it comes to newsboat extracting. gonna rewrite it all in rust when it becomes more mature.

## Installation
check makefile to change where you want to install the script (so that
it's globably available for your user. Default location is "~/.local/bin"

### Dependencies
* mpv 
* Python 3.11 or higher 
* newsboat installed and configured
* local tv videos configured (supported searched video formats: 
'.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm', '.3gp',
'.mpeg', '.mpg', '.vob')

```bash
git clone https://github.com/Abishevs/UTWENE.git
cd UTWENE
make install
```

## Setup
Create an config file. in 
```bash
mkdir ~/.config/utwene/
vim ~/.config/utwene/config.toml
```
There provide all of these. Where tag is an newsboat tag (can be only one rn), but it uses it to
determine which feeds to use.
```toml
[newsboat]
db = "~/.newsboat/cache.db"
urls = "~/.newsboat/urls"
tag = "ML"

[tv]
paths = ["~/path/to/videos",]
```

### There is also an yt rss extractor utility
With that utility. Provide an yt video url and it will find channel_id
and create an rss feed url and append it to your newsboat/urls with an
"YT" tag. Also add an comment with yt channel name

```bash
py yt-get-rss.py url >> ~/.newsboat/urls
```
Example output:
```bash
# channel_name
url "YT"
```

