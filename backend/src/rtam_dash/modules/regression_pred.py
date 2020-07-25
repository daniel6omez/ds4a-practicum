from datetime import datetime as dt
import holidays

import dash_html_components as html
import os


#Dash Bootstrap Components
import dash_bootstrap_components as dbc 

import statsmodels.api as sm
import pandas as pd

#######
#######


def regression_predict(month, day, isHoliday):
    """
        this function return the model prediction 
        model recibe a dataframe with the follow columns
        MonthNum: the number of month (1: january, ..., 12: december), 
        WeekDayNum: numbr of day (0: Sunday, ... 6: Saturday),
        IsHoliday: a binary column (1: is holiday, 0: is not holiday) 
    """
    

    model = sm.load(os.getcwd()+'/model/LR_model.pkl')
    
    tmp = pd.DataFrame([[month, day, isHoliday]], columns=["MonthNum", "WeekDayNum", "IsHoliday"])
    result = round(model.predict(tmp)[0])
    return result

def call_regression_model(date):  
    dt_date = dt.strptime(date, "%Y-%m-%d")  
    day =  dt_date.weekday()
    day = day+1 if day < 6 else 0
    month =  dt_date.month
    isHoliday = int(dt_date in holidays.CO())
    
    return regression_predict(month, day, isHoliday)


def suffix(d):
    return 'th' if 11<=d<=13 else {1:'st',2:'nd',3:'rd'}.get(d%10, 'th')

def custom_strftime(format, t):
    return t.strftime(format).replace('{S}', str(t.day) + suffix(t.day))

def custom_message(date):
    accidents = str(call_regression_model(date)) 
    dt_date = dt.strptime(date, "%Y-%m-%d")
    txt = accidents + " traffic incidents are estimated for " + custom_strftime('%a {S} of %B, %Y', dt_date)
    #https://docs.python.org/2/library/datetime.html#strftime-strptime-behavior
    #pd.to_datetime(date, format="%Y-%m-%d").strftime(' %d %B ')
  
    return txt




