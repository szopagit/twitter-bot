import requests
from requests_oauthlib import OAuth1
from load_data import load_data_for_post
import os

def post_wallet():


    content = load_data_for_post()
    url = "https://api.twitter.com/2/tweets"
    API_KEY = os.getenv("API_KEY")
    API_SECRET = os.getenv("API_SECRET")
    ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
    ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")
    auth = OAuth1(
        API_KEY,
        API_SECRET,
        ACCESS_TOKEN,
        ACCESS_TOKEN_SECRET
    )

    response = requests.post(
        url,
        json={"text": content},
        auth=auth
    )

    response.raise_for_status()

if __name__ == "__main__":
    post_wallet()