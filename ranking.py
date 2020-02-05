import typing as t
import pandas as pd
from math import exp, tanh

SPRING, SUMMER, AUTUMN, WINTER = "printemps", "été", "automne", "hiver"
GLOBAL_SCORES = "recomender system score"
AVERAGE_SCORES = "average user score"
RECENCY_SCORES = "recency distribution"
POSITIVITY_SCORES = "positivity distribution"
NUM_MATCHING_RATINGS = "nombre d'avis correspondant aux filtres"

def rank_from_scores(df: pd.DataFrame,
        city: t.Optional[str]=None,
        min_score: int = 0,
        #user_based_score: t.Optional[t.Dict[int, float]]=None,  # dict of hotel label-encoded id to score
        season: t.Optional[t.Iterable[str]]=None,  # if no season is specified, no filter is applied 
        recency: bool=True,
        positivity: bool=True) -> pd.Series:

    # filter-out the locations that do not match the provided one
    if city is not None:
        is_location = df["city"] == city
        print(f"filter by location: old {len(df)}, new {is_location.sum()}")
        df = df[is_location]

    # filter-out the times that do not match the provided one
    if season is not None:
        month = df["stay_date"].dt.month
        is_season = month.isin(
            ({3, 4, 5} if SPRING in season else set()).union(
                {6, 7, 8} if SUMMER in season else set()
            ).union(
                {9, 10, 11} if AUTUMN in season else set()
            ).union(
                {12, 1, 2} if WINTER in season else set()
            ))
        
        print(f"filter by season: old {len(df)}, new {is_season.sum()}")
        df = df[is_season]

    # --- compute the base score value of the review ---
    scores = df["rating"]

    # ponderate the scores by the recency of the review (exp(-x), x being the number of days since the review was posted)
    recency_multiplier = df["gap_stay_today"].dt.days.apply(lambda days: exp(-days))

    # ponderate with the positivity scores
    positivity_scores = (df["text_polarity"] * (1 - df["text_objectivity"]))
    positivity_scores += (df["title_polarity"] * (1 - df["title_objectivity"]))
    positivity_scores /= 2

    # weighted average
    def process_hotel(group):
        indexes = group.index

        # compute the full weights to apply
        # the full weights are the products of all the partial weights used, allways at least the expertise
        
        # the expertise (+1 because it start at 0) is the base weight 
        expertise_weight = 1 + df['user_expertise'][indexes]
        weights = expertise_weight

        # add the recency weighting if necessary
        if recency:
            recency_multiplier_group = recency_multiplier[indexes]
            weights *= recency_multiplier_group

        # add the recency weighting if necessary
        if positivity:
            positivity_scores_group = positivity_scores[indexes]
            weights *= positivity_scores_group

        # return the weighted scores
        scores = group
        return (scores * weights).sum() / weights.sum()
    
    # compute the score of each hotel
    final_scores = scores.groupby(df["hotel"][scores.index]).apply(process_hotel)
    final_scores = final_scores.rename(GLOBAL_SCORES)
    final_scores = final_scores.to_frame()

    # add the average score per hotel
    average_scores = df["rating"][scores.index].groupby(df["hotel"][scores.index]).mean()
    average_scores = average_scores.rename(AVERAGE_SCORES)
    final_scores = final_scores.join(average_scores)

    # add the recency distribution per hotel
    recency_multiplier_hotel = recency_multiplier[scores.index].groupby(df["hotel"][scores.index]).apply(list)
    recency_multiplier_hotel = recency_multiplier_hotel.rename(RECENCY_SCORES)
    final_scores = final_scores.join(recency_multiplier_hotel)
    
    # add the number of ratings per hotel
    num_ratings_hotel = recency_multiplier[scores.index].groupby(df["hotel"][scores.index]).apply(len)
    num_ratings_hotel = num_ratings_hotel.rename(NUM_MATCHING_RATINGS)
    final_scores = final_scores.join(num_ratings_hotel)

    # add the positivity distribution per hotel
    positivity_scores_hotel = positivity_scores[scores.index].groupby(df["hotel"][scores.index]).apply(list)
    positivity_scores_hotel = positivity_scores_hotel.rename(POSITIVITY_SCORES)
    final_scores = final_scores.join(positivity_scores_hotel)

    # remove low average scores
    final_scores = final_scores[final_scores[AVERAGE_SCORES] >= min_score]

    # ponderate the score with the user-specific score of the hotel
    #if user_based_score is not None:

    final_scores = final_scores.sort_values(by=[GLOBAL_SCORES, AVERAGE_SCORES, NUM_MATCHING_RATINGS], ascending=False)

    return final_scores

if __name__ == "__main__":
    import numpy as np
    df = pd.read_csv("processed_data.csv.zip")

    #load dates
    df["stay_date"] = pd.to_datetime(df["stay_date"])
    df["gap_stay_today"] = pd.to_timedelta(df["gap_stay_today"])

    print("loaded")
    final_scores = rank_from_scores(df)
    print(final_scores.head())
    final_scores = rank_from_scores(df, min_score=4)
    print(final_scores.head())
    final_scores = rank_from_scores(df, season={SPRING})
    print(final_scores.head())
    final_scores = rank_from_scores(df, season={SUMMER, SPRING})
    print(final_scores.head())
    final_scores = rank_from_scores(df, recency=False)
    print(final_scores.head())
    final_scores = rank_from_scores(df, positivity=False)
    print(final_scores.head())
    final_scores = rank_from_scores(df, positivity=False, recency=False)
    print(final_scores.head())