# -*- coding: utf-8 -*-
"""
Created on Fri Nov  3 11:39:50 2017

@author: agill
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pymysql as sql
from matplotlib.animation import FuncAnimation

rmax = 140

hostname = 'smtcosvm05.mwo.local'
username = 'reader'
password = 'mwo231'

def animate(i):
    
    #clearing data off of the previous chart so that the data does not build up and kill memory
    ax.clear()
    
    #declaring empty list to put MySQL data into
    TmStamp   = []
    Max_inH20 = []
    Min_inH20 = []
    Max_mph   = []
    Min_mph   = []

    #Connecting to the database
    myConnection = sql.connect(host=hostname, user=username, passwd=password)
    
    #creating database cursor that can navigate around
    cur = myConnection.cursor()

    #The data query
    cur.execute("SELECT TmStamp, max(SETRA0TO30_0970_DIFFP_INWC_Max), min(SETRA0TO30_0970_DIFFP_INWC_Min), (max(SETRA0TO30_0970_WS_KTS_Max)*1.15), (min(SETRA0TO30_0970_WS_KTS_Max)*1.15) \
                FROM loggerNetRaw.SMTB_SETRA0TO30_0970 where TmStamp between curdate() and curdate()+1 \
                group by year(TmStamp), month(TmStamp), date(TmStamp), hour(TmStamp), minute(TmStamp);")

    #Pulling data from the darabase
    results = cur.fetchall()

    #Filling the empty list with the data retrieved
    for row in results:
        TmStamp.append(row[0])
        Max_inH20.append(row[1])
        Min_inH20.append(row[2])
        Max_mph.append(row[3])
        Min_mph.append(row[4])
    
    #Adding the list into a dataframe so that it will be much easier to work with
    df = pd.DataFrame({'A':TmStamp, 
                       'B':Max_inH20, 
                       'C':Min_inH20, 
                       'D':Max_mph, 
                       'E':Min_mph})

    #Renaiming the colunms so that they will stay the same every dataquery. more of a fail safe really
    df.columns = ['TmStamp', 'Max_inH20', 'Min_inH20', 'Max_mph', 'Min_mph']
    
    #Turning the date string into a date time formate python can read
    df['TmStamp'] = pd.to_datetime(df['TmStamp'])

    #Creating a new dataframe where the index(minute of day) is changed to degrees then radians to be able to be plotted on 
    #circular chart
    indexed_df = df.set_index((df.index*(360/1440))*(np.pi/180))

    #resetting variables so I dont have to type in the whole variable every time I need it
    x  = indexed_df.index
    y1 = indexed_df['Max_inH20']
    y2 = indexed_df['Min_inH20']
    x1 = indexed_df['Max_mph']
    x2 = indexed_df['Min_mph']

    #creating the text for the peak wind in the cener of the chart
    text = '%1.f mph/%1.f kts'%(max(x1), (max(x1)/1.15))

    #Creating the time stamp for the center as well as finding the point on the chart where the peak gust occured
    peak_time_index = indexed_df.loc[indexed_df['Max_mph'].idxmax()]
    peak_time = peak_time_index['TmStamp']
    peak_tm_text = '%s'%(peak_time)
    gust_point = peak_time_index.name
    
    #all the graph stuff
    ax.set_theta_zero_location('N')
    ax.fill_between(x, x1, x2, color="red", alpha=.85)
    ax.set_rmax(rmax)
    ax.set_rgrids([10,20,30,40,50,60,70,80,90,100,110,120,130,140], angle=(45.))
    ax.set_xticks(np.linspace(0, 2*np.pi, 24, endpoint=False))
    ax.set_xticklabels(range(24))

    #Changing the center of the graph as well as all the titles
    ax.set_rorigin(-rmax * 0.3)
    ax.set_xlabel('Wind Speed MPH (red)/Hour of day (outside numbers)')
    ax.set_title('Hays Wind Chart')
    ax.text(1,-11, 'Mt. Washington Observatory', fontsize=6)
    
    #Peak gust arrow
    ax.annotate('Peak Gust', xy=(gust_point,(max(x1))), xytext=(gust_point,(max(x1)+20)), 
            arrowprops=dict(facecolor='black', shrink=0.05))
    
    #changing font size of peak wind gust for when the winds go over 100mph
    if max(x1)>100:
        ax.text(-11,-8, text, fontsize=12)
    else:
        ax.text(-11,-8, text, fontsize=15)
    ax.text(-10.5, -15, peak_tm_text, fontsize=8)

#Figure Stuff
    
fig = plt.figure(figsize=(11,11))
ax = fig.add_subplot(111, projection='polar')
ani = FuncAnimation(fig, animate, interval = 5000)
plt.show()
