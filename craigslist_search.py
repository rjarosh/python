import requests
from bs4 import BeautifulSoup
from datetime import datetime
import tweepy
import pandas as pd


def twitter():
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    api = tweepy.API(auth)
    return api

def hours_in_dt(dt):
    #return the hours in a timedelta
    return dt.seconds/3600
'''
This script can be set to run as frequently as you'd like (using crontab, scheduler, etc)
It will log all the items that are returned, save as CSV file, and if there's a new item,
it will update the tweepy twitter api and tweet the link for the new item(s).
'''

# Variables that contains the credentials to access Twitter API
ACCESS_TOKEN = ''
ACCESS_SECRET = ''
CONSUMER_KEY = ''
CONSUMER_SECRET = ''
api = twitter()

#fill in the search query here
link="https://tampa.craigslist.org/search/sss?query=SEARCH_TERMS_HERE&srchType=T"

r=requests.get(link)
soup=BeautifulSoup(r.text,'html.parser')
listings=soup.find_all('li',{"class":"result-row"})

now=datetime.now()
tweet="NEW ORGAN LISTINGS: \n\n"

try:
    df=pd.read_csv('craigslist_organs.csv')
except:
    df=pd.DataFrame(columns=['Item','Price','Post ID','Link','Date Posted'])

    
for x in range(len(listings)):
    date_listed=listings[x].find('time').get('datetime')
    date_cleaned=datetime.strptime(date_listed,'%Y-%m-%d %H:%M')
    time_delta=now-date_cleaned
    item=listings[x].find('h3',{"class":"result-heading"}).text.strip()
    try:
        price=listings[x].find('span',{'class':'result-price'}).text
    except:
        price='$0'

    link=listings[x].find('a').get('href')
    post_id=listings[x].find('a',{'class':'result-title hdrlnk'}).get('data-id')
        
    if int(post_id) not in df['Post ID'].unique():
        #first update the df
        df.loc[len(df)] = [item,price,post_id,link,date_cleaned]
        #prep the tweet
        #shorten long item names
        if len(item) > 8:
            item=item[0:7]+'...'
        tweet+=item + ' ' + price + '\n' + link + '\n* * *\n\n'
df.to_csv('craigslist_organs.csv',index=False)
if tweet != "NEW ORGAN LISTINGS: \n\n":
        api.update_status(tweet[0:279])
        


