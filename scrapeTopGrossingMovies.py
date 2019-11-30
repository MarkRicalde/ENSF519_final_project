import os
import pandas as pd
import requests
from bs4 import BeautifulSoup

filename   = 'top_grossing_movies.csv'

def get_highest_grossing_movies(year, top_n):
    print('Gathering highest grossing movies for: {}'.format(year))
    url = r'https://www.the-numbers.com/market/{}/top-grossing-movies'.format(year)
    data = requests.get(url).text
    parser = BeautifulSoup(data, 'html.parser')
    tags = parser.find_all('tr')
    if tags == None:
        return None
    top_movies = []
    count = 0
    for movie_tag in tags:
        if count >= top_n:
            # If there are more movies than top_n, skip them
            break
        cols = movie_tag.find_all('td')
        results_list = [c.text for c in cols]
        if len(results_list) == 0 or not(results_list[0].isdigit()):
            continue
        year = parser.find('h1').text.replace('Annual Movie Chart - ', '')
        results_list.append(year)
        top_movies.append(results_list)
        count += 1
    return top_movies

def clean_numerical_col(text):
    return ''.join(ch for ch in text if ch not in ['$', ','])


movie_dict = {}
# Parse through previous csv - don't re scrape existing data
if os.path.exists(filename):
    prior_data = pd.read_csv(filename)
    for year in prior_data.release_year:
        movie_dict[year] = None

all_results = []
for year in range(1930, 2018):
    if year in movie_dict:
        continue
    try:
        highest_grossing_results = get_highest_grossing_movies(year, 100)
    except Exception as e:
        print(' Error getting html data...')
        print(e)
        continue
    if highest_grossing_results == None:
        continue
    for result in highest_grossing_results:
        all_results.append(result)
    movie_dict[year] = None

df = pd.DataFrame.from_records(all_results, columns=['Rank', 'Title', 'Release Date', 'Distributor', 'Genre', 'Gross', 'Tickets Sold', 'highest_grossing_year'])
df['Gross'] = df['Gross'].apply(clean_numerical_col)
df['Tickets Sold'] = df['Tickets Sold'].apply(clean_numerical_col)
df.to_csv(filename)