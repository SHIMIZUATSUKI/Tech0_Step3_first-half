import streamlit as st
import pandas as pd
import sqlite3
import os
from streamlit_folium import folium_static
import folium
import requests
import urllib




import streamlit as st
from PIL import Image
import os

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

import streamlit as st

# サイドバーにタイトルを追加
st.sidebar.title("REAの機能")

# サイドバーにリンクを追加
st.sidebar.markdown("[物件の地図を表示する](https://tech0step3first-half-ftb9oi6xikjbwqxmzfvxpq.streamlit.app/)")
st.sidebar.markdown("[費用をシュミレーションする](https://tech0step3first-half-mvckdwx53mvpnxuvsm6dbf.streamlit.app/)")
st.sidebar.markdown("[周辺相場を見る](https://tech0step3first-half-9kcibptsuvr2ezjevrdhbx.streamlit.app/)")



