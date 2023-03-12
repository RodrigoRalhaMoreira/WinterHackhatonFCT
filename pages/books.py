   
import pickle
from tkinter import Image
import streamlit as st
import numpy as np


params = st.experimental_get_query_params()
name = params["id"][0]



model = pickle.load(open('artifacts/model.pkl','rb'))
book_names = pickle.load(open('artifacts/book_names.pkl','rb'))
final_rating = pickle.load(open('artifacts/final_rating.pkl','rb'))
book_pivot = pickle.load(open('artifacts/book_pivot.pkl','rb'))


#todo
def getPosterFromName(book_name):
    book_id = np.where(book_pivot.index == book_name)[0][0]
    distance, suggestion = model.kneighbors(book_pivot.iloc[book_id,:].values.reshape(1,-1), n_neighbors=1)

    poster_urls = fetch_poster(suggestion)
    poster_url = poster_urls[0]
    return poster_url   

#todo
def fetch_poster(suggestion):
    book_name = []
    ids_index = []
    poster_url = []

    for book_id in suggestion:
        book_name.append(book_pivot.index[book_id])

    for name in book_name[0]: 
        ids = np.where(final_rating['title'] == name)[0][0]
        ids_index.append(ids)

    for idx in ids_index:
        url = final_rating.iloc[idx]['image_url']
        poster_url.append(url)

    return poster_url



col0, col1 = st.columns([1,3])

posterURL = getPosterFromName(name)

with col0:
    st.image(posterURL)

with col1:
    st.title(name)



    


