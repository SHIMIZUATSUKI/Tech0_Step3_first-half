import streamlit as st

# タイトルの設定
st.title('My Streamlit App')

# ユーザーにテキスト入力を促す
user_input = st.text_input("あなたの名前を入力してください", '')

# テキストを画面に表示
st.write(f'こんにちは、{user_input}！')
