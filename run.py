
# coding: utf-8

# # CFD-Online community analysis
# 
# In this notebook we will examine the most popular CFD software forums on CFD-online.com. 

# In[ ]:

import matplotlib.pyplot as plt
get_ipython().magic('matplotlib inline')
import seaborn as sns
from pxl.styleplot import set_sns
set_sns()
plt.rcParams["axes.grid"] = True
plt.rcParams["axes.formatter.limits"] = (-4, 4)
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import os

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
df = pd.DataFrame(columns=["forum", "threads", "posts"])

for forum in forums:
    s = pd.Series()
    s["forum"] = forum
    s["threads"] = threads[forum]
    s["posts"] = posts[forum]
    df = df.append(s, ignore_index=True)

df = df.set_index("forum")
df["pt_ratio"] = df.posts/df.threads


# In[ ]:

# Create a slice of that DataFrame for only the most popular forums
df2 = df[df.posts > 1e4].sort("posts")
df2 = df2.drop("posts", 1)

fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(7.5, 3), sharey=True)

df2.threads.plot(ax=ax1, kind="barh")
df2.pt_ratio.plot(ax=ax2, kind="barh", color=sns.color_palette()[2])

ax1.set_ylabel("")
ax2.set_ylabel("")
ax1.set_xlabel("Threads")
ax2.set_xlabel("Posts/threads")
fig.tight_layout()

if not os.path.isdir("figures"):
    os.mkdir("figures")

fig.savefig("figures/cfd-online.pdf")

plt.show()

