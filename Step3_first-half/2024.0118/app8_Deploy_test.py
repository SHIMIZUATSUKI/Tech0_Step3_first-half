import streamlit as st
import pandas as pd
import sqlite3
import os

# Streamlit Cloud上での実行時に、正しいデータベースファイルのパスを取得
db_path = os.path.join(os.getcwd(), 'Tokyo_RealEstate_DB.db')

# データベースファイルの存在を確認
if not os.path.exists(db_path):
    st.error(f"データベースファイルが見つかりません: {db_path}")
else:
    # データベースに接続
    conn = sqlite3.connect(db_path)

    query = 'SELECT * FROM "Ota_Ward"'  # テーブル名を正確に指定
    df = pd.read_sql_query(query, conn)

    st.write(df)

    conn.close()
