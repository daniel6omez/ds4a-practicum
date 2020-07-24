import statsmodels.api as sm
import pandas as pd
from datetime import datetime as dt
import holidays
import json

def prepare_date():
    dt_date = dt.today().date()
    day =  dt_date.weekday()
    day = day+1 if day < 6 else 0
    month =  dt_date.month
    isHoliday = int(dt_date in holidays.CO())

    return dt_date.strftime("%Y-%m-%d"), pd.DataFrame([[month, day, isHoliday]], columns=["MonthNum", "WeekDayNum", "IsHoliday"])

def today_pred():    
    model = sm.load("../model/LR_model.pkl")
    date, df = prepare_date()
    pred = round(model.predict(df)[0])

    result = {'date': date, 'prediction':pred}    

    with open('../assets/daily_predict.json', 'w') as fp:
        json.dump(result, fp)


if __name__ == "__main__":
    today_pred()
    
