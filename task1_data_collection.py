
       import requests
import json
from datetime import datetime
import os

# Create data folder
os.makedirs("data", exist_ok=True)

TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

ids = requests.get(TOP_STORIES_URL).json()

data = []
index = 0

# Keep fetching until we get 120 valid stories
while len(data) < 120 and index < len(ids):
    try:
        story = requests.get(ITEM_URL.format(ids[index])).json()
        index += 1

        if story is None or "title" not in story:
            continue

        data.append({
            "post_id": story.get("id"),
            "title": story.get("title"),
            "category": "general",
            "score": story.get("score", 0),
            "num_comments": story.get("descendants", 0),
            "author": story.get("by", ""),
            "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    except:
        index += 1
        continue

# Save JSON
filename = f"data/trends_{datetime.now().strftime('%Y%m%d')}.json"
with open(filename, "w") as f:
    json.dump(data, f, indent=4)

print("Collected", len(data), "stories")
print("Saved:", filename)
