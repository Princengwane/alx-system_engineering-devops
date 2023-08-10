#!/usr/bin/python3
"""
Function that queries the Reddit API and prints
the top ten hot posts of a subreddit
"""


import requests

def count_words(subreddit, word_list, after=None, count_dict=None):
    if count_dict is None:
        count_dict = {}

    base_url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    params = {"limit": 100, "after": after}
    headers = {"User-Agent": "Reddit API Scraper"}

    response = requests.get(base_url, params=params, headers=headers)

    if response.status_code != 200:
        print("An error occurred while fetching data from Reddit.")
        return

    data = response.json()
    posts = data["data"]["children"]

    for post in posts:
        title = post["data"]["title"].lower()
        for word in word_list:
            word = word.lower()
            if word in title:
                count_dict[word] = count_dict.get(word, 0) + title.count(word)

    after = data["data"]["after"]
    
    if after is not None:
        count_words(subreddit, word_list, after, count_dict)
    else:
        sorted_counts = sorted(count_dict.items(), key=lambda x: (-x[1], x[0]))
        for keyword, count in sorted_counts:
            print(f"{keyword}: {count}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: {} <subreddit> <list of keywords>".format(sys.argv[0]))
        print("Ex: {} programming 'python java javascript'".format(sys.argv[0]))
    else:
        subreddit = sys.argv[1]
        keywords = sys.argv[2:]
        count_words(subreddit, keywords)
