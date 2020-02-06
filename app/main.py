import streamlit as st
import numpy as np
import pandas as pd
import time
import svd
import ranking
import numpy as np

import matplotlib.pyplot as plt
plt.rcParams["figure.figsize"] = (7,4)

# CONSTANTS
SEASONS = ('Automne', 'Hiver', 'Éte','Printemps')

TITLE = "Recommandation"
SIDE_TITLE = "Paramètres"




SCORE_FILTERING_MESSAGE = "Filtrer par le score moyen des avis :"
LOCATION_MESSAGE = "Entrez votre position :"
SEASON_DEPARTURE_MESSAGE = "Entrez la période du voyage :"
IDENTIFIER_MESSAGE="Entrez votre identifiant : "
RECENT_REVIEW_MESSAGE = "Privilégier les avis récents."
ACCOUNT_SENT_ANALYSIS_MESSAGE = "Mettre en avant les avis au contenu positif"
HISTORY_MESSAGE = "Utiliser mon historique."
LOADING_MESSAGE = "Patientez un instant."
DETAILS_MESSAGE = "Afficher les détails."

LABEL_BUTTON_SEARCH = "Rechercher"


#Preloading
df_data = pd.read_csv("data/processed_data.csv.zip")

df_data["stay_date"] = pd.to_datetime(df_data["stay_date"])
df_data["gap_stay_today"] = pd.to_timedelta(df_data["gap_stay_today"])


# UI
st.title(TITLE)
st.sidebar.title(SIDE_TITLE)

# Filter by  mean score for each hotel
review_score_threshold = st.sidebar.slider(SCORE_FILTERING_MESSAGE,
                                           min_value=0,
                                           max_value = 5,
                                           step=1)
# User location
user_location = st.sidebar.text_input(LOCATION_MESSAGE)
user_location = user_location if user_location else None

# Season
season = st.sidebar.multiselect(SEASON_DEPARTURE_MESSAGE,SEASONS)
season = season if season else None

use_history = st.sidebar.checkbox(HISTORY_MESSAGE)

user_id = None
if use_history:
    
# Identifier (We should apply less 1 to have the correct id )
    user_id = st.sidebar.text_input(IDENTIFIER_MESSAGE)

# Checkboxes
prioritize = st.sidebar.checkbox(RECENT_REVIEW_MESSAGE)
sent_analysis = st.sidebar.checkbox(ACCOUNT_SENT_ANALYSIS_MESSAGE)
more_details= st.sidebar.checkbox(DETAILS_MESSAGE)




AVERAGE_SCORE = "score"



def recommand(n=20,alpha = 1 ,beta = 1):
   
    df = ranking.rank_from_scores(df_data,
                                         min_score = review_score_threshold,
                                         recency = prioritize,
                                         positivity = sent_analysis,
                                         season=season,
                                         city = user_location)
    df = pd.DataFrame(df)

    
    if user_id: 
        df_svd= svd.predict(user_id)
        df = df.join(df_svd, lsuffix='_caller', rsuffix='_other')
        df[AVERAGE_SCORE] = (alpha  * df[ranking.GLOBAL_SCORES ]) +  (beta* df[svd.SCORE_SVD])
        df[AVERAGE_SCORE] = df[AVERAGE_SCORE]/(alpha+beta)

        return df.nlargest(n, AVERAGE_SCORE, keep='first')

    # st.table(df[ranking.GLOBAL_SCORES ])
    return df.nlargest(n,ranking.GLOBAL_SCORES, keep='first')
    
def recommand_ui():


    def row_to_gui(top_k,detail):


        col_sel = [ranking.GLOBAL_SCORES]
        
        if detail:
            col_sel = top_k.columns.difference([ranking.RECENCY_SCORES,ranking.POSITIVITY_SCORES])
        
        if user_id:
            col_sel.extend([svd.SCORE_SVD,AVERAGE_SCORE])

                    
        for index, row in top_k.iterrows():
            st.table(row[col_sel])

            if detail:
                plt.hist(row[ranking.RECENCY_SCORES])
                plt.title("Distribution de la récence")
                st.pyplot()

                plt.hist(row[ranking.POSITIVITY_SCORES ])
                plt.title("Distribution des scores de positivité")
                st.pyplot()
                
    top_k = recommand() 
    row_to_gui(top_k,more_details)

                    

if st.sidebar.button(LABEL_BUTTON_SEARCH):

    with st.spinner(LOADING_MESSAGE):
        my_bar = st.progress(0)
        for percent_complete in range(100):
            time.sleep(0.05)
            my_bar.progress(percent_complete + 1)
        recommand_ui()
    my_bar.empty()

