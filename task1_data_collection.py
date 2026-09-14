import requests
import json
import os
import time
from datetime import datetime
import re 

# URLS
STORIES_URL="https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL="https://hacker-news.firebaseio.com/v0/item/{}.json"

HEADERS={
    "User-Agent":"TrendPulse/1.0"
}

# KEYWORDS
CATEGORY_KEYWORDS={
    "technology":["ai","software","tech","code","computer","data","cloud","api","gpu","llm"],
    "worldnews":["war","government","country","president","election","climate","attack","global"],
    "sports":["nfl","nba","fifa","sport","team","player","league","championship","game"],
    "science":["research","study","space","physics","biology","discovery","nasa","genome"],
    "entertainment":["movie","music","film","netflix","game","book","show","award","streaming"]
}

# function to assign category

def get_category(title):
    title_lower=title.lower()
    for category,keywords in CATEGORY_KEYWORDS.items():
        for keyword in keywords:
            if keyword.lower() in title_lower:

                return category
    return None

# fetching top story IDs

def fetch_top_story_ids():
    try:
        response=requests.get(STORIES_URL,headers=HEADERS,timeout=10)
        response.raise_for_status()
        return response.json()[:500]
    except Exception as e:
        print(f"Unable to fetch top story IDs:{e}")
        return[]

 # collect stories


def collect_all_stories():
    story_ids = fetch_top_story_ids()
    stories = []

    # Maximum 25 stories per category
    MAX_PER_CATEGORY = 25

    # Track number of stories collected for each category
    category_count = {
        category: 0 for category in CATEGORY_KEYWORDS
    }

    print("Collecting stories across categories...")

    # Process each category separately
    for category, keywords in CATEGORY_KEYWORDS.items():

        print(f"\nCollecting {category} stories...")

        for story_id in story_ids:

            # Stop when this category reaches 25 stories
            if category_count[category] >= MAX_PER_CATEGORY:
                break

            try:
                response = requests.get(
                    ITEM_URL.format(story_id),
                    headers=HEADERS,
                    timeout=5
                )

                response.raise_for_status()

                story = response.json()

                # Skip invalid stories
                if not story or story.get("type") != "story":
                    continue

                title = story.get("title", "")
                title_lower = title.lower()

                # Check whether the title contains
                # any keyword from the current category
                matched = False

                for keyword in keywords:
                    if keyword.lower() in title_lower:
                        matched = True
                        break

                # Skip if no keyword matches
                if not matched:
                    continue

                story_data = {
                    "post_id": story.get("id"),
                    "title": title,
                    "category": category,
                    "score": story.get("score", 0),
                    "num_comments": story.get("descendants", 0),
                    "author": story.get("by", ""),
                    "collected_at": datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                }

                stories.append(story_data)

                # Increase category count
                category_count[category] += 1

            except Exception as e:
                print(f"Unable to fetch story {story_id}: {e}")
                continue

        # Wait 2 seconds before next category
        time.sleep(2)

    return stories, category_count




# Run collection
stories, category_count = collect_all_stories()

# Create data directory
os.makedirs("data", exist_ok=True)

# Save JSON file
filename = f"data/trends_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

print("\nCollection Complete")
print("_" * 50)
for category, count in category_count.items():
    print(f"{category:<15}: {count} stories collected")
print("_" * 50)

with open(filename, "w", encoding="utf-8") as file:
    json.dump(stories, file, indent=2, ensure_ascii=False)

print(f"Collected {len(stories)} stories. Saved to {filename}")