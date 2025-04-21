import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
import os

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  
DB_PATH = os.path.join(BASE_DIR, 'db', 'fashion_trends.db')

engine = create_engine(f'sqlite:///{DB_PATH}')


st.title("Fashion Trend Tracker")
with engine.connect() as connection:
    df = pd.read_sql(text('SELECT * FROM trends'), connection)


selected_trend = st.selectbox("Choose a trend:", df['variable'].unique())
df['date'] = pd.to_datetime(df['date'])
trend_data = df[df['variable'] == selected_trend]
trend_data = trend_data.set_index('date').drop(['variable'], axis = 1)
st.line_chart(trend_data)

max_value = trend_data['popularity'].max()
max_date = trend_data['popularity'].idxmax().strftime('%Y-%m-%d')
min_value = trend_data['popularity'].min()
min_date = trend_data['popularity'].idxmin().strftime('%Y-%m-%d')
avg_value = trend_data['popularity'].mean()

if len(trend_data) > 30:
    growth = (trend_data['popularity'].iloc[-1] - trend_data['popularity'].iloc[-31]) / trend_data['popularity'].iloc[-31] * 100

else:
    growth = None

st.subheader("Trend Insights:")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Max Popularity", f"{max_value:.2f}", f"on {max_date}")
col2.metric("Min Popularity", f"{min_value:.2f}", f"on {min_date}")
col3.metric("Avg Popularity", f"{avg_value:.2f}")
if growth is not None:
    delta_color = "normal" if growth == 0 else ("inverse" if growth < 0 else "off")
    col4.metric("30-Day Growth", f"{growth:.2f}%", delta=None, delta_color=delta_color)
else:
    col4.write("Not enough data for 30-day growth.")

