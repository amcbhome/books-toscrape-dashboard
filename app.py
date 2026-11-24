import os
import pandas as pd
import streamlit as st
from scraper import scrape_all_books

st.set_page_config(
    page_title="Books to Scrape | 5-Star Dashboard",
    layout="wide",
)

# --- Custom CSS: Fit on one screen & enlarge metric cards ---
st.markdown(
    """
    <style>
        /* Reduce top/bottom page padding so everything fits on one screen */
        .block-container {
            padding-top: 1.5rem;
            padding-bottom: 1rem;
            max-width: 96%;
        }
        /* Style KPI cards as distinct, readable boxes */
        div[data-testid="stMetric"] {
            background-color: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(255, 255, 255, 0.12);
            border-radius: 10px;
            padding: 12px 16px;
        }
        /* Enlarge KPI labels */
        div[data-testid="stMetricLabel"] p {
            font-size: 1.05rem !important;
            font-weight: 600 !important;
        }
        /* Enlarge KPI numbers */
        div[data-testid="stMetricValue"] {
            font-size: 2.35rem !important;
            font-weight: 700 !important;
            line-height: 1.15 !important;
        }
        /* Tighten spacing around dividers */
        hr {
            margin-top: 0.75rem !important;
            margin-bottom: 0.75rem !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
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

# --- Compact Header ---
title_col, meta_col = st.columns([3, 1])
with title_col:
    st.markdown("## Books to Scrape: 5-Star Catalogue Overview")
with meta_col:
    st.markdown(
        "<div style='text-align:right; padding-top:12px; opacity:0.75;'>"
        "Source: books.toscrape.com (1,000 books)</div>",
        unsafe_allow_html=True,
    )

# --- KPI Cards: Row 1 (Counts & Averages) ---
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Number of Books", f"{total_books:,}")
c2.metric("5-Star Books", f"{total_five_star:,} ({(total_five_star / total_books) * 100:.1f}%)")
c3.metric("Avg Cost (5-Star Book)", f"£{avg_price_5:.2f}")
c4.metric("Avg Cost (All 1,000 Books)", f"£{avg_price_all:.2f}")

# --- KPI Cards: Row 2 (Min & Max Ranges) ---
c5, c6, c7, c8 = st.columns(4)
c5.metric("Min Cost (5-Star Book)", f"£{min_price_5:.2f}")
c6.metric("Max Cost (5-Star Book)", f"£{max_price_5:.2f}")
c7.metric("Min Cost (All Books)", f"£{min_price_all:.2f}")
c8.metric("Max Cost (All Books)", f"£{max_price_all:.2f}")

st.divider()

# --- Pictorial Showcase: 4 Selected 5-Star Books ---
header_col, btn_col = st.columns([5, 1])
with header_col:
    st.markdown("### Featured 5-Star Books")
with btn_col:
    if st.button("Shuffle 4 Books", use_container_width=True):
        st.session_state["sample_seed"] = st.session_state.get("sample_seed", 42) + 1

seed = st.session_state.get("sample_seed", 42)
featured_books = five_star_df.sample(n=min(4, len(five_star_df)), random_state=seed)

pic_cols = st.columns(4)
for col, (_, book) in zip(pic_cols, featured_books.iterrows()):
    with col:
        with st.container(border=True):
            img_col, info_col = st.columns([1.15, 1.35])
            with img_col:
                # Native width (155px) keeps the cover crisp and prevents stretching
                st.image(book["image_url"], width=155)
            with info_col:
                st.markdown(f"**{book['title']}**")
                st.markdown(f"### £{book['price']:.2f}")
                st.caption("★★★★★ (5/5)")
                st.link_button("View Book", book["book_url"], use_container_width=True)
