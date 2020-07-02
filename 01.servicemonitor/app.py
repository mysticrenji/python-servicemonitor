#!/usr/bin/python3

import pandas as pd
import requests
from collections import namedtuple
import os
import time
import glob
import datetime as dt
import schedule


#Initialized tuple to hold the status

df= pd.read_csv("urls.csv")

#Function to check the status is 200/OK and Error is also captured by update the url with 000
def check_website_status(site):
    WebsiteStatus= namedtuple('WebsiteStatus', ['status', 'reason'])
    try:
        response= requests.head(site, timeout=5)
        status= response.status_code
        reason= response.reason
        print(site +"-"+ str(status) )
    except requests.exceptions.ConnectionError:
        status = '000'
        reason = 'ConnectionError'
        print( site +"-"+ str(status) )
    website_status= WebsiteStatus (status,reason)
    return website_status

#Consolidate csv generated in 10 minutes occurances and generate html
def consolidate_csv():
       # csvfiles=glob.glob('./csv/*.csv')
    now = dt.datetime.now()
    ago = now-dt.timedelta(minutes=60)
    listsortedcsv=[]
    i=0
    for root, dirs,files in os.walk('./csv/'):  
        for fname in files:
            if os.path.splitext(fname)[-1] == '.csv':
                path = os.path.join(root, fname)
                st = os.stat(path)    
                mtime = dt.datetime.fromtimestamp(st.st_mtime)
                if mtime > ago:
                
                    print('%s modified %s'%(path, mtime))
                    listsortedcsv.insert(i,path)
                    i=i+1
                #df_from_each_file = (pd.read_csv(path) for f)
                #concatenated_df   = pd.concat(df_from_each_file, ignore_index=True)
               # concatenated_df.to_html('myTable.htm',index=False)
                #htmlTable = df.to_html()
    #combine all files in the listsortedcsv
    combined_csv = pd.concat([pd.read_csv(f) for f in listsortedcsv ],ignore_index=True)
    #export to csv
    #combined_csv.to_csv( "combined_csv.csv", index=False, encoding='utf-8-sig')
    combined_csv.to_html('./staticfiles/index.html',index=False)
    htmlTable = df.to_html()

#Iterating through the dataframes and publish it to a csv
def generate_csv():
    timestr = time.strftime("%Y%m%d-%H%M%S")
    for index,rows in df.iterrows():
        site= rows['url']
        website_status= check_website_status(site);

        df.at[index,'status code'] = website_status.status
        df.at[index,'status reason'] = website_status.reason
        df.at[index,'datetime'] = time.strftime("%Y-%m-%d %I:%M %p")
        df.to_csv("./csv/" + timestr + ".csv", index=False)
    consolidate_csv() 

#Schedule the process for 10 minutes
schedule.every(10).minutes.do(generate_csv) 


while True:
    schedule.run_pending() 
    time.sleep(1) 