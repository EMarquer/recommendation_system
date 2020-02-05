import streamlit as st
import numpy as np
import pandas as pd
import time
import svd



# CONSTANTS
SEASONS = ('Automne', 'Hiver', 'Éte','Printemps')

TITLE = "Recommandation"
SIDE_TITLE = "Paramètres"

SCORE_FILTERING_MESSAGE = "Filtrer par le score moyen des avis :"
LOCATION_MESSAGE = "Entrez votre position :"
SEASON_DEPARTURE_MESSAGE = "Quand souhaitez-vous partir ?"
IDENTIFIER_MESSAGE="Taper votre identifiant : "
RECENT_REVIEW_MESSAGE = "Je souhaite privilégier les avis récents."
ACCOUNT_SENT_ANALYSIS_MESSAGE = "Je souhaite utiliser la valence émotionelle du contenu des avis."
HISTORY_MESSAGE = "Je souhaite utiliser mon historique."
LOADING_MESSAGE = "Patientez un instant."
DETAILS_MESSAGE = "Je souhaite voir les détails."

LABEL_BUTTON_SEARCH = "Rechercher"

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

# Season
season = st.sidebar.multiselect(SEASON_DEPARTURE_MESSAGE,SEASONS)


use_history = st.sidebar.checkbox(HISTORY_MESSAGE)

if use_history:
    
# Identifier (We should apply less 1 to have the correct id )
    user_id = st.sidebar.number_input(
        IDENTIFIER_MESSAGE,
        step = 1,min_value=0,value=0
    )

# Checkboxes
prioritize = st.sidebar.checkbox(RECENT_REVIEW_MESSAGE)
sent_analysis = st.sidebar.checkbox(ACCOUNT_SENT_ANALYSIS_MESSAGE)
more_details= st.sidebar.checkbox(DETAILS_MESSAGE)



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

if st.sidebar.button(LABEL_BUTTON_SEARCH):

    with st.spinner(LOADING_MESSAGE):
        my_bar = st.progress(0)
        for percent_complete in range(100):
            time.sleep(0.05)
            my_bar.progress(percent_complete + 1)
        recommand_ui()
    my_bar.empty()

