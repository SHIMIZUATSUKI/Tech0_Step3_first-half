import streamlit as st
import pandas as pd
import sqlite3
import os
from streamlit_folium import folium_static
import folium
import requests
import urllib
from PIL import Image
import base64


# 画像ファイルの名前を指定
image_file = "REA.jpg"

# 現在のディレクトリのパスを取得
current_dir = os.path.dirname(os.path.realpath(__file__))

# 画像ファイルへの完全なパスを組み立て
image_path = os.path.join(current_dir, image_file)

# 画像を読み込み
image = Image.open(image_path)

# 画像を表示
st.image(image, caption='Your Image Caption', use_column_width=True)

st.title('REA')
st.write('Real Estate Analysis app')
st.write('*不動産情報を分析できるアプリです。')
st.write('*本アプリでは主に2人暮らしの方をターゲットにした東京都23区不動産情報を扱っています。')
st.write('*REAを使って、納得いく物件探しにトライしてみましょう!')
st.write('←左の画面から使いたい機能を選んでください。')


# サイドバーにタイトルを追加
st.sidebar.title("REAの機能")

# サイドバーにリンクを追加
# サイドバーに画像リンクを追加
link1 = "https://tech0step3first-half-ftb9oi6xikjbwqxmzfvxpq.streamlit.app/"
link2 = "https://tech0step3first-half-mvckdwx53mvpnxuvsm6dbf.streamlit.app/"
link3 = "https://tech0step3first-half-9kcibptsuvr2ezjevrdhbx.streamlit.app/"

# 各機能の画像ファイル名を指定（例として、仮のファイル名を使用しています）
image_file1 = "map.jpg"
image_file2 = "simulation.jpg"
image_file3 = "analysis.jpg"




# 画像へのパスを作成
image_path1 = os.path.join(current_dir, image_file1)
image_path2 = os.path.join(current_dir, image_file2)
image_path3 = os.path.join(current_dir, image_file3)


def get_image_as_base64(path):
    with open(path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# 画像のBase64エンコーディングを取得
encoded_image1 = get_image_as_base64(image_path1)
encoded_image2 = get_image_as_base64(image_path2)
encoded_image3 = get_image_as_base64(image_path3)

# HTMLを使ってサイドバーに画像リンクを追加
st.sidebar.write('▼画像をクリック')

st.sidebar.write('■ 物件の所在地を調べる')
st.sidebar.markdown(f'<a href="{link1}" target="_blank"><img src="data:image/jpeg;base64,{encoded_image1}" alt="物件の地図を表示する" style="width:100%;"></a>', unsafe_allow_html=True)
st.sidebar.write('■ 物件の費用をシュミレーションする')
st.sidebar.markdown(f'<a href="{link2}" target="_blank"><img src="data:image/jpeg;base64,{encoded_image2}" alt="費用をシュミレーションする" style="width:100%;"></a>', unsafe_allow_html=True)
st.sidebar.write('■ 物件の周辺相場をみる')
st.sidebar.markdown(f'<a href="{link3}" target="_blank"><img src="data:image/jpeg;base64,{encoded_image3}" alt="周辺相場を見る" style="width:100%;"></a>', unsafe_allow_html=True)
