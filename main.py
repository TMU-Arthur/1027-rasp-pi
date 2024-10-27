import streamlit as st
from firebase import firebase
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
import requests

url = "https://rasp-pi-505c8-default-rtdb.asia-southeast1.firebasedatabase.app"
line_url = 'https://notify-api.line.me/api/notify'
line_token = "DA9gx3gp66ZhjReg20NB4d1co5MoTNoXdvk0cvUE1eX"

fdb = firebase.FirebaseApplication(url, None)

st.title("Dashboard")
st.button("Refresh")

item_list = []

try:
    for i in fdb.get('/', ''):
        item_list.append(fdb.get(i,""))

    df = pd.DataFrame(item_list)
    st.write(df)

    df_hnt = {
        'Humidity': pd.Series([round(random.uniform(70,78), 1) for i in range(10)]),
        'Temperature': pd.Series([round(random.uniform(26,28), 1) for i in range(10)]),
        'PM2.5': pd.Series([round(random.uniform(80,100), 1) for i in range(10)]),
    }

    st.line_chart(pd.DataFrame(df_hnt))

    st.markdown("### Temperature")
    df_temp = df_hnt['Temperature']
    st.line_chart(df_temp)

    temp = df_hnt['Temperature'].iloc[-1]
    st.write("Temperature:", temp)

    st.markdown("### Humidity")
    df_humid = df_hnt['Humidity']
    st.line_chart(df_humid)

    humid = df_hnt['Humidity'].iloc[-1]
    st.write("Humidity:", humid)

    st.markdown("### PM2.5")
    df_pm = df_hnt['PM2.5']
    st.line_chart(df_pm)

    pm = df_hnt['PM2.5'].iloc[-1]
    st.write("PM2.5:", pm)

    st.markdown("### 設定Line通知")
    if st.button("Send Line Notification"):
        headers = {'Authorization': 'Bearer ' + line_token}
        data = {
            'message':df_temp    # 設定要發送的訊息
        }
        requests.post(line_url, headers=headers, data=data)   # 使用 POST 方法
except:
    st.error("No data available")
