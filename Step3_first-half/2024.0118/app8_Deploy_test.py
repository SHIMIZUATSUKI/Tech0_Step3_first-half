import streamlit as st
import pandas as pd
import sqlite3
import os

# 現在のファイルのディレクトリを取得（'2024.0118' ディレクトリが含まれると仮定）
current_dir = os.path.dirname(os.path.abspath(__file__))

# '2024.0118' が既に含まれているかどうかをチェック
if '2024.0118' in current_dir:
    db_path = os.path.join(current_dir, 'Tokyo_RealEstate_DB.db')
else:
    db_path = os.path.join(current_dir, '2024.0118', 'Tokyo_RealEstate_DB.db')

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
