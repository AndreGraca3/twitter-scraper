from datetime import datetime
from twikit import Client
import requests
import os
import json
from dotenv import load_dotenv

# Load and read environment variables from .env file
load_dotenv()
username = os.getenv("USERNAME")
email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")
webhook_url = os.getenv("WEBHOOK_URL")
user_id = os.getenv("USER_ID")

# Initialize client
client = Client('en-US')

# Login to Twitter and save cookies
try:
    print("Loading cookies...")
    client.load_cookies('cookies.json')
except:
    print("No cookies found, logging in...")
    client.login(
        auth_info_1=username ,
        auth_info_2=email,
        password=password
    )
    client.save_cookies('cookies.json')

def fetch_latest_tweet():
    tweets = client.get_user_tweets(user_id, "Tweets", 1)
    return tweets[0]

def check_for_new_tweet():
    latest_tweet = fetch_latest_tweet()
    with open("last_tweet_id.txt", "r+") as file:
        last_tweet_id = file.read()
        if(latest_tweet.id != last_tweet_id):
            file.seek(0)
            file.write(latest_tweet.id)
            file.truncate()
            return latest_tweet
        else:
            return None

def main():
    new_tweet = check_for_new_tweet()
    if new_tweet:
        tweeted_at = datetime.strptime(new_tweet.created_at, '%a %b %d %H:%M:%S %z %Y')
        message = {
            "embeds": [
                {
                    "type": "link",
                    "description": new_tweet.text,
                    "color": 16711680,
                    "fields": [
                        {
                            "name": "🕒",
                            "value": f"**{tweeted_at.strftime('%H:%M:%S')}**",
                            "inline": True
                        },
                        {
                            "name": "🗨️",
                            "value": f"**{new_tweet.reply_count}**",
                            "inline": True
                        },
                        {
                            "name": "🔁",
                            "value": f"**{new_tweet.retweet_count}**",
                            "inline": True
                        },
                        {
                            "name": "❤️",
                            "value": f"**{new_tweet.favorite_count}**",
                            "inline": True
                        },
                        {
                            "name": "📈",
                            "value": f"**{new_tweet.view_count}**",
                            "inline": True
                        }
                    ],
                    "footer": {
                        "text": "Powered by Graça",
                        "icon_url": "https://i.imgur.com/fL67hTu.jpeg"
                    }
                }
            ],
        }
        video = None
        if(new_tweet.media):
            if(new_tweet.media[0]["type"] == "photo"):
                message["embeds"][0]["image"] = {"url": new_tweet.media[0]["media_url_https"]}
            if(new_tweet.media[0]["type"] == "video"):
                variant = next(variant for variant in new_tweet.media[0]["video_info"]["variants"] if variant["content_type"] == "video/mp4")
                video = variant["url"]
        requests.post(webhook_url, json=message)
        if(video):
            requests.post(webhook_url, json={"content": video})
    else:
        print("No new tweets found")

if __name__ == "__main__":
    main()