'''
used when i was having intermittent drops due to a broken ont from the isp
'''

import os
import time
from datetime import datetime
import pandas as pd

df = pd.Series(['STARTED AT ' + datetime.now().strftime('%D, %H:%M:%S') + '\n' + 'FAILED PINGs: \n'])
df.to_csv('ping_results.csv')

count_machine=0
while True:
    a=os.system("ping -c 1 192.168.254.254")
    if a != 0:    
        message ='***** ' + datetime.now().strftime('%D, %H:%M:%S') + ' PING FAILED'
        df=df.append(pd.Series([message]))
        df.to_csv('ping_results.csv')
        print(message)
    count_machine += 1
    if count_machine == 300:
        print(datetime.now().strftime('%D, %H:%M:%S') + ' Still working...')
        count_machine = 0
    time.sleep(1)
