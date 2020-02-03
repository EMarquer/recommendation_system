import streamlit as st
import numpy as np
import pandas as pd


"""
# Recommandation

"""


option = st.sidebar.selectbox("Which recommender system do you want to use?",
     ["Memory based","Model based"])



user_city = st.sidebar.text_input("What is your current Location ?")

user_id = st.sidebar.text_input("What is your user id ?")

trip_date = st.sidebar.date_input("When will you arrive ?", value=None, key=None)


review_filter = st.sidebar.slider("Filter by score review:",min_value=0,max_value = 5,step=1)


st.image('210996409.jpg',use_column_width=True)

df = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [43.76, -115.4],
    columns=['lat', 'lon'])
st.map(df)


df = pd.read_csv('false_sample.csv')
st.table(df)




def recommendation(user_id ,user_city,trip_date,review_criterion):
    pass


