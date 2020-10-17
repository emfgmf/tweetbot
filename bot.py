from tweepy import OAuthHandler
from tweepy import API
from tweepy import Cursor
import time
import os

LAST_SEEN_FILE_PATH = 'last_seen.txt'
RETWEET_USER = 'RetweetTrigger' # 'Int_SORSE'

# Our consumer key
# consumer_key = secrets["consumer_key"]
consumer_key = os.environ['CONSUMER_KEY']
# Our consumer secret
# consumer_secret = secrets["consumer_secret"]
consumer_secret = os.environ['CONSUMER_SECRET']
# Our access token
# key = secrets["key"]
key = os.environ['KEY']
# Our access token secret
# secret = secrets["secret"]
secret = os.environ['SECRET']

# Authenticate using OAuth 1a authentication
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(key, secret)

# Get the API object using the defined authentication
api = API(auth)

def read_last_seen():
    # Read file
    with open(LAST_SEEN_FILE_PATH, 'r') as file:
        last_seen_id = int(file.read().strip())
        return last_seen_id

def write_last_seen(last_seen_id):
    with open(LAST_SEEN_FILE_PATH, 'w') as file:
        file.write(str(last_seen_id))
    return
        
def reply():
    # Get all (available) status texts by Int_SORSE after last seen tweet id
    id = read_last_seen()
    new_tweets = []
    new_statuses = Cursor(api.user_timeline, id=RETWEET_USER, since_id=id).items()

    # Add all new statuses since the last seen to list
    for status in new_statuses:
        new_tweets.append(status.id)

    # If there were any new tweets, retweet them
    if len(new_tweets) > 0:
        # Write last status
        write_last_seen(new_tweets[0])

        for id in reversed(new_tweets):
            # Favourite this tweet
            api.create_favorite(id)
            # Retweet
            api.retweet(id)

while True:
    reply()
    time.sleep(60)