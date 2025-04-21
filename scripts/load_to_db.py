import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('sqlite:///./db/fashion_trends.db')
df = pd.read_csv('data/trends.csv')
df.to_sql('trends', engine, index=False, if_exists='replace')
