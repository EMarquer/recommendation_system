import streamlit as st
import numpy as np
import pandas as pd
import time
import svd

"""
# Recommandation

"""


# Sidebar definition

# Title of the sidebar
st.sidebar.title("Parameters")

# Filter by  mean score for each hotel
review_score_threshold = st.sidebar.slider("Filter by score review:",min_value=0,max_value = 5,step=1)


# User location
user_location = st.sidebar.text_input("Enter your city location?")

# Season
season = st.sidebar.multiselect(
    'when do you want to leave',
    ('Autumn', 'Winter', 'Summer','Spring'))


use_history = st.sidebar.checkbox("I want to use my history.")

if use_history:
    

# Identifier (We should apply less 1 to have the correct id )
    user_id = st.sidebar.number_input(
        "Enter your user id:",
        step = 1,min_value=0,value=0
    )

prioritize = st.sidebar.checkbox("I want to prioritize the recent review.")

sent_analysis = st.sidebar.checkbox("I want to use the content of the review.*")

#if sent_analysis:
#    sentiment = st.sidebar.radio("Choose the posivity score.",(':smiley', 'Drama', 'Documentary'))


def recommand_ui():
    res = recommand()
    if not res:
        df = pd.DataFrame()
        df['hotel'] = [543]
        df['score'] = [4]
        st.table(df)
    else:
        st.table(res)

                    
def recommand(): 
    pass


if st.sidebar.button('Recommend me hotels'):

    with st.spinner('Wait for it...'):
        my_bar = st.progress(0)
        for percent_complete in range(100):
            time.sleep(0.05)
            my_bar.progress(percent_complete + 1)
        recommand_ui()
    st.success('Done!')
    my_bar = None






#      ["Memory based","Model based"])



# user_city = st.sidebar.text_input("What is your current Location ?")

# user_id = st.sidebar.text_input("What is your user id ?")

# trip_date = st.sidebar.date_input("When will you arrive ?", value=None, key=None)


# review_filter = st.sidebar.slider("Filter by score review:",min_value=0,max_value = 5,step=1)


# #st.image('210996409.jpg',use_column_width=True)

# df = pd.DataFrame(
#     np.random.randn(1000, 2) / [50, 50] + [43.76, -115.4],
#     columns=['lat', 'lon'])
# st.map(df)


# #df = pd.read_csv('false_sample.csv')
# #st.table(df)




# def recommendation(user_id ,user_city,trip_date,review_criterion):
#     pass


