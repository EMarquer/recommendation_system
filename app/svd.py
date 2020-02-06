from joblib import dump, load
from sklearn import preprocessing
from surprise import SVD,NMF,SVDpp
from surprise import NormalPredictor
import pandas as pd



SCORE_SVD = "D'après vos précédents avis, cet hôtel obtiendrait une note (note de 0 à 5) :" 



hotel_le = load('app/le_hotel.joblib')
user_le = load('app/le_user.joblib')
model = load('app/svd.joblib')

# List of hotels
hotel_list = hotel_le.transform(hotel_le.classes_)

def predict(user='Anon'):
    user_id = user_le.transform([user])[0]
    predictions = []

    for h in hotel_list:
        predictions.append((h,model.predict(user_id,h)[3]))    
    predictions.sort(key=lambda x: x[1], reverse=True)

    hotels, scores = zip(*predictions)

    df = pd.DataFrame()
    #df['hotel_id'] =  hotel_le.inverse_transform(hotels)
    df['hotel_id'] =  hotels
    df[SCORE_SVD] = scores

    df = df.set_index('hotel_id')
    return df

print(predict('GlennMiller_11'))
