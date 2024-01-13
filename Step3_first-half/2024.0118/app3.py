import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

@st.cache_data  # st.cacheからst.cache_dataに変更
def load_data():
    # SQLAlchemyのエンジンを作成し、データベースに接続
    engine = create_engine('sqlite:///Tokyo_RealEstate_DB.db')
    
    # SQLクエリを実行し、結果をDataFrameに読み込む
    query = 'SELECT * FROM "Ota_Ward"'
    df = pd.read_sql(query, engine)
    
    # 英語のカラム名を日本語に変更する変換
    column_translations_reversed = {
        "Property Name": "物件名",
        "Address": "住所",
        "Access": "アクセス",
        "Nearest Station 1": "最寄駅1",
        "Time to Nearest Station 1 (min)": "最寄駅1からの時間(分)",
        "Nearest Station 2": "最寄駅2",
        "Time to Nearest Station 2 (min)": "最寄駅2からの時間(分)",
        "Nearest Station 3": "最寄駅3",
        "Time to Nearest Station 3 (min)": "最寄駅3からの時間(分)",
        "Building Age (years)": "築年数(年)",
        "Building Floors": "建物の階数",
        "Floor Number": "階数",
        "Rent (Yen)": "家賃(円)",
        "Maintenance Fee (Yen)": "管理費(円)",
        "Deposit (Yen)": "敷金(円)",
        "Key Money (Yen)": "礼金(円)",
        "Layout": "間取り",
        "Area (m2)": "面積(m2)"
    }
    
    # カラム名を英語から日本語に変更
    df.rename(columns=column_translations_reversed, inplace=True)

    
    # 必要なカラムを整数型に変換
    df['最寄駅1からの時間(分)'] = pd.to_numeric(df['最寄駅1からの時間(分)'], errors='coerce')
    df['家賃(円)'] = pd.to_numeric(df['家賃(円)'], errors='coerce')
    df['築年数(年)'] = pd.to_numeric(df['築年数(年)'], errors='coerce')
    
    return df


def filter_data(df, time_range, layout, rent_range, age_range):
    # 最寄駅からの時間でフィルタリング
    df = df[df['最寄駅1からの時間(分)'].between(time_range[0], time_range[1])]
    # 間取りでフィルタリング
    df = df[df['間取り'].isin(layout)]
    # 家賃でフィルタリング
    df = df[df['家賃(円)'].between(rent_range[0], rent_range[1])]
    # 築年数でフィルタリング
    df = df[df['築年数(年)'].between(age_range[0], age_range[1])]
    return df

def main():
    st.title('Real estate information viewer for Ota Ward, Tokyo')
    st.write('*東京都大田区の不動産情報を検索できます。')

    df = load_data()

    # サイドバーの設定
    st.sidebar.title("▼検索条件")
    time_range = st.sidebar.slider('最寄駅からの時間（分）の範囲', 0, 30, (0, 15), 1)
    layout = st.sidebar.multiselect('間取り', df['間取り'].unique())
    rent_range = st.sidebar.slider('家賃の範囲（円）', 0, 300000, (100000, 150000), 10000)
    age_range = st.sidebar.slider('築年数の範囲（年）', 0, 30, (0, 10), 1)
    
    # 検索ボタン
    if st.sidebar.button('検索'):
        # データのフィルタリング
        filtered_df = filter_data(df, time_range, layout, rent_range, age_range)
        st.dataframe(filtered_df[['物件名', 'アクセス', '間取り', '家賃(円)', '管理費(円)', '敷金(円)', '礼金(円)','建物の階数','面積(m2)','築年数(年)', '住所']], width=1200, height=500)
    else:
        st.write("←左の入力欄から条件を設定し、'検索'ボタンを押してください。")

if __name__ == '__main__':
    main()