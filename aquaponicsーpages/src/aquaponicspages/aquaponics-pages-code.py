import streamlit as st
import requests
import pandas as pd
from PIL import Image
import base64
import os
import subprocess
from functools import lru_cache
st.write("Current working directory:", os.getcwd())
st.write("File exists:", os.path.exists("Image/アクポニイメージ.png"))
def password_authentication():
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if not st.session_state["authenticated"]:
        password = st.text_input("パスワードを入力してください", type="password")
        if st.button("ログイン"):
            if password == "orscwin7":
                st.session_state["authenticated"] = True
                st.success("認証に成功しました。")
            else:
                st.error("パスワードが間違っています。")
                return False
        else:
            return False
    return True

st.set_page_config(
    page_title="ORSC_アクアポニックスWeb",
    page_icon="Image/aqua_icon.png",
    layout="wide"
)

# 画像をリサイズしてキャッシュする関数
@lru_cache(maxsize=32)
def resize_and_cache_image(image_path, new_size):
    image = Image.open(image_path)
    resized_image = image.resize(new_size)
    resized_image_path = f"resized_{os.path.basename(image_path)}"
    resized_image.save(resized_image_path)
    return resized_image_path

# アイコンを表示する関数
@lru_cache(maxsize=32)
def display_icon(image_path, image_url, col, width, height):
    resized_image_path = resize_and_cache_image(image_path, (width, height))
    with open(resized_image_path, "rb") as img_file:
        img_base64 = base64.b64encode(img_file.read()).decode()
    with col:
        st.markdown(
            f'<a href="{image_url}" target="_blank"><img src="data:image/png;base64,{img_base64}" width="{width}" height="{height}"></a>',
            unsafe_allow_html=True
        )

#リサイズの有無を指定して背景画面を表示
def add_bg_with_title(image_file, title_text, resize=False, new_size=(800, 300)):
    if resize:
        # 画像をリサイズしてキャッシュ
        resized_image_path = resize_and_cache_image(image_file, new_size)
        # リサイズした画像をbase64エンコード
        with open(resized_image_path, "rb") as image:
            encoded_string = base64.b64encode(image.read()).decode()
    else:
        # リサイズせずに画像をbase64エンコード
        with open(image_file, "rb") as image:
            encoded_string = base64.b64encode(image.read()).decode()
    
    # 背景画像として表示
    st.markdown(
        f"""
        <style>
        .bg-container {{
            position: relative;
            width: 100%;
            height: {new_size[1]}px;
            background-image: url(data:image/{"png"};base64,{encoded_string});
            background-size: cover;
            background-position: center;
        }}
        .title-text {{
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-size: 48px;
            color: white;
            text-align: center;
            white-space: nowrap;
            background-color: rgba(0, 0, 0, 0.5);
            padding: 20px;
            border-radius: 10px;
        }}
        </style>
        <div class="bg-container"><div class="title-text">{title_text}</div></div>
        """,
        unsafe_allow_html=True
    )

# サイドバーにタブを作成
tab = st.sidebar.radio("メニュー", ["ホーム", "計測状況", "ハウスカメラ", "サイト管理"])

# サイドバーにアイコンを表示する関数
@lru_cache(maxsize=32)
def display_sidebar_icon(image_path, image_url, width, height):
    resized_image_path = resize_and_cache_image(image_path, (width, height))
    with open(resized_image_path, "rb") as img_file:
        img_base64 = base64.b64encode(img_file.read()).decode()
    st.markdown(
        f'<div style="text-align: center;"><a href="{image_url}" target="_blank">'
        f'<img src="data:image/png;base64,{img_base64}" width="{width}" height="{height}"></a></div>',
        unsafe_allow_html=True
    )

# ユーザーの権限を管理するためのデータ(adminの権限保有者は「サイト管理」へのアクセス権限持つよう調整)
user_data = {
    "tsuyoshi.sato@orsc.co.jp": {"password": "abeshi1129", "role": "admin"},
    "daichi.nakagawa@orsc.co.jp": {"password": "orscwin7", "role": "admin"},
    "akihisa.iwasaki@orsc.co.jp": {"password": "orscwin7", "role": "admin"},
    # 他のユーザーを追加可能
    # サイト管理に権限を与えない場合admin→"viewer"　
}

# 認証状態を管理する関数
def authenticate_user(email, password):
    if email in user_data and user_data[email]["password"] == password:
        st.session_state["authenticated"] = True
        st.session_state["user_email"] = email
        st.session_state["user_role"] = user_data[email]["role"]
        return True
    else:
        st.error("メールアドレスまたはパスワードが間違っています。")
        return False

# 認証フォームを表示する関数
def login_form():
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if not st.session_state["authenticated"]:
        st.subheader("ログイン")
        email = st.text_input("メールアドレス")
        password = st.text_input("パスワード", type="password")
        if st.button("ログイン"):
            authenticate_user(email, password)


if tab == "ホーム":
    if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
        login_form()
    else:
        add_bg_with_title("Image/アクポニイメージ.png", "アクアポニックス計測システム", resize=False)
        col_akuponimain, col_moukaweather = st.columns([5, 2])

        with col_akuponimain:
            st.write("アイコンをクリックすると各ページのURLを参照します。")
            st.markdown('<h1 class="custom-title">計測データ</h1>', unsafe_allow_html=True)
            col0, col1,col2= st.columns(3)
            with st.spinner('アイコンを読み込み中...'):
                display_icon("Image/アクポニ打ち合わせ資料.png", "https://drive.google.com/drive/folders/1NaMoLD8Xrt2akZncrEwc382uh-dL8Sj5/", col0, 200,200)
                display_icon("Image/アクポニPLC計測データ.png", "https://drive.google.com/drive/folders/0AHHJiTXY2uaDUk9PVA", col1, 200, 200)
                display_icon("Image/アクポニモニタリング結果共有.png", "https://drive.google.com/drive/folders/0AG1YIuJ5NR6yUk9PVA", col2, 200,200)

            st.markdown('<h1 class="custom-title">ハウスカメラ映像（開発中）</h1>', unsafe_allow_html=True)
            st.write("該当ポイントをクリックすると映像が確認できます")
            col_iwasaki,col_camera1,_= st.columns(3)
            usename = "admin"
            password = "aqua0285"
            camera_url1 = f"https://{usename}:{password}@10.14.71.122/"
            # アイコンのリンクとして使用
            display_icon("Image/技術部共有.png", camera_url1, col_camera1, 150, 150)
            display_icon("Image/岩崎開発中.png", "http://10.14.71.136:8000/", col_iwasaki, 150,150)

            col_satoaqua,_,_ =st.columns(3)
            display_icon("Image/sato_kaihatuchuu.png", "https://orsc-aquaponics-pages-zp27terjwfvoxrmyhcvjqp.streamlit.app/", col_satoaqua, 150, 150)


                    
        with col_moukaweather:
            url = "https://weathernews.jp/onebox/radar/tochigi/09209/"
            st.components.v1.iframe(src=url, width=400, height=700)
