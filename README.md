# YouTube Data Engineering Pipeline & Dashboard

## Summary
This project is an end-to-end data engineering pipeline that extracts Youtube video data using the Youtube Data API, and transforms it using Python and pandas, loads it into a PostgreSQL database, and visualizes it using a Streamlit dashboard.

## Tech Stack
- Python
- Pandas
- Requests
- PostgreSQL
- SQLAlchemy
- Streamlit
- YouTube Data API

### Extract
- Fetch video data from the YouTube Data API
- Search for videos related to "Data Engineering Course"

### Transform
- Clean and process JSON data using Pandas
- Convert data types (views, likes, comments, dates)
- Handle missing values

### Load
- Store cleaned data into PostgreSQL
- Table name: youtube_videos

### Visualization
- Display KPIs (total views, likes, number of videos)
- Show top videos
- Show top channels
- Show trends over time
- Filter data by channel
