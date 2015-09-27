#!/usr/bin/env python
"""
This script parses the cfd-online.com main forum page for thread and post
counts.
"""

import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

soup = BeautifulSoup(requests.get("http://cfd-online.com/Forums/").text, "lxml")

# Find all numbers in tables on the page
numbers = soup.find_all("td", text=re.compile("\d+"))

# alt1 class is threads, alt2 class is posts
forums = []
threads = {}
posts = {}

for n in numbers:
    forum = n.parent.find("strong").text
    if not forum in forums:
        forums.append(forum)
    if "alt1" in n.attrs["class"]:
        threads[forum] = int(n.text.replace(",", ""))
    elif "alt2" in n.attrs["class"]:
        posts[forum] = int(n.text.replace(",", ""))

# Create a DataFrame from the dictionaries
df = pd.DataFrame()

for forum in forums:
    s = pd.Series()
    s["forum"] = forum
    s["threads"] = threads[forum]
    s["posts"] = posts[forum]
    df = df.append(s, ignore_index=True)

print(df)
