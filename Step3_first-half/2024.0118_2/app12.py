import streamlit as st
import pandas as pd
import sqlite3
import os
from streamlit_folium import folium_static
import folium
import requests
import urllib

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

# 国土地理院のAPIを利用して緯度と経度を取得する関数
def get_coordinates(address):
    response = requests.get(f"https://msearch.gsi.go.jp/address-search/AddressSearch?q={urllib.parse.quote(address)}")
    if response.json():
        lon, lat = response.json()[0]["geometry"]["coordinates"]
        return [lat, lon]
    else:
        return [None, None]


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
    st.title('Real Estate Analysis Map Viewer for 23 Ward, Tokyo')
    st.write('*東京都23区の不動産情報を検索できます。')
    st.write('*主に2人暮らしをはじめる方向けです。')
    st.write('*気になるエリアの物件の地図を表示できます。')

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
    
    # 検索ボタン
    if st.sidebar.button('検索'):
        # 選択された区に基づいてデータをフィルタリング
        if selected_wards:
            df_filtered_by_wards = df[df['住所'].str.contains('|'.join(selected_wards))]
        else:
            df_filtered_by_wards = df
            
         # その他のフィルターを適用
        filtered_df = filter_data(df_filtered_by_wards, time_range, layout, rent_range, age_range, no_deposit, no_key_money)
        
        # フィルタリングされたデータフレームのインデックスに名前を設定
        filtered_df.index.name = '物件No.'

        
        # フィルタリングされた物件数を表示
        filtered_count = len(filtered_df)
        st.write(f"条件に合った物件数: {filtered_count}")
        st.dataframe(filtered_df.reset_index()[['物件No.', '物件名', 'アクセス', '間取り', '家賃(円)', '管理費(円)', '敷金(円)', '礼金(円)', '階数', '建物の階数', '面積(m2)', '築年数(年)', '住所', 'URL']], width=1500, height=500)
        
        # 住所のカラムにジオコーディングを適用
        filtered_df['Coordinates'] = filtered_df['住所'].apply(get_coordinates)
        
        # フィルタリングされた物件の座標の平均を計算
        valid_coords = filtered_df['Coordinates'].dropna()
        if len(valid_coords) > 0:
            average_lat = valid_coords.apply(lambda x: x[0]).mean()
            average_lon = valid_coords.apply(lambda x: x[1]).mean()
            map_center = [average_lat, average_lon]
        else:
            # 有効な座標がない場合、デフォルトの中心座標を使用
            map_center = [35.6895, 139.6917]

        # 地図の初期化（平均座標を中心として）
        m = folium.Map(location=map_center, zoom_start=12)

        # 各座標にマーカーをプロットし、物件名をポップアップで表示
        for _, row in filtered_df.iterrows():
            coord = row['Coordinates']
            if coord[0] is not None and coord[1] is not None:
                
                folium.Circle(
                location=coord,
                radius=200,
                color='blue',
                fill=True,
                fill_color='blue'
               ).add_to(m)
                
                folium.Marker(
                    location=coord,
                    popup=row['物件名'],
                    icon=folium.Icon(icon='info-sign')
                ).add_to(m)

        # Streamlitアプリに地図を表示
        folium_static(m)
        st.write("※地図上に表示される物件の位置は付近住所に所在することを表すものであり、実際の物件所在地とは異なる場合がございます。")
        st.write("正確な物件所在地は、取扱い不動産会社にお問い合わせください。")
        
    else:
        st.write("←左の入力欄から条件を設定し、'検索'ボタンを押してください。")
            

if __name__ == '__main__':
    main()