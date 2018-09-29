#!/usr/bin/env python
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
import os
import requests
import re
import sys

def get(url, regex):
    r = requests.get(url)
    if not r.ok:
        return

    html = BeautifulSoup(r.text, "lxml")
    imgs = html.find_all("a", {"href": regex})
    spl = url.split('/')
    imgdir = os.path.expandvars('$HOME/Pictures/4chan/'
                                + spl[-3] + '/'
                                + spl[-1] + '/')
    os.makedirs(imgdir, exist_ok=True)

    for img in imgs:
        try:
            imglink = img["href"]
            imgname = imglink.split("/")[-1]
            urlretrieve("http:" + imglink, imgdir + imgname)
        except Exception as e:
            print("Failed to download img", str(e))

    print('Saved images in', imgdir)


if __name__ == '__main__':
    regex = re.compile(".jpg$|.png$|.gif$|.jpeg$|.webm$")
    urls = sys.argv[1:]
    for url in urls:
        get(url, regex)    
