import typing as t
import pandas as pd
from math import exp

SPRING, SUMMER, AUTUMN, WINTER = "printemps", "été", "automne", "hiver"

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
            ({1, 2, 3} if season == SPRING else set()).union(
                {4, 5, 6} if season == SUMMER else set()
            ).union(
                {7, 8, 9} if season == AUTUMN else set()
            ).union(
                {10, 11, 12} if season == WINTER else set()
            ))
        
        print(f"filter by season: old {len(df)}, new {is_season.sum()}")
        df = df[is_season]

    # compute the base score value of the review
    scores = df["rating"] * df['user_expertise']

    # ponderate the scores by the recency of the review (exp(-x), x being the number of days since the review was posted)
    if recency:
        recency_multiplier = df["gap_stay_today"].dt.days.apply(lambda days: exp(-days))

    # ponderate with the positivity scores
    if positivity:
        positivity_scores = (df["text_polarity"] * (1 - df["text_objectivity"]))
        positivity_scores += (df["title_polarity"] * (1 - df["title_objectivity"]))
        positivity_scores /= 2

    # weighted average
    def weighted_avg(group):
        indexes = group.index

        weighted_values = group

        if recency:
            recency_multiplier_group = recency_multiplier[indexes]
            weighted_values *= recency_multiplier_group

        if positivity:
            positivity_scores_group = positivity_scores[indexes]
            weighted_values *= positivity_scores_group

        weights = (
            (recency_multiplier_group * positivity_scores_group).sum() if recency and positivity else
            recency_multiplier_group.sum() if recency else
            positivity_scores_group.sum() if positivity else
            len(weighted_values) # no weights, standard average
        )

        return weighted_values.sum() / weights
    
    # compute the score of each hotel
    final_scores = scores.groupby(df["hotel"][scores.index]).apply(weighted_avg)

    # remove low scores
    final_scores = final_scores[final_scores >= min_score]

    # ponderate the score with the user-specific score of the hotel
    #if user_based_score is not None:

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
    final_scores = rank_from_scores(df, season=SPRING)
    print(final_scores.head())
    final_scores = rank_from_scores(df, recency=False)
    print(final_scores.head())
    final_scores = rank_from_scores(df, positivity=False)
    print(final_scores.head())
    final_scores = rank_from_scores(df, positivity=False, recency=False)
    print(final_scores.head())