import pandas as pd
import re
import string

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from nltk.stem.snowball import SnowballStemmer

stemmer = SnowballStemmer("english")
cached_stop_words = ENGLISH_STOP_WORDS

def clean_text(df):
    # Lower casing the text
    df = df.apply(lambda x: x.lower())

    # Removing punctuation and numbers
    translation = str.maketrans("", "", string.punctuation + string.digits)
    df = df.apply(lambda x: x.translate(translation))

    # Removing stop words
    df = df.apply(lambda x: [item for item in x.split() if item not in cached_stop_words])

    # Stemming the words
    df = df.apply(lambda x: [stemmer.stem(item) for item in x])
    return df


# Load and preprocess oscar dataset
print('Reading input csv...')
data = pd.read_csv('oscar_movie_scripts.csv', names=['title', 'release_year', 'script'], header=None, encoding='ISO-8859-1')
# Cleaning the script text
print('Cleaning input features...')
data['oscar_nominee'] = True
data["script"] = clean_text(data["script"])
data.to_csv('cleaned_oscar_movie_scripts.csv')

# Load and preprocess non-oscar dataset
print('Reading input csv...')
data = pd.read_csv('non_oscar_movie_scripts.csv', names=['title', 'release_year', 'script'], header=None, encoding='ISO-8859-1')
# Cleaning the script text
print('Cleaning input features...')
data['oscar_nominee'] = False
data['script'] = data['script'].astype(str)
data["script"] = clean_text(data["script"])
data.to_csv('cleaned_non_oscar_movie_scripts.csv')