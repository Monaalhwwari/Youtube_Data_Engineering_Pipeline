import logging
import requests
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

api = os.getenv("api_key")
password =os.getenv("db_password")
print("API KEY:", api)
print("DB PASSWORD:", password)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


engine = create_engine(f"postgresql://postgres:{password}@localhost:5432/Youtube_API")

@st.cache_data
def extract():

    url = "https://www.googleapis.com/youtube/v3/search"

    params = {
        "key": api,
        "part": "snippet",
        "maxResults": 10,
        "q": "Data Engineering Course",
        "publishedAfter": "2026-01-01T00:00:00Z",
        "order": "viewCount",
        "type": "video",
        "videoDuration": "long"
    }

    response = requests.get(url, params=params)
    data = response.json()
    print(data)

    data = pd.json_normalize(data["items"])
    df= pd.DataFrame(data)

    first_df = df.dropna(subset=["id.videoId"])

    first_df = first_df.rename(columns={"id.videoId": "id"})

    video_ids  = first_df["id"].astype(str).tolist()


    v_params = {
        "key": api,
        "part": "statistics",
        "id": ",".join(video_ids)
    }

    v_url = "https://www.googleapis.com/youtube/v3/videos"

    v_response = requests.get(v_url, params=v_params)
    Second_df = v_response.json()
    Second_df = pd.json_normalize(Second_df["items"])

    Second_df["videoId"] = Second_df["id"].astype(str)

    return first_df, Second_df

@st.cache_data
def transform(First_df,Second_df):

    merged_dataFrame = First_df.merge(Second_df, on="id", how="inner")

    merged_dataFrame=merged_dataFrame[[
        "snippet.title",
        "snippet.channelTitle",
        "statistics.viewCount",
        "statistics.likeCount",
        "statistics.commentCount",
        "snippet.publishedAt",

    ]]

    merged_dataFrame=merged_dataFrame.rename(columns={
        "snippet.title": "title",
        "snippet.channelTitle": "channelTitle",
        "statistics.viewCount": "viewCount",
        "statistics.likeCount": "likeCount",
        "statistics.commentCount": "commentCount",
        "snippet.publishedAt": "Date",
    })

    merged_dataFrame["title"]=merged_dataFrame["title"].astype(str)

    merged_dataFrame["channelTitle"]=merged_dataFrame["channelTitle"].astype(str)

    merged_dataFrame["viewCount"]=merged_dataFrame["viewCount"].astype(int)

    merged_dataFrame["likeCount"]=merged_dataFrame["likeCount"].astype(int)

    merged_dataFrame["commentCount"]=merged_dataFrame["commentCount"].astype(int)

    merged_dataFrame["Date"]=pd.to_datetime(merged_dataFrame["Date"])

    merged_dataFrame=merged_dataFrame.dropna(subset=["channelTitle","title","viewCount","likeCount","commentCount","Date"])

    logging.info(merged_dataFrame.shape[0])

    return merged_dataFrame

def load(df):
    df.to_sql(
        name="youtube_videos",
        con=engine,
        if_exists="replace",
        index=False
    )
    logging.info("Database loaded")

    df = pd.read_sql("SELECT * FROM youtube_videos", engine)

    logging.info(df.shape[0])

if __name__ == "__main__":
    first_df, Second_df = extract()
    mer_df=transform(first_df, Second_df)
    load(mer_df)
