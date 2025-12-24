import streamlit as st
import pandas as pd
from book_prod import load_data, recommend_books

st.set_page_config(
    page_title="Book Recommendation Engine",
    layout="centered"
)

st.title("📚 Book Recommendation Engine")

@st.cache_data(show_spinner=True)
def get_dataset():
    return load_data(
        "data/BX-Book-Ratings.csv",
        "data/BX-Books.csv"
    )

dataset = get_dataset()

book_query = st.text_input(
    "Enter a full book title",
    placeholder="e.g. the fellowship of the ring (the lord of the rings, part 1)"
)

if st.button("Get Recommendations"):

    if not book_query.strip():
        st.warning("Please enter a book title.")
    else:
        with st.spinner("Computing recommendations..."):
            top10, worst10 = recommend_books(dataset, book_query)

        if top10 is None:
            st.error("Not enough data for this book.")
        else:
            st.subheader("✅ Top Recommended Books")

            st.dataframe(
                top10.reset_index()[[
                    "book", "ISBN", "avg_rating", "corr"
                ]].rename(columns={
                    "book": "Title",
                    "avg_rating": "Average Rating",
                    "corr": "Correlation"
                }),
                use_container_width=True,
                hide_index=True
            )

            st.subheader("❌ Least Similar Books")

            st.dataframe(
                worst10.reset_index()[[
                    "book", "ISBN", "avg_rating", "corr"
                ]].rename(columns={
                    "book": "Title",
                    "avg_rating": "Average Rating",
                    "corr": "Correlation"
                }),
                use_container_width=True,
                hide_index=True
            )
