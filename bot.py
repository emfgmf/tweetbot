from tweepy import OAuthHandler
from tweepy import API
from tweepy import Cursor
import time
import os

LAST_SEEN_FILE_PATH = './last_seen.txt'
RETWEET_USER = 'RetweetTrigger' # 'Int_SORSE'

# The following four variables must be available as environment variables
# Our consumer key
consumer_key = os.environ['API_KEY']
# Our consumer secret
consumer_secret = os.environ['API_KEY_SECRET']
# Our access token
key = os.environ['ACCESS_TOKEN']
# Our access token secret
secret = os.environ['ACCESS_TOKEN_SECRET']

# Authenticate using OAuth 1a authentication
# See http://docs.tweepy.org/en/v3.9.0/auth_tutorial.html#oauth-1a-authentication
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