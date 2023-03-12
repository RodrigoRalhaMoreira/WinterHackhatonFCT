import pickle
import numpy as np
import streamlit as st
from dataclasses import dataclass



years = ["1990", "1995", "2000", "2005", "2010", "2015", "2020"]
ncols = 4
nlines = 2
aspectR = 0.59
posterWidth = 150
posterHeight = posterWidth/aspectR

BIG_SEARCH = 50
DEFAULT_SEARCH = ncols * nlines +1


st.set_page_config(
    page_title="WhileTrue",
    page_icon=":books:",
    initial_sidebar_state="collapsed"
)


hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)



model = pickle.load(open("artifacts/model.pkl", "rb"))
book_names = pickle.load(open("artifacts/book_names.pkl", "rb"))
final_rating = pickle.load(open("artifacts/final_rating.pkl", "rb"))
book_pivot = pickle.load(open("artifacts/book_pivot.pkl", "rb"))
authors = pickle.load(open("artifacts/authors.pkl", "rb"))









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
        book_author = final_rating.iloc[idx]["author"]
        if not (st.session_state["from"] != "" and book_year and int(book_year) >= int(st.session_state["from"])):
            poster_url.append(None)
        elif not (st.session_state["to"] != "" and book_year and int(book_year) <= int(st.session_state["to"])):
            poster_url.append(None)
        elif (st.session_state["author"] != ""  and book_author and book_author != st.session_state["author"]): 
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
        if st.session_state["author"] != "" or st.session_state["from"] != "" or st.session_state["to"] != ""
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




# ----- site design ------- 





st.header("Find something to read")




col0, col1 = st.columns([80,20])

with col0:
    selected_books = st.selectbox("Search for a book", book_names)


with col1:
    st.markdown("<div style='height:34px'></div>", unsafe_allow_html=True)
    if st.button("Filters", use_container_width=True):
        update_state = (
            "True" if st.session_state["show_filters"] == "False" or st.session_state["show_filters"] == "" else "False"
        )


        st.session_state["show_filters"] = update_state


# Initialization
if "author" not in st.session_state:
    st.session_state["author"] = ""
if "from" not in st.session_state:
    st.session_state["from"] = ""
if "to" not in st.session_state:
    st.session_state["to"] = ""
if "show_filters" not in st.session_state:
    st.session_state["show_filters"] = ""


ss_show_filter = st.session_state["show_filters"]
if ss_show_filter == "True":
    author = st.selectbox("Select Author", authors)
    left_column, right_column = st.columns(2)
    from_date = left_column.selectbox("From:", years)
    to_date = right_column.selectbox("To:", years, index=6)
    print ("HHHHHHHHHH")
    print (author)
    print (authors[0])
    if (author != authors[0]):
        print ("!!!")
        st.session_state["author"] = author
    else:
        st.session_state["author"] = ""
    st.session_state["from"] = from_date
    st.session_state["to"] = to_date
elif ss_show_filter == "False":
    st.session_state["author"] = ""
    st.session_state["from"] = ""
    st.session_state["to"] = ""


if st.button('Show Recommendations'):
    st.write(st.session_state["author"])
    recommended_books,poster_url = recommend_book(selected_books)

    if len(recommended_books) <= 1:
        st.write("No available recommendations for this specific case!")
    else:
        cols = st.columns(ncols)
        for j in range(nlines):
            for i in range(ncols):
                k = j*ncols + i +1
                if(k<len(poster_url)):
                    with cols[i]:
                        url = "http://localhost:8501/books?id="+recommended_books[k]
                        image = poster_url[k]
                        name = recommended_books[k]
                    # st.markdown(f"<div style='text-align:center'> <a target=\'_self\' href='{url}'> <img src='{image}' alt='{name}' width=\"{posterWidth}\" height=\"{posterHeight}\" style='max-width:100%'></a><p line-height='0.1' style='text-align:center'>{name}</p></div>", unsafe_allow_html=True)
                        #st.markdown(f"<div style='text-align:center'> <a target=\'_self\' href='{url}'> <img src='{image}' alt='{name}' width=\"{posterWidth}\" height=\"{posterHeight}\" style='max-width:100%'></a><div style='margin-bottom: 5px; padding-bottom: 5px;'></div><p style=\"line-height: 1.2;\">{name}</p></div>", unsafe_allow_html=True)
                        st.markdown(f"<div style='text-align:center'> <a target=\'_self\' href='{url}'> <img src='{image}' alt='{name}' width=\"{posterWidth}\" height=\"{posterHeight}\" style='max-width:100%'></a><div style='margin-bottom: 5px; padding-bottom: 5px;'></div><p style=\"line-height: 1.3; max-height: 2.6em; overflow: hidden;\">{name}</p></div>", unsafe_allow_html=True)


