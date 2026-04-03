# Import libraries
import requests
import json
import os
from datetime import datetime

# Step 1: Get top story IDs
url = "https://hacker-news.firebaseio.com/v0/topstories.json"
response = requests.get(url)
story_ids = response.json()[:500]  # first 500

# Categories with keywords
categories = {
    "technology": ["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["nfl", "nba", "fifa", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome"],
    "entertainment": ["movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming"]
}

# Function to assign category
def get_category(title):
    title = title.lower()
    for cat, keywords in categories.items():
        for word in keywords:
            if word in title:
                return cat
    return "others"

# Store results
results = []
category_count = {cat: 0 for cat in categories}

# Step 2: Fetch story details
for story_id in story_ids:
    story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
    res = requests.get(story_url)
    story = res.json()

    if story is None or "title" not in story:
        continue

    title = story.get("title", "")
    category = get_category(title)

    # Limit 25 per category
    if category in category_count and category_count[category] >= 25:
        continue

    if category in category_count:
        category_count[category] += 1

    data = {
        "post_id": story.get("id"),
        "title": title,
        "category": category,
        "score": story.get("score", 0),
        "num_comments": story.get("descendants", 0),
        "author": story.get("by", "unknown"),
        "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    results.append(data)

    # Stop when enough collected
    if len(results) >= 125:
        break

# Step 3: Save to JSON
os.makedirs("data", exist_ok=True)

filename = f"data/trends_{datetime.now().strftime('%Y%m%d')}.json"

with open(filename, "w") as f:
    json.dump(results, f, indent=4)

# Final output
print(f"Collected {len(results)} stories. Saved to {filename}")