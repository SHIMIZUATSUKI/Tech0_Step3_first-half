import streamlit as st
import pandas as pd
import sqlite3

# .dbファイルへのパスを設定
db_path = 'Tokyo_RealEstate_DB.db'
conn = sqlite3.connect(db_path)

query = "SELECT * FROM \"Ota_Ward\""  # テーブル名を正確に指定
df = pd.read_sql_query(query, conn)

st.write(df)

conn.close()
