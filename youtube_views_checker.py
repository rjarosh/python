'''
This script uses a dictionary of youtube links with title:link format and checks the number
of views using the requests library. It then saves the number of views for each individual
youtube video in a separate csv file. If the number of views increases, twilio tweets an update. 
'''

import requests
import re
import pandas as pd
from datetime import datetime
import time
import tweepy

def twitter():
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    api = tweepy.API(auth)
    return api

# Variables that contains the credentials to access Twitter API
ACCESS_TOKEN = 'fill_in_credentials'
ACCESS_SECRET = 'fill_in_credentials'
CONSUMER_KEY = 'fill_in_credentials'
CONSUMER_SECRET = 'fill_in_credentials'

def check_views(video,link):
    todays_date = datetime.now().strftime('%d-%m')
    now_time = datetime.now().strftime('%H:%M')
    
    df = pd.read_csv(video+'.csv')
    #print(df)
    
    #get the site
    r = requests.get(link)
    text = r.text
    tag = re.compile('\d+ views')
    views = re.findall(tag,text)[0]
    
    #get the digit number of views. It's returned in a list so I need to get that item out
    cleaned_views=re.findall('\d+',views)[0]
    #print(cleaned_views)
    
    #check to see if increase in views from the previous check i.e. the last row of the df
    #first make sure it's not the first time the script has run
    if len(df) > 0:
        if int(cleaned_views) > int(df['Views'][-1:]):
            tweet = f'{todays_date}: {now_time}\nIncrease in views for the "{video.title()}" video! : {cleaned_views} views'
            api = twitter()
            api.update_status(status=tweet)

    
    #append to the df
    df.loc[len(df)] = [todays_date, now_time, int(cleaned_views)]
    #df = df.append([todays_date, now_time, int(cleaned_views)],axis=0)

    
    df.to_csv(video+'.csv',index=False)
    

link_dict = {'link1':'https://youtu.be/link_here',
             'link2':'https://youtu.be/link_here'}

#create original csvs
link1csv = pd.DataFrame(columns=['Date','Time','Views'])
link1csv.to_csv('link1.csv',index=False)

link2csv = pd.DataFrame(columns=['Date','Time','Views'])
link2csv.to_csv('link2.csv',index=False)

#continue to run with a 60 minute break inbetween each loop
while True:
    for k, v in link_dict.items():
        df = check_views(k,v)
    print('Success: ' + datetime.now().strftime('%d-%m at %H:%M'))
    time.sleep(3600)
