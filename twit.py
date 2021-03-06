import twitter
import json

TEST_HANDLE = "abruptus9"
KEYWORDS = ["commission", "comm", "slot", "badge", "request", "ych"]

# TODO: Rearrange methods in a way that makes sense
# TODO: Detect when comms are closed
# TODO: Time-sensitive opening posts & count closed if later closed
# TODO: Consolidate data into one method

def initialize_api():
    api = None
    with open('keys.json') as key_file:
        key_data = json.load(key_file)
        twitter_keys = key_data["twitter"]
        api = twitter.Api(consumer_key=twitter_keys['consumer_key'],
                  consumer_secret=twitter_keys['consumer_secret'],
                  access_token_key=twitter_keys['access_token'],
                  access_token_secret=twitter_keys['access_token_secret'])
    return api

def get_latest_tweets(api=None, screen_name=None, num_tweets=100):
    tweets = api.GetUserTimeline(screen_name=screen_name, count=num_tweets)
    return tweets

def find_commission_info_in_latest_tweets(api=None, screen_name=None, num_tweets=100):
    tweets = get_latest_tweets(api=api, screen_name=screen_name, num_tweets=num_tweets)
    commission_open_tweets = []
    for tweet in tweets:
        if tweet.text.startswith("@") or tweet.text.startswith("RT @"):
            continue
        if are_commissions_open_from_text(tweet.text):
            commission_open_tweets.append(tweet.text.replace("\n", " "))
            #print("[[OPEN " + tweet.created_at + "]]: \n" + tweet.text.replace("\n", " "))
        # if "full" in tweet.text.lower() and [k for k in KEYWORDS if k in tweet.text.lower()]:
        #     print("[CLOSED]: " + tweet.text)
    return commission_open_tweets


def get_user_data(api=None, screen_name=None):
    user = api.GetUser(screen_name=screen_name)
    description = user.description
    name = user.name
    consolidated_text = description + " | " + name
    return consolidated_text


def are_commissions_open_from_text(text):
    text = text.lower()
    if any([k for k in KEYWORDS if k in text]):
        # print(consolidated_text)
        if "open" in text:
            if not "not" in text.split("open")[0]:
                return True
    return False

def determine_if_commissions_are_open(api=None, screen_name=None):
    print(screen_name)
    user_data = get_user_data(api, screen_name)
    return bool(are_commissions_open_from_text(user_data) or find_commission_info_in_latest_tweets(api, screen_name))


# Debugging    
if __name__ == "__main__":
    api = initialize_api()
    for handle in ["abruptus9", "Allosaurex", "DragonJourney", "VaneEltin", "mervvin_art", "HigsbyTheDeer"]:
        #get_user_data(api=api, screen_name=handle)
        #find_commission_info_in_latest_tweets(api=api, screen_name=handle)
        print(determine_if_commissions_are_open(api, handle))
        print("\n=======\n")

