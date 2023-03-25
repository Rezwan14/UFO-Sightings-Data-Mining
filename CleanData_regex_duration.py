#Import pandas for reading and analyzing CSV data:
#https://towardsdatascience.com/regular-expressions-regex-with-examples-in-python-and-pandas-461228335670

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re

#read edit file
ufo = pd.read_csv('uforaw.csv')


#drop unnecessary columns
new_ufo = ufo[['city','state','date_time','shape','duration','text',
               'city_latitude','city_longitude']]

new_ufo.dropna(subset=['state'])
#can also just make it based on actual states
new_ufo = new_ufo[new_ufo['state'].str.len() == 2]


new_ufo.dropna(subset=['date_time'])
new_ufo['date_time'] = new_ufo['date_time'].str.replace('T',' ')
new_ufo['date_time'] = pd.to_datetime(new_ufo['date_time'])

#remove older than 2004
new_ufo = new_ufo.loc[(new_ufo['date_time']> '2003-12-31')]
new_ufo['shape'] = new_ufo['shape'].fillna('Missing')

#DROP MISSING SHAPES
#new_ufo = new_ufo.dropna(subset=['shape'])

ufodur = new_ufo
nump = '\d?(-?)(\d?)'
pattern = '(!?(i?)(Sec.*|sec.*|Min.*|min.*|Ho.*|hour.*|hr.*))*'
ufodur['length'] = ufo['duration'].str.replace(pattern, '', regex=True)
ufodur['timeinterval'] = ufo['duration'].str.replace(nump, '', regex=True)
ufodur.head(15)

#rest is null
#cast as int

###time amount

def regexTime(length):
    time_duration = 1
    text = ""
    some = 'i?(Few|few|mere|Mere|some|Some|Couple|couple|Several|several)'
    #some takes lower end
    #if there are multiple numbers, split and average
    if (length is int or length is float): 
        time_duration = length
    else: text = str(length)
    if (len(text) == 0):
        time_duration = 1
        
    if (re.match(some, text)):
        time_duration = 5

    else:
    #findall (\d) and average
    #p = re.compiler(r'\d+') #findall int
        p = re.findall('\d+',text)
        sumP = 0
        for i in p:
            sumP += int(i)

        if (len(p) == 0):
            time_duration = 1
        else:
            average = sumP/len(p)
            time_duration = average
    return time_duration

###time interval
    
def regexInterval(interval):
    time_length = 0
    text = str(interval)
    #define a bunch of patterns for time
    minute = '(Min\w+)|(min\w+)'
    second = '(Sec\w+)|(sec\w+)'
    hour = '(Hour.*)|(hour.*)|(hr.*)|(hrs.*)'

    #case for each minute
    if (re.search(minute,text)):
        time_length = 60
    elif (re.search(second,text)):
        time_length = 1
    elif (re.search(hour,text)):
        time_length = 3600
        
    return time_length


ufodur['newlength']=ufodur['length'].apply(lambda a: regexTime(a))
ufodur['newtime']=ufodur['timeinterval'].apply(lambda a: regexInterval(a))
ufodur['duration_sec'] = (ufodur['newtime']*ufodur['newlength'])
ufodur['duration_sec'].replace(0, np.nan, inplace=True)
ufodur = ufodur.drop(columns=['newlength','newtime','length','timeinterval','duration'])
#print(regexInterval(ufodur['timeinterval'][0]))

#MAPPABLE
map_ufo = ufodur.dropna(subset=['city_latitude'])
map_ufo.to_csv("mapufo.csv",encoding='utf-8', index=False)

#test set

ufodur.to_csv("editufo.csv",encoding='utf-8', index=False)
