import pickle
import numpy as np
import streamlit as st
from dataclasses import dataclass

BIG_SEARCH = 50
DEFAULT_SEARCH = 6

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Create a sidebar with some options
with st.sidebar:
    st.title("Sidebar Title")

st.header("Find something to read")

model = pickle.load(open("artifacts/model.pkl", "rb"))
book_names = pickle.load(open("artifacts/book_names.pkl", "rb"))
final_rating = pickle.load(open("artifacts/final_rating.pkl", "rb"))
book_pivot = pickle.load(open("artifacts/book_pivot.pkl", "rb"))
genres = ["Action", "Crime", "Drama", "Comedy", "Horror", "Sci-Fi/Fantasy"]
years = ["1990", "1995", "2000", "2005", "2010", "2015", "2020"]

selected_books = st.selectbox("Search \U0001F50D", book_names)
# Initialization
if "genre" not in st.session_state:
    st.session_state["genre"] = ""
if "from" not in st.session_state:
    st.session_state["from"] = ""
if "to" not in st.session_state:
    st.session_state["to"] = ""
if "show_filters" not in st.session_state:
    st.session_state["show_filters"] = ""

if st.button("Filters"):
    update_state = (
        "True" if st.session_state["show_filters"] == "False" or st.session_state["show_filters"] == "" else "False"
    )
    st.session_state["show_filters"] = update_state

if st.session_state["show_filters"] == "True":
    genre = st.selectbox("Select Genre", genres)
    left_column, right_column = st.columns(2)
    from_date = left_column.selectbox("From:", years)
    to_date = right_column.selectbox("To", years, index=6)
    st.session_state["genre"] = genre
    st.session_state["from"] = from_date
    st.session_state["to"] = to_date


def filter_sugestions(suggestion):
    book_name = []
    ids_index = []
    poster_url = []
    books_filtered = []

    for book_id in suggestion:
        book_name.append(book_pivot.index[book_id])

    for name in book_name[0]:
        ids = np.where(final_rating["title"] == name)[0][0]
        ids_index.append(ids)

    for idx in ids_index:
        book_year = final_rating.iloc[idx]["year"]
        if not (st.session_state["from"] != "" and book_year and int(book_year) >= int(st.session_state["from"])):
            poster_url.append(None)
        elif not (st.session_state["to"] != "" and book_year and int(book_year) <= int(st.session_state["to"])):
            poster_url.append(None)
        else:
            url = final_rating.iloc[idx]["image_url"]
            poster_url.append(url)

    for book_id, idx in zip(suggestion[0], poster_url):
        if idx:
            books_filtered.append(book_id)
    books_filtered = np.array([books_filtered])
    return books_filtered


def fetch_poster(suggestion):
    book_name = []
    ids_index = []
    poster_url = []

    for book_id in suggestion:
        book_name.append(book_pivot.index[book_id])

    for name in book_name[0]:
        ids = np.where(final_rating["title"] == name)[0][0]
        ids_index.append(ids)

    for idx in ids_index:
        url = final_rating.iloc[idx]["image_url"]
        poster_url.append(url)

    return poster_url


def recommend_book(book_name: str):
    books_list = []
    book_id = np.where(book_pivot.index == book_name)[0][0]
    n_neighbors = (
        BIG_SEARCH
        if st.session_state["genre"] != "" or st.session_state["from"] != "" or st.session_state["to"] != ""
        else DEFAULT_SEARCH
    )
    distance, suggestion = model.kneighbors(book_pivot.iloc[book_id, :].values.reshape(1, -1), n_neighbors=n_neighbors)

    if n_neighbors == BIG_SEARCH:
        suggestion = filter_sugestions(suggestion)
    if not len(suggestion[0]):
        return [], []
    for i in range(len(suggestion)):
        books = book_pivot.index[suggestion[i]]
        for j in books:
            books_list.append(j)
    poster_url = fetch_poster(suggestion)
    return books_list, poster_url


if st.button("Show Recommendation"):
    recommended_books, poster_url = recommend_book(selected_books)
    if len(recommended_books) == 0:
        st.write("No available recommendations for this specific case!")
    else:
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.text(recommended_books[1])
            st.image(poster_url[1])
        with col2:
            st.text(recommended_books[2])
            st.image(poster_url[2])
        with col3:
            st.text(recommended_books[3])
            st.image(poster_url[3])
        with col4:
            st.text(recommended_books[4])
            st.image(poster_url[4])
        with col5:
            st.text(recommended_books[5])
            st.image(poster_url[5])
