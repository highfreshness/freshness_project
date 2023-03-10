import sys
import streamlit as st
import requests
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
sys.path.append(str(Path(__file__).resolve().parent.parent))
from component.config import AP_SERVER_URL 

URL = AP_SERVER_URL + "/ex_date/"

st.title('π μ ν΅κΈ°ν μ‘°ν')

col1, col2, col3 = st.columns(3)

with col1:
    days_7 = st.button("7μΌ")
    
with col2:
    days_14 = st.button("14μΌ")
    
with col3:
    days_21 = st.button("21μΌ")
    
if days_7:
    today = datetime.today().strftime("%Y/%m/%d")
    ex_date = datetime.today() + timedelta(days=7)
    ex_date = ex_date.strftime("%Y/%m/%d")
    res = requests.get(url=URL, params={"today":today, "ex_date":ex_date})
    if res.status_code == 200:    
        if len(res.json()) == 0 :
            st.write("ν΄λΉ κΈ°κ° λ΄ μ ν΅κΈ°ν λλ μνμ΄ μ‘΄μ¬νμ§ μμ΅λλ€.")
        else:
            df = pd.DataFrame.from_records(res.json())
            df = df[['ls_cd', 'barcode', 'ls_dt', 'ex_dt', 'ls_ct']]
            df.rename(columns={'ls_cd':'μκ³ μ½λ', 'ls_dt':'μκ³ μΌμ', 'ex_dt':'μ ν¨κΈ°κ°', 'ls_ct':'μλ'}, inplace=True)
            st.dataframe(df)
    else:
        st.write("νμ¬ ν΅μ μ΄ μννμ§ μμ΅λλ€. κ΄λ¦¬μλ₯Ό μ°Ύμμ£ΌμΈμ")
            
elif days_14:
    today = datetime.today().strftime("%Y/%m/%d")
    ex_date = datetime.today() + timedelta(days=14)
    ex_date = ex_date.strftime("%Y/%m/%d")
    res = requests.get(url=URL, params={"today":today, "ex_date":ex_date})
    if res.status_code == 200:    
        if len(res.json()) == 0 :
            st.write("ν΄λΉ κΈ°κ° λ΄ μ ν΅κΈ°ν λλ μνμ΄ μ‘΄μ¬νμ§ μμ΅λλ€.")
        else:
            df = pd.DataFrame.from_records(res.json())
            df = df[['ls_cd', 'barcode', 'ls_dt', 'ex_dt', 'ls_ct']]
            df.rename(columns={'ls_cd':'μκ³ μ½λ', 'ls_dt':'μκ³ μΌμ', 'ex_dt':'μ ν¨κΈ°κ°', 'ls_ct':'μλ'}, inplace=True)
            st.dataframe(df)
    else:
        st.write("νμ¬ ν΅μ μ΄ μννμ§ μμ΅λλ€. κ΄λ¦¬μλ₯Ό μ°Ύμμ£ΌμΈμ")
        
elif days_21:
    today = datetime.today().strftime("%Y/%m/%d")
    ex_date = datetime.today() + timedelta(days=21)
    ex_date = ex_date.strftime("%Y/%m/%d")
    res = requests.get(url=URL, params={"today":today, "ex_date":ex_date})
    if res.status_code == 200:    
        if len(res.json()) == 0 :
            st.write("ν΄λΉ κΈ°κ° λ΄ μ ν΅κΈ°ν λλ μνμ΄ μ‘΄μ¬νμ§ μμ΅λλ€.")
        else:
            df = pd.DataFrame.from_records(res.json())
            df = df[['ls_cd', 'barcode', 'ls_dt', 'ex_dt', 'ls_ct']]
            df.rename(columns={'ls_cd':'μκ³ μ½λ', 'ls_dt':'μκ³ μΌμ', 'ex_dt':'μ ν¨κΈ°κ°', 'ls_ct':'μλ'}, inplace=True)
            st.dataframe(df)
    else:
        st.write("νμ¬ ν΅μ μ΄ μννμ§ μμ΅λλ€. κ΄λ¦¬μλ₯Ό μ°Ύμμ£ΌμΈμ")