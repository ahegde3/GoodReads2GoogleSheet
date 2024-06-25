import feedparser
import json

def fetchRssData():
    # URL of the RSS feed
    rss_url = "https://www.goodreads.com/review/list_rss/70445162?key=qg0XmblgluNyknWOzUaB4y2ApKPhq64rhV6MNScwws7hKg3B&shelf=read"

    # Parse the RSS feed
    feed = feedparser.parse(rss_url)
    print(feed.entries[0])

    # Convert the feed to a JSON object
    json_data = json.dumps(feed.entries, indent=4)
    # Convert the JSON string back to a Python object
    data = json.loads(json_data)

    # Print the JSON output
    print(len(data))


if __name__ == "__main__":
    fetchRssData()