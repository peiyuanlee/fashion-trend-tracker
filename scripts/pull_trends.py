from pytrends.request import TrendReq
import os.path
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine

pytrends = TrendReq(hl='en-US', tz=360)

def save_keyword_popularity(keyword_list):
    today = datetime.today().strftime('%Y-%m-%d')
    
    all_data = []
    for keyword in keyword_list:
        try:
            pytrends.build_payload([keyword], timeframe='now 7-d', geo='US')
            df = pytrends.interest_over_time()
            if not df.empty:
                latest_popularity = int(df[keyword].iloc[-1])
                all_data.append((today, keyword, latest_popularity))
        except Exception as e:
            print(f"Error with {keyword}: {e}")

    # Save to database
    if all_data:
        engine = create_engine('sqlite:///./db/fashion_trends.db')
        df_to_save = pd.DataFrame(all_data, columns=['date', 'variable', 'popularity'])
        print(df_to_save.head())
        df_to_save.to_sql('trends', con=engine, if_exists='append', index=False)

file_path = 'data/trenads.csv'
if os.path.exists(file_path):
    print('hi')
    save_keyword_popularity(['boho', 'grunge', 'vintage', 'y2k', 'streetwear'])
else:
    keywords = ['boho', 'grunge', 'vintage', 'y2k', 'streetwear']
    pytrends.build_payload(keywords, cat=0, timeframe='today 5-y', geo='', gprop='')

    df = pytrends.interest_over_time()
    df = df.reset_index()
    df = df.drop(columns=['isPartial'])
    df = pd.melt(df, id_vars = ['date'], value_vars= ['boho', 'grunge', 'y2k', 'vintage', 'streetwear'], value_name= 'popularity')
    df.to_csv('data/trends.csv', index=False)
