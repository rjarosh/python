import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from twilio.rest import Client
import time
import json

# the following line needs your Twilio Account SID and Auth Token
client = Client("credentials_here", "credentials_here")

link = "https://www.cvs.com/immunizations/covid-19-vaccine/immunizations/covid-19-vaccine.vaccine-status.FL.json?vaccineinfo"
master_df = pd.DataFrame(columns=['city','status'])

#set counter to make sure only first time df is created
#set city counters so I only get 1 text per city
counter = 0
tampa = 0
plant = 0
sarasota = 0
lakeland = 0
riverview = 0
brandon = 0

while True:
    try:
        r = requests.get(link)
        soup = BeautifulSoup(r.content,'html.parser')

        data_list = []
        data_dict = {}

        d=json.loads(soup.text)

        for x in range(len(d['responsePayloadData']['data']['FL'])):
            temp=dict(d['responsePayloadData']['data']['FL'][x])
            data_dict['city'] = temp['city']
            data_dict['status'] = temp['status']
            data_list.append(data_dict.copy())

        t = datetime.now().strftime('%m/%d, %H:%M')
        df = pd.DataFrame(columns=['city','status'],data=data_list)

        if (tampa == 0) & (df[df['city']=='TAMPA']['status'].str.contains('Available').any()):
            print(f'Vaccine available in BRADENTON: {t}!')
            client.messages.create(to="+phonenumber", from_="+phonenumber", body="CVS Vaccine availabe in TAMPA!")
            tampa += 1

        if (plant == 0) & (df[df['city']=='PLANT CITY']['status'].str.contains('Available').any()):
            print(f'Vaccine available in PLANT CITY: {t}!')
            client.messages.create(to="+phonenumber", from_="+phonenumber", body="CVS Vaccine availabe in PLANT CITY!")
            plant+=1
        
        if (riverview == 0) & (df[df['city']=='RIVERVIEW']['status'].str.contains('Available').any()):
            print(f'Vaccine available in RIVERVIEW: {t}!')
            client.messages.create(to="+phonenumber", from_="+phonenumber", body="CVS Vaccine availabe in TAMPA!")
            tampa += 1
            
        if (brandon == 0) & (df[df['city']=='BRANDON']['status'].str.contains('Available').any()):
            print(f'Vaccine available in BRANDON: {t}!')
            client.messages.create(to="+phonenumber", from_="+phonenumber", body="CVS Vaccine availabe in TAMPA!")
            tampa += 1
        
        #currently interested in only the above cities
        """
        if (sarasota == 0) & (df[df['city']=='SARASOTA']['status'].str.contains('Available').any()):
            print(f'Vaccine available in SARASOTA: {t}!')
            client.messages.create(to="+phonenumber", from_="+phonenumber", body="CVS Vaccine availabe in SARASOTA!")
            sarasota+=1

        if (lakeland == 0) & (df[df['city']=='LAKELAND']['status'].str.contains('Available').any()):
            print(f'Vaccine available in LAKELAND: {t}!')
            client.messages.create(to="+phonenumber", from_="+phonenumber", body="CVS Vaccine availabe in LAKELAND!")
            lakeland+=1

        
        if df[df['city']=='BRADENTON']['status'].str.contains('Available').any():
            print(f'Vaccine available in BRADENTON: {t}!')
            client.messages.create(to="+phonenumber", from_="+phonenumber", body="Vaccine availabe in BRADENTON!")

        if df[df['city']=='DAYTONA BEACH']['status'].str.contains('Available').any():
            print(f'Vaccine available in DAYTONA: {t}!')
            client.messages.create(to="+phonenumber", from_="+phonenumber", body="Vaccine availabe in DAYTONA BEACH!")

        if df[df['city']=='LAKELAND']['status'].str.contains('Available').any():
            print(f'Vaccine available in LAKELAND: {t}!')
            client.messages.create(to="+phonenumber", from_="+phonenumber", body="Vaccine availabe in LAKELAND!")

        if df[df['city']=='PLANT CITY']['status'].str.contains('Available').any():
            print(f'Vaccine available in PLANT CITY: {t}!')
            client.messages.create(to="+phonenumber", from_="+phonenumber", body="Vaccine availabe in PLANT CITY!")
        """

        if counter == 0:
            master_df = df

        master_df[t]=df['status']
        counter+=1

        master_df.to_csv('vaccine_availability2.csv')
        print(f'Last run: {t}')

        time.sleep(60)
    except:
        time.sleep(10)
        continue

