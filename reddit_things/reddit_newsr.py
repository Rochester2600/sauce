#!/usr/bin/env python3
# ---------------------------------------------------------
# a script to snarf a list of reddits, sorted by creation
# time.
# ---------------------------------------------------------
import requests
import psycopg2
from time import sleep

# ---------------------------------------------------------
# variables
# ---------------------------------------------------------
# reddit api vars
api_url = 'http://www.reddit.com/subreddits/new/.json'
api_params = {'limit':'100'}
api_timeout = 3    # number of seconds to wait before giving up
api_delay = 2        # number of seconds to wait between requests

# required headers to avoid rate limiting by reddit api
req_headers = {
        'User-Agent': 'Subreddit lister script by rossja',
        'X-Contact-Email': 'algorythm@gmail.com'
}

# database vars
dbhost = 'localhost'
dbname = 'redspy'
dbuser = 'redspy'
dbpass = 'redspy'


# ---------------------------------------------------------
# set up us the code
# ---------------------------------------------------------
def main():

    # connect to the database
    #print("connecting to database...")
    db = psycopg2.connect(
        host = dbhost,
        dbname = dbname,
        user = dbuser,
        password = dbpass
    )

    #if db:
    #    print("connected")

    # make the request to the reddit API
    try:
        json = requests.get(
            api_url,
            params=api_params,
            timeout=api_timeout,
            headers=req_headers
        ).json()

        # parse the JSON response
        newsr = parse_json(json)

        # add the results to the database
        for url in newsr:
            #print("'{0}','{1}'".format(url,newsr[url]))
            add2db(db, url, newsr[url])

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

# ---------------------------------------------------------
# parse the JSON response from the reddit API
# ---------------------------------------------------------
def parse_json(json):
    #print(json.keys())
    sr = {}
    for child in json['data']['children']:
        title = child['data']['title']
        url = 'http://reddit.com' + child['data']['url']
        #print("'{0}','{1}'".format(url,title))
        sr[url] = title
    return(sr)


# ---------------------------------------------------------
# add data to the database
# ---------------------------------------------------------
def add2db(db, url, title):
        cur = db.cursor()
        #print("adding data: '{0}','{1}'".format(url,title))
        try:
            cur.execute("insert into newsr(url, descr) values (%s,%s)", (url, title,))
        except psycopg2.IntegrityError:
            db.rollback()
        else:
            db.commit()


# ---------------------------------------------------------
# OMG! MAIN!
# ---------------------------------------------------------
if __name__ == "__main__":    main()
