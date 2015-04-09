#!/usr/bin/env python3
# ---------------------------------------------------------
# a script to snarf submitted posts by a specific user
# ---------------------------------------------------------
import sys
import requests
from time import sleep

if (len(sys.argv) < 2) or (sys.argv[1] == ""):
  print("you need to provide a reddit user name")
  sys.exit(1)
else:
  rusr = sys.argv[1]

# ---------------------------------------------------------
# variables
# ---------------------------------------------------------
api_url = "http://www.reddit.com/user/{0}/submitted/.json".format(rusr)
api_params = {'limit':'100'}
api_timeout = 3  # number of seconds to wait before giving up
api_delay = 2    # number of seconds to wait between requests
req_headers = {
  'User-Agent': 'List user posts script by rossja',
  'X-Contact-Email': 'algorythm@gmail.com'
}

# ---------------------------------------------------------
# set up us the code
# ---------------------------------------------------------
def main():

  try:
    json = requests.get(
      api_url,
      params=api_params,
      timeout=api_timeout,
      headers = req_headers
    ).json()
    parse_json(json)

  except requests.exceptions.Timeout:
    # request timed out
    print("Timed out, your network sucks")
    sys.exit(1)

  except requests.exceptions.TooManyRedirects:
    # request got lost in redirect responses
    print("OMG! Too many redirects, ragequitting")
    sys.exit(1)

  except requests.exceptions.RequestException as e:
    # something else borked
    print(e)
    sys.exit(1)

def parse_json(json):
  #print(json.keys())
  for child in json['data']['children']:
    subreddit = child['data']['subreddit']
    posturl = child['data']['url']
    print("'{0}','{1}'".format(subreddit,posturl))

# ---------------------------------------------------------
# OMG! MAIN!
# ---------------------------------------------------------
if __name__ == "__main__":  main()
