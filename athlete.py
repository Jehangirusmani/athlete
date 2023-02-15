# -*- coding: utf-8 -*-
"""
Created on Sun Feb 12 14:46:02 2023

@author: JEHANGIR
"""
import pandas as pd
import numpy as np
import streamlit as st
import matplotlib as plt
st.set_page_config (layout="wide")
 
st.title('Athlete All Data')

file_athlete = r'C:\Users\JEHANGIR\OneDrive\Desktop\KHI AI All lectures\Lecture 5\Assignment 3\athlete_events.csv'
file_noc = r'C:\Users\JEHANGIR\OneDrive\Desktop\KHI AI All lectures\Lecture 5\Assignment 3\noc_regions.csv'
df = pd.read_csv(file_athlete)
df1 = pd.read_csv(file_noc)
df2 = pd.merge(df,df1,on='NOC',how='left')

print(df.isnull().sum())

df2['Age']= df2['Age'].fillna(df['Age'].mean())
df2['Medal'] = df2['Medal'].fillna('NA')

#df2['Medal'].unique()  # NA, Gold, Bronze, Silver
# df2['Gold_Medal'] = df2[df2['Medal']=='Gold']   >> counter check 

df2['Gold_Medal'] = df2['Medal'].apply(lambda x: 1 if x == 'Gold' else None)
df2['Silver_Medal'] = df2['Medal'].apply(lambda x: 1 if x == 'Silver' else None)
df2['Bronze_Medal'] = df2['Medal'].apply(lambda x: 1 if x == 'Bronze' else None)

unique_ID = df2['ID'].nunique() # 135571 unique part. and 271116 total data part.
Country_counts = df2['Team'].value_counts()

with st.container():
    col1=st.columns(1)
    countries = df2['region'].unique()
    selected_country = st.selectbox('Select Your Country', countries)
    subset_1 = df2[df2['region']==selected_country]

with st.container():
    col2, col3, col4, col5 = st.columns(4)
    with col2:
        col2.metric('Paticipants Total',subset_1['ID'].nunique())
        col3.metric('Gold Medals',subset_1['Gold_Medal'].count())
        col4.metric('Silver Medals',subset_1['Silver_Medal'].count())
        col5.metric('Bronze Medals',subset_1['Bronze_Medal'].count())
    
with st.container():
    col1, col2, col3 = st.columns(3)
    with col1:
        Gold_Line = subset_1.groupby('Year')['Gold_Medal'].count()
        Silver_Line = subset_1.groupby('Year')['Silver_Medal'].count()
        Bronze_Line = subset_1.groupby('Year')['Bronze_Medal'].count()
        plt.plot(Gold_Line.index, Gold_Line.values, label="Line 1")
        plt.plot(Silver_Line.index, Silver_Line.values, label="Line 2")
        plt.plot(Bronze_Line.index, Bronze_Line.values, label="Line 3")
        st.set_option('deprecation.showPyplotGlobalUse', False)
        col1.pyplot()
    with col2:
        Horizontal_Medal = subset_1[subset_1['Medal'] != 'NA']
        Name_Athlete = Horizontal_Medal.groupby('Name')['Medal'].count().sort_values(ascending=False).head(5)
        plt.barh(Name_Athlete.index, Name_Athlete.values)
        col2.pyplot()
    with col3:
        Medals_Sport = Horizontal_Medal.groupby('Sport')['Medal'].count().sort_values(ascending=False).head(5)
        col3.table(Medals_Sport)

with st.container():
    col1, col2, col3 = st.columns(3)
    with col1:
        plt.hist(x='Age',data=subset_1, bins=30, color='green')
        plt.title('xyz')
        plt.xlabel('kdjbvde')
        plt.ylabel('Frequency')
        col1.pyplot()
    with col2:
        Gender_Medals = Horizontal_Medal.groupby(['Sex', 'Medal'])['Medal'].count() #after sex, medal denotes to show gender wise
        fig = plt.pie(Gender_Medals, labels=Gender_Medals.index, autopct='%2f')
        col2.pyplot()
    with col3:
        Season_Medals = Horizontal_Medal.groupby('Season')['Medal'].count()
        plt.title('Vertical Bar Chart')
        plt.xlabel('Season')
        plt.ylabel('Medals')
        plt.bar(Season_Medals.index, Season_Medals.values, color='blue')
        col3.pyplot()

