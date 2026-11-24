import os
import pandas as pd
import streamlit as st
from scraper import scrape_all_books

st.set_page_config(
    page_title="Books to Scrape | 5-Star Dashboard",
    layout="wide",
)


@st.cache_data
def load_data() -> pd.DataFrame:
    if os.path.exists("books_data.csv"):
        return pd.read_csv("books_data.csv")
    return scrape_all_books()


df = load_data()
five_star_df = df[df["rating"] == 5].reset_index(drop=True)

# --- Calculations ---
total_books = len(df)
total_five_star = len(five_star_df)

avg_price_all = df["price"].mean()
min_price_all = df["price"].min()
max_price_all = df["price"].max()

avg_price_5 = five_star_df["price"].mean()
min_price_5 = five_star_df["price"].min()
max_price_5 = five_star_df["price"].max()

# --- Header ---
st.title("Books to Scrape: 5-Star Catalogue Overview")
st.caption("Source: books.toscrape.com (1,000-book catalogue)")

# --- KPI Cards: Row 1 (Counts & Averages) ---
st.subheader("Catalogue & 5-Star Metrics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="Total Number of Books", value=f"{total_books:,}")
with col2:
    st.metric(
        label="5-Star Books",
        value=f"{total_five_star:,}",
        delta=f"{(total_five_star / total_books) * 100:.1f}% of catalogue",
    )
with col3:
    st.metric(label="Avg Cost (5-Star Book)", value=f"£{avg_price_5:.2f}")
with col4:
    st.metric(label="Avg Cost (All 1,000 Books)", value=f"£{avg_price_all:.2f}")

# --- KPI Cards: Row 2 (Min & Max Ranges) ---
col5, col6, col7, col8 = st.columns(4)

with col5:
    st.metric(label="Min Cost (5-Star Book)", value=f"£{min_price_5:.2f}")
with col6:
    st.metric(label="Max Cost (5-Star Book)", value=f"£{max_price_5:.2f}")
with col7:
    st.metric(label="Min Cost (All Books)", value=f"£{min_price_all:.2f}")
with col8:
    st.metric(label="Max Cost (All Books)", value=f"£{max_price_all:.2f}")

st.divider()

# --- Pictorial Showcase: 4 Selected 5-Star Books ---
header_col, btn_col = st.columns([4, 1])
with header_col:
    st.subheader("Featured 5-Star Books")
with btn_col:
    if st.button("Shuffle 4 Books", use_container_width=True):
        st.session_state["sample_seed"] = st.session_state.get("sample_seed", 42) + 1

seed = st.session_state.get("sample_seed", 42)
featured_books = five_star_df.sample(n=min(4, len(five_star_df)), random_state=seed)

pic_cols = st.columns(4)
for col, (_, book) in zip(pic_cols, featured_books.iterrows()):
    with col:
        with st.container(border=True):
            st.image(book["image_url"], use_container_width=True)
            st.markdown(f"**{book['title']}**")
            st.write(f"Price: **£{book['price']:.2f}** | Rating: ★★★★★")
            st.link_button("View on Site", book["book_url"], use_container_width=True)

# --- Full 5-Star Data Table ---
with st.expander(f"View all {total_five_star} 5-Star Books"):
    st.dataframe(
        five_star_df[["title", "price", "book_url"]].sort_values(by="price"),
        use_container_width=True,
        hide_index=True,
        column_config={
            "title": "Book Title",
            "price": st.column_config.NumberColumn("Price (£)", format="£%.2f"),
            "book_url": st.column_config.LinkColumn("Catalogue Link"),
        },
    )
