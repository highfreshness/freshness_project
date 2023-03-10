import sys
import socket
import streamlit as st
import requests
import pandas as pd
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from component.config import AP_SERVER_URL 

URL = AP_SERVER_URL + "/item"

st.title('π μν μ‘°ν')

product = st.text_input("μ‘°νν  μνμ λ°μ½λλ₯Ό μλ ₯ν΄μ£ΌμΈμ.")

if st.button('μ‘°ν'):
    if product == None:
        res = requests.get(url=URL, timeout=3) # μ μ²΄ μ‘°ν
        print(res.json())
        if len(res.json()) == 0:
            st.write("λ±λ‘λ μνμ΄ μμ΅λλ€.")
        else:
            df = pd.DataFrame.from_records(res.json())
            df = df[['item_cd', 'item_nm', 'item_cat_nm', 'item_maker']]
            df.rename(columns={'item_cd':'λ°μ½λ', 'item_nm':'μνλͺ', 'item_cat_nm':'μν λΆλ₯', 'item_maker':'μ μ‘°μ¬'}, inplace=True)
            st.dataframe(df)
    else:
        res = requests.get(url=URL, params={"barcode" : product},  timeout=3)
        df = pd.DataFrame.from_records(res.json())
        df = df[['item_cd', 'item_nm', 'item_cat_nm', 'item_maker']]
        df.rename(columns={'item_cd':'λ°μ½λ', 'item_nm':'μνλͺ', 'item_cat_nm':'μν λΆλ₯', 'item_maker':'μ μ‘°μ¬'}, inplace=True)
        st.dataframe(df)
