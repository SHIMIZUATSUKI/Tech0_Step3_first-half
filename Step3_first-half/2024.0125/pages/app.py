import streamlit as st
import pandas as pd
import sqlite3
import os
from streamlit_folium import folium_static
import folium
import requests
import urllib
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.font_manager as font_manager
import numpy as np

# Define the font family you want to use
matplotlib.rcParams['font.family'] = 'Helvetica'

# Streamlitのキャッシュデコレータを追加して、データの読み込みを高速化
@st.cache(ttl=3600, max_entries=10, allow_output_mutation=True)
def load_data():
    # 現在のファイルのディレクトリを取得
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # データベースファイルへのパスを構築
    db_path = os.path.join(current_dir, 'Tokyo23_RealEatate_DB.db')
    # データベースに接続
    conn = sqlite3.connect(db_path)
    # SQLクエリを実行し、結果をDataFrameに読み込む
    query = 'SELECT * FROM "Tokyo_23"'
    df = pd.read_sql_query(query, conn)
    # 英語のカラム名を日本語に変更する変換
    column_translations_reversed = {
        "Property Name": "物件名",
        "Property Photo": "物件写真",
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
        "Area (m2)": "面積(m2)",
        "URL":"URL"
    }
    
    # カラム名を英語から日本語に変更
    df.rename(columns=column_translations_reversed, inplace=True)

    
    # 必要なカラムを整数型に変換
    df['最寄駅1からの時間(分)'] = pd.to_numeric(df['最寄駅1からの時間(分)'], errors='coerce')
    df['家賃(円)'] = pd.to_numeric(df['家賃(円)'], errors='coerce')
    df['築年数(年)'] = pd.to_numeric(df['築年数(年)'], errors='coerce')
    
    
    
    
    
    conn.close()  # データベース接続を閉じる
    return df


def filter_data(df, time_range, layout, rent_range, age_range, no_deposit, no_key_money):
    # 最寄駅からの時間でフィルタリング
    df = df[df['最寄駅1からの時間(分)'].between(time_range[0], time_range[1])]
    # 間取りでフィルタリング
    df = df[df['間取り'].isin(layout)]
    # 家賃でフィルタリング
    df = df[df['家賃(円)'].between(rent_range[0], rent_range[1])]
    # 築年数でフィルタリング
    df = df[df['築年数(年)'].between(age_range[0], age_range[1])]
    # 敷金のフィルタリング
    if no_deposit:
        df = df[df['敷金(円)'] == 0]
    
    # 礼金のフィルタリング
    if no_key_money:
        df = df[df['礼金(円)'] == 0]
        
    return df

# 東京23区をアイウエオ順に並べたリスト
wards_of_tokyo = ["足立区", "荒川区", "板橋区", "江戸川区", "大田区", "葛飾区", "北区", "江東区", 
                  "品川区", "渋谷区", "新宿区", "杉並区", "墨田区", "世田谷区", "台東区", "中央区", 
                  "千代田区", "豊島区", "中野区", "練馬区", "目黒区", "文京区", "港区"]

