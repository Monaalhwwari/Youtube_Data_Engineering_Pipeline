import pandas as pd
from sqlalchemy import create_engine, URL
import streamlit as st
from dotenv import load_dotenv
import os

load_dotenv()

password = os.getenv("db_password")

connection_url = URL.create(
    "postgresql+psycopg2",
    username="postgres",
    password=password,
    host="127.0.0.1",
    port=5432,
    database="Youtube_API"
)

engine = create_engine(connection_url)

df = pd.read_sql("SELECT * FROM youtube_videos", engine)

# visualaization

st.title("YouTube Dashboard")

views,likes,videos=st.columns(3)

views.metric("Total Views", df["viewCount"].sum())
likes.metric("Total Likes", df["likeCount"].sum())
videos.metric("Total Videos", len(df))

## top videos
st.subheader("Top 3 Videos")
st.dataframe(df.sort_values("viewCount",ascending=False)[["title","viewCount","likeCount"]].head(3))

# top channels
st.subheader("Top Channels by Views")
top_channels = (df.groupby("channelTitle")["viewCount"]
.sum()
.sort_values(ascending=False))

st.bar_chart(top_channels)

# Likes and Views Over Time
st.subheader("Likes and Views Overtime")
time_df = df.groupby("Date")[["viewCount", "likeCount"]].sum()

st.line_chart(time_df)

# choose channel
st.subheader("Choose a channel to view their stats")
channel = st.selectbox("Select Channel", df["channelTitle"].unique())
filtered_df = df[df["channelTitle"]==channel]
st.metric("Total Views",filtered_df["viewCount"].sum())

st.dataframe(filtered_df[["title", "viewCount"]])
