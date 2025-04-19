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
    selected_keyword = st.selectbox("Choose a trend:", df.columns[1:-1])
    st.line_chart(df.set_index('date')[selected_keyword])