def main():
    st.title('Real Estate Analysis Reasearch MarketPrice for 23 Ward, Tokyo')
    st.write('*東京都23区の不動産情報を検索できます。')
    st.write('*主に2人暮らしをはじめる方向けです。')
    st.write('*気になった物件の家賃の相場を調査できます。')

    df = load_data()

    # サイドバーの設定
    st.sidebar.title("▼検索条件")
    
    # サイドバーで東京23区を選択
    selected_wards = st.sidebar.multiselect('23区を選択', wards_of_tokyo)
    #各種細かい条件設定
    #家賃・敷金・礼金
    rent_range = st.sidebar.slider('家賃の範囲（円）', 100000, 300000, (150000, 200000), 10000)
    # サイドバーで敷金・礼金の有無の選択
    no_deposit = st.sidebar.checkbox('敷金なし')
    no_key_money = st.sidebar.checkbox('礼金なし')
    #物件の立地
    time_range = st.sidebar.slider('最寄駅からの時間（分）の範囲', 0, 30, (0, 15), 1)
    layout = st.sidebar.multiselect('間取り', df['間取り'].unique())
    age_range = st.sidebar.slider('築年数の範囲（年）', 0, 30, (0, 10), 1)
    
    st.write("←左の入力欄から条件を設定し、'検索'ボタンを押してください。")
    
    # 散布図とヒストグラムの作成に必要なサイドバー項目を追加
    scatter_x_options = ['最寄駅1からの時間(分)', '築年数(年)', '面積(m2)']

    
    # 検索ボタン
    if st.sidebar.button('検索'):
        # 選択された区に基づいてデータをフィルタリング
        if selected_wards:
            df_filtered_by_wards = df[df['住所'].str.contains('|'.join(selected_wards))]
        else:
            df_filtered_by_wards = df
            
            
        # その他のフィルターを適用
        st.session_state['filtered_df'] = filter_data(df_filtered_by_wards, time_range, layout, rent_range, age_range, no_deposit, no_key_money)
        
    # 物件Noの選択と詳細の表示
    if 'filtered_df' in st.session_state and len(st.session_state['filtered_df']) > 0:
        filtered_df = st.session_state['filtered_df']
        filtered_df.index.name = '物件No.'
        st.write(f"条件に合った物件数: {len(filtered_df)}")
        st.dataframe(filtered_df.reset_index()[['物件No.', '物件名', 'アクセス', '間取り', '家賃(円)', '管理費(円)', '敷金(円)', '礼金(円)', '建物の階数', '面積(m2)', '築年数(年)', '住所', 'URL']], width=1500, height=500)
        
        property_no = st.selectbox('物件Noを選択してください', filtered_df.index, index=0)

        if property_no is not None:
            selected_property = filtered_df.loc[property_no]
            st.write('物件名:', selected_property['物件名'])
            st.image(selected_property['物件写真'], caption='物件写真')
            st.markdown(f"[物件の詳細]({selected_property['URL']})", unsafe_allow_html=True)

            # 費用シミュレーション
            initial_cost = selected_property['敷金(円)'] + selected_property['礼金(円)']
            monthly_cost = selected_property['家賃(円)'] + selected_property['管理費(円)']
            annual_cost = (selected_property['家賃(円)'] + selected_property['管理費(円)']) * 12

            st.write('初期費用:', initial_cost, '円')
            st.write('1ヶ月の費用:', monthly_cost, '円')
            st.write('1年間の費用:', annual_cost, '円')
            st.write('*初期費用は敷金と礼金を合計した金額です。')    

            # 散布図を描画
            # scatter_x_options = ['最寄駅1からの時間(分)', '築年数(年)', '面積(m2)']
            for feature in scatter_x_options:
                fig, ax = plt.subplots()
                # 選択された物件以外を青色でプロット
                ax.scatter(filtered_df[filtered_df.index != property_no][feature], 
                        filtered_df[filtered_df.index != property_no]['家賃(円)'],
                        color='blue', label='その他の物件')
                # 選択された物件を赤色でプロット
                if property_no in filtered_df.index:
                    ax.scatter(filtered_df.loc[property_no, feature], 
                            filtered_df.loc[property_no, '家賃(円)'],
                            color='red', label='選択された物件')
                
                ax.set_xlabel(feature, fontsize=14)
                ax.set_ylabel('家賃(円)', fontsize=14)
                ax.set_title(f'家賃 vs {feature}', fontsize=16)
                ax.legend()
                st.pyplot(fig)
            
            
            # 家賃のヒストグラム
            fig, ax = plt.subplots()
            counts, bins, patches = ax.hist(filtered_df['家賃(円)'], bins=20, color='skyblue')

            # 選択された物件がどのビンに属するかを見つける
            bin_index = np.digitize([selected_property['家賃(円)']], bins)[0] - 1
            patches[bin_index].set_facecolor('red')

            ax.set_title('家賃のヒストグラム')
            ax.set_xlabel('家賃(円)')
            ax.set_ylabel('件数')
            st.pyplot(fig)
            
            # 最寄駅1からの時間(分)のヒストグラム
            fig, ax = plt.subplots()
            counts, bins, patches = ax.hist(filtered_df['最寄駅1からの時間(分)'], bins=20, color='skyblue')

            bin_index = np.digitize([selected_property['最寄駅1からの時間(分)']], bins)[0] - 1
            patches[bin_index].set_facecolor('red')

            ax.set_title('最寄駅1からの時間のヒストグラム')
            ax.set_xlabel('最寄駅1からの時間(分)')
            ax.set_ylabel('件数')
            st.pyplot(fig)


            # 築年数のヒストグラム
            fig, ax = plt.subplots()
            counts, bins, patches = ax.hist(filtered_df['築年数(年)'], bins=20, color='skyblue')

            bin_index = np.digitize([selected_property['築年数(年)']], bins)[0] - 1
            patches[bin_index].set_facecolor('red')

            ax.set_title('築年数のヒストグラム')
            ax.set_xlabel('築年数(年)')
            ax.set_ylabel('件数')
            st.pyplot(fig)

            # 面積(m2)のヒストグラム
            fig, ax = plt.subplots()
            counts, bins, patches = ax.hist(filtered_df['面積(m2)'], bins=20, color='skyblue')

            bin_index = np.digitize([selected_property['面積(m2)']], bins)[0] - 1
            patches[bin_index].set_facecolor('red')

            ax.set_title('面積のヒストグラム')
            ax.set_xlabel('面積(m2)')
            ax.set_ylabel('件数')
            st.pyplot(fig)


            
            
        else:
            st.write('該当の物件はございません。')

if __name__ == '__main__':
    main()