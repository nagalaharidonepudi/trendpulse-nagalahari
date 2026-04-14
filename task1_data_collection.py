import requests
import json
from datetime import datetime
import os

# Create data folder
os.makedirs("data", exist_ok=True)

TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

headers = {"User-Agent": "TrendPulse/1.0"}

categories = {
    "technology": ["ai","software","tech","code","computer","data","cloud","api","gpu","llm"],
    "worldnews": ["war","government","country","president","election","climate","attack","global"],
    "sports": ["nfl","nba","fifa","sport","game","team","player","league","championship"],
    "science": ["research","study","space","physics","biology","discovery","nasa","genome"],
    "entertainment": ["movie","film","music","netflix","game","book","show","award","streaming"]
}

def get_category(title):
    title = title.lower()
    for cat, words in categories.items():
        for w in words:
            if w in title:
                return cat
    return None

# Fetch IDs
ids = requests.get(TOP_STORIES_URL).json()[:500]

data = []
count = {c:0 for c in categories}

for i in ids:
    try:
        story = requests.get(ITEM_URL.format(i)).json()
        if not story or "title" not in story:
            continue
        
        cat = get_category(story["title"])
        if not cat:
            continue
        
        if count[cat] >= 25:
            continue
        
        data.append({
            "post_id": story.get("id"),
            "title": story.get("title"),
            "category": cat,
            "score": story.get("score",0),
            "num_comments": story.get("descendants",0),
            "author": story.get("by",""),
            "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        
        count[cat]+=1
        
        if sum(count.values())>=125:
            break
    except:
        continue

# Save file
filename = f"data/trends_{datetime.now().strftime('%Y%m%d')}.json"
with open(filename,"w") as f:
    json.dump(data,f,indent=4)

print("Collected",len(data),"stories")
print("Saved:",filename)