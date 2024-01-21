import streamlit as st
import pandas as pd
import sqlite3
import os
from streamlit_folium import folium_static
import folium
import requests
import urllib

st.title('REA')
st.write('Real Estate analysis app')
st.write('*東京都23区の不動産情報を検索できます。')
st.write('*主に2人暮らしをはじめる方向けです。')