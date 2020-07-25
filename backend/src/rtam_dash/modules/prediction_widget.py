import dash
import dash_core_components as dcc
from datetime import datetime as dt


date_picker_model=dcc.DatePickerSingle(
                id='date_picker_model',
                min_date_allowed=dt(2019, 1, 1),
                max_date_allowed=dt(2020, 12, 31),
                initial_visible_month=dt.today().date(),
                clearable=True,
                with_portal=True,
                date=str(dt.today().date())
                #start_date=dt(2016,1,1).date(),
                #end_date=dt(2017, 1, 1).date()
            )
