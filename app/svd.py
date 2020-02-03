from joblib import dump, load
from sklearn import preprocessing
from surprise import SVD,NMF,SVDpp
from surprise import NormalPredictor



hotel_le = load('le_hotel.joblib')
user_le = load('le_user.joblib')
model = load('svd.joblib')

# List of hotels
hotels = hotel_le.transform(hotel_le.classes_)


def predict_top_k(user='Anon',k=10):
    user_id = user_le.transform([user])[0]
    predictions = []
    for h in hotels:
        predictions.append((h,model.predict(user_id,h)[3]))    
    predictions.sort(key=lambda x: x[1], reverse=True)
    just_hotel = [p[0] for p in predictions[0:k]]
    return hotel_le.inverse_transform(just_hotel)

#print(predict_top_k('GlennMiller_11'))
