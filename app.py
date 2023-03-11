import pickle
import numpy as np  
import streamlit as st
from dataclasses import dataclass



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


st.header('Find something to read')

model = pickle.load(open('artifacts/model.pkl','rb'))
book_names = pickle.load(open('artifacts/book_names.pkl','rb'))
final_rating = pickle.load(open('artifacts/final_rating.pkl','rb'))
book_pivot = pickle.load(open('artifacts/book_pivot.pkl','rb'))
genres =['Action', 'Crime', 'Drama', 'Comedy', 'Horror', 'Sci-Fi/Fantasy']
languages=['English','French','Spanish','Italian']

selected_books = st.selectbox(
    "Search \U0001F50D",
    book_names
)
# Initialization
if 'genre' not in st.session_state:
    st.session_state['genre'] = ''
if 'language' not in st.session_state:
    st.session_state['language'] = ''
if 'show_filters' not in st.session_state:
    st.session_state['show_filters'] = ""

if st.button("Filters"):
    update_state = 'True' if st.session_state['show_filters'] == 'False' or st.session_state['show_filters'] == '' else "False"
    st.session_state['show_filters'] = update_state
    
    
if st.session_state["show_filters"] == "True":
    genre=st.selectbox('Select Genre', genres)
    language=st.selectbox('Select Language', languages)
    st.session_state['genre'] = genre
    st.session_state['language'] = language


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



def recommend_book(book_name):
    books_list = []
    book_id = np.where(book_pivot.index == book_name)[0][0]
    distance, suggestion = model.kneighbors(book_pivot.iloc[book_id,:].values.reshape(1,-1), n_neighbors=6 )

    poster_url = fetch_poster(suggestion)
    
    for i in range(len(suggestion)):
            books = book_pivot.index[suggestion[i]]
            for j in books:
                books_list.append(j)
    return books_list , poster_url    
       



if st.button('Show Recommendation'):
    recommended_books,poster_url = recommend_book(selected_books)
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

        