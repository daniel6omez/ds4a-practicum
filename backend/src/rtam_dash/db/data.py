
import json
import numpy as np
import pandas as pd
import io
from sqlalchemy import create_engine
 
DB_USERNAME = 'postgres@psql-ds4a-prod'
DB_PASSWORD = 'FliFUDlbO72cq2h9AaFF'
HOST = 'psql-ds4a-prod.postgres.database.azure.com'

#engine = create_engine('sqlite:///crime.db')
engine=create_engine(f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{HOST}/ds4a',connect_args={'sslmode':'require'},  max_overflow=20)
query ='select * from processed.accidents'
# df = pd.read_sql("select * from processed.accidents", engine.connect(), parse_dates=('Date'))

def read_sql_inmem_uncompressed(query, db_engine):

    copy_sql = "COPY ({query}) TO STDOUT WITH CSV {head}".format(
       query=query, head="HEADER"
    )
    conn = db_engine.raw_connection()
    cur = conn.cursor()
    store = io.StringIO()
    cur.copy_expert(copy_sql, store)
    store.seek(0)
    df = pd.read_csv(store,parse_dates=['Date'])
    return df

df = read_sql_inmem_uncompressed(query, engine)
dff = df.copy()