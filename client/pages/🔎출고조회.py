import sys
import streamlit as st
import requests
import pandas as pd
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from component.config import AP_SERVER_URL 
URL = AP_SERVER_URL + "/deliver/"

st.title('๐ ์ถ๊ณ  ์กฐํ')

col1, col2 = st.columns(2)

with col1:
    front_time = st.date_input("์กฐํ ์์ ๊ธฐ๊ฐ")
    front_time = str(front_time).replace("-", "/")
with col2:
    back_time = st.date_input("์กฐํ ์ข๋ฃ ๊ธฐ๊ฐ")
    back_time = str(back_time).replace("-", "/")
    
if st.button('์กฐํ'):
    if front_time != None and back_time != None:
        res = requests.get(url=URL, params = {"period_front":front_time, "period_back":back_time})
    deliver_json = res.json() # type = list

    if len(deliver_json) == 0:
        st.write("ํด๋น ๊ธฐ๊ฐ์ ์๊ณ ๋ ๋ด์ญ์ด ์์ต๋๋ค.")
    else:
        df = pd.DataFrame.from_records(deliver_json)
        df = df[['ld_cd', 'ld_dt', 'ex_dt', 'ld_ct', 'barcode']]
        df.rename(columns={'barcode':'๋ฐ์ฝ๋', 'ld_cd':'์ถ๊ณ ์ฝ๋', 'ex_dt':'์ ํจ๊ธฐ๊ฐ', 'ld_dt':'์ถ๊ณ ์ผ์', 'ld_ct':'์๋'}, inplace=True)
        st.dataframe(df)
