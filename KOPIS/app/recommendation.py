from joblib import load
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import requests
import xml.etree.ElementTree as ET

service_key = "9e01c797c9504aa68b51104412042f2a"

preprocessor = load('./preprocessor.joblib')
transformed_data = load('./transformed_data.joblib')

def make_df(gender, year, genre, region, price):
    if gender == "남성":
        gender = 0
    else:
        gender = 1

    minimum, maximum = price[:-1].split('~')
    minimum = int(minimum.replace(',', ''))
    maximum = int(maximum.replace(',', ''))

    price_avg = (minimum+maximum)//2
    
    user_input = {
    '성별': [gender],
    '연령': [year],
    '장르명': [genre],
    '공연지역명': [region],
    '장당금액': [price_avg]
    }

    user_df = pd.DataFrame(user_input)

    return user_df


def recommend(selected_gender, selected_year, selected_genre, selected_region, selected_price, top_n=100):
    user_df = make_df(selected_gender, selected_year, selected_genre, selected_region, selected_price)
    transformed_user = preprocessor.transform(user_df)
    similarities = cosine_similarity(transformed_user, transformed_data)
    top_indices = similarities[0].argsort()[-top_n:][::-1]
    recommendations = [performance_codes[i] for i in top_indices]
    recommendations = list(set(recommendations))[:5]

    return recommendations
    # performance_names = []
    # for i in recommendations:
    #     url = "http://www.kopis.or.kr/openApi/restful/pblprfr/{}?service={}".format(i, service_key)
    #     response = requests.get(url)

    #     if response.status_code == 200:
    #         root = ET.fromstring(response.content)
    #         for child in root:
    #             for c in child:
    #                 if c.tag == "prfnm":
    #                     performance_name = c.text
    #                     performance_names.append(performance_name)
    #                     break

    # return performance_names


