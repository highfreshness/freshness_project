import sys
import streamlit as st
import requests
import pandas as pd
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from component.config import AP_SERVER_URL 
URL = AP_SERVER_URL + "/stock/"

st.title('π μκ³  μ‘°ν')

col1, col2 = st.columns(2)

with col1:
    front_time = st.date_input("μ‘°ν μμ κΈ°κ°")
    front_time = str(front_time).replace("-", "/")
with col2:
    back_time = st.date_input("μ‘°ν μ’λ£ κΈ°κ°")
    back_time = str(back_time).replace("-", "/")
if st.button('μκ³  μ‘°ν'):
    if front_time != None and back_time != None:
        res = requests.get(url=URL, params = {"period_front":front_time, "period_back":back_time})
    stock_json = res.json() # type = list

    if len(stock_json) == 0:
        st.write("ν΄λΉ κΈ°κ°μ μκ³ λ λ΄μ­μ΄ μμ΅λλ€.")
    else:
        df = pd.DataFrame.from_records(stock_json)
        df = df[['ls_cd', 'ls_dt', 'ex_dt', 'ls_ct', 'barcode']]
        df.rename(columns={'barcode':'λ°μ½λ', 'ls_cd':'μκ³ μ½λ', 'ex_dt':'μ ν¨κΈ°κ°', 'ls_dt':'μκ³ μΌμ', 'ls_ct':'μλ'}, inplace=True)
        st.dataframe(df)
