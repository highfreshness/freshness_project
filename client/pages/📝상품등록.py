import sys
import requests
import streamlit as st
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from component.config import AP_SERVER_URL

URL = AP_SERVER_URL + "/item/"

st.title('π μν λ±λ‘')

item_cd = st.text_input("λ°μ½λ")

col1, col2, col3= st.columns(3)

with col1:
    item_nm = st.text_input("μ νλͺ")
    
with col2:
    item_cat_nm = st.text_input("λΆλ₯")
    
with col3:
    item_maker = st.text_input("μ μ‘°μ¬")
    
if st.button("μ μ‘"):
    if item_cd and item_cat_nm and item_nm and item_maker:
        datas = {
            "item_cd": item_cd,
            "item_nm": item_nm,
            "item_cat_nm": item_cat_nm,
            "item_maker" : item_maker
        }
        res = requests.post(url = URL, json=datas, timeout=3)
        print(res.json())
        
        print(type(res.json()))
        if res.status_code == 200:
            st.write("μνμ΄ μ μμ μΌλ‘ λ±λ‘λμμ΅λλ€.")
            st.write(f"λ±λ‘λ μν : {res.json()['item_nm']}")
        else:
            st.write("μνμ΄ μ μμ μΌλ‘ λ±λ‘λμ§ μμμ΅λλ€. λ°μ½λ λλ μλ ₯κ°μ νμΈν΄μ£ΌμΈμ")
    else:
        st.write("λΉ ν­λͺ©μ΄ μμ΅λλ€. λ€μ νμΈ ν΄μ£ΌμΈμ")