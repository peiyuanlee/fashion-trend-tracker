from prophet import Prophet
import pandas as pd 

def forecast_prophet(df, keyword, n_days=30):
    trend_df = df[df['variable'] == keyword].copy()
    trend_df['date'] = pd.to_datetime(trend_df['date'])

    prophet_df = trend_df.rename(columns={'date': 'ds', 'popularity': 'y'})[['ds', 'y']]
    
    model = Prophet()
    model.fit(prophet_df)

    future = model.make_future_dataframe(periods=n_days)
    forecast = model.predict(future)

    return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
