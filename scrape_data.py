import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://api.teleport.org/api"

def get_data(path_url, base_url=BASE_URL):
    response = requests.get(f"{base_url}/{path_url}").json()
    urls = []
    cities = []
    for res in response['_links']['ua:item']:
        urls.append(res['href'])
        cities.append(res['name'])
    
    city_categories = []
    city_scores = []
    city_summaries = []
    
    for url in urls:
        response = requests.get(f"{url}scores/").json()
        city_categories.append(response['categories'])
        city_scores.append(round(response['teleport_city_score'], 2))
        soup = BeautifulSoup(response['summary'], 'html.parser')
        city_summaries.append(soup.text)
        
    return (cities, city_categories, city_scores, city_summaries)


def transform_data(cities, city_categories, city_scores, city_summaries):
    housing_scores = []
    venture_capital_scores = []
    education_scores = []
    economy_scores = []
    environmental_quality_scores = []
    startups_scores = []
    cost_of_living_scores = []
    healthcare_scores = []
    commute_scores = []
    travel_connectivity_scores = []
    business_freedom_scores = []
    taxation_scores = []
    internet_access_scores = []
    leisure_and_culture_scores = []
    tolerance_scores = []
    outdoors_scores = []
    safety_scores = []
    
    for category in city_categories:
        for c in category:
            if c['name'] == 'Housing':
                housing_scores.append(round(c['score_out_of_10'], 2))
            if c['name'] == 'Venture Capital':
                venture_capital_scores.append(round(c['score_out_of_10'], 2))
            if c['name'] == 'Economy':
                economy_scores.append(round(c['score_out_of_10'], 2))
            if c['name'] == 'Education':
                education_scores.append(round(c['score_out_of_10'], 2))
            if c['name'] == 'Safety':
                safety_scores.append(round(c['score_out_of_10'], 2))
            if c['name'] == 'Leisure and Culture':
                leisure_and_culture_scores.append(round(c['score_out_of_10'], 2))
            if c['name'] == 'Taxation':
                taxation_scores.append(round(c['score_out_of_10'], 2))
            if c['name'] == 'Environmental Quality':
                environmental_quality_scores.append(round(c['score_out_of_10'], 2))
            if c['name'] == 'Internet Access':
                internet_access_scores.append(round(c['score_out_of_10'], 2))
            if c['name'] == 'Outdoors':
                outdoors_scores.append(round(c['score_out_of_10'], 2))
            if c['name'] == 'Tolerance':
                tolerance_scores.append(round(c['score_out_of_10'], 2))
            if c['name'] == 'Commute':
                commute_scores.append(round(c['score_out_of_10'], 2))
            if c['name'] == 'Business Freedom':
                business_freedom_scores.append(round(c['score_out_of_10'], 2))
            if c['name'] == 'Startups':
                startups_scores.append(round(c['score_out_of_10'], 2))
            if c['name'] == 'Travel Connectivity':
                travel_connectivity_scores.append(round(c['score_out_of_10'], 2))
            if c['name'] == 'Healthcare':
                healthcare_scores.append(round(c['score_out_of_10'], 2))
            if c['name'] == 'Cost of Living':
                cost_of_living_scores.append(round(c['score_out_of_10'], 2))
    
    data = {"City": cities, "Housing_Score": housing_scores, "Economy_Score": economy_scores, 
            "Education_Score": education_scores, "Cost_of_Living_Score": cost_of_living_scores, 
            "Taxation_Score": taxation_scores, "Healthcare_Score": healthcare_scores, 
            "Environmental_Quality_Score": environmental_quality_scores, 
            "Business_Freedom_Score": business_freedom_scores, "Internet_Access_Score": internet_access_scores, 
            "Outdoors_Score": outdoors_scores, "Startups_Score": startups_scores,
           "Commute_Score": commute_scores, "Tolerance_Score": tolerance_scores, 
            "Travel_Connectivity_Score": travel_connectivity_scores,
           "Venture_Capital_Score": venture_capital_scores, "Safety_Score": safety_scores, 
            "City_Score": city_scores, "Summary": city_summaries}     
    df = pd.DataFrame(data)
    df["Summary"] = df['Summary'].replace({r'\s+$': '', r'^\s+': ''}, regex=True).replace({r'\n\s+': ' '}, regex=True)
    return df.drop('Summary', axis=1)


cities, city_categories, city_scores, city_summaries = get_data("urban_areas")
data = transform_data(cities, city_categories, city_scores, city_summaries)

data.to_csv(".quality_of_life_v1.csv", index=False)


        