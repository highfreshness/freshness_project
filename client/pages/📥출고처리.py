import sys
import streamlit as st
import requests
from datetime import datetime
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from component.config import AP_SERVER_URL

st.title('ð¥ ì¶ê³  ì²ë¦¬')

URL = AP_SERVER_URL + "/deliver/"

qrcode = st.text_input('ìíì QRì ìë ¥í´ì£¼ì¸ì.', max_chars=21)
barcode = qrcode[:14]
ex_date = qrcode[13:17] + "/" + qrcode[17:19] + "/" + qrcode[19:]
ld_cd = datetime.today().strftime("%Y%m%d%H%M%S%f")
ld_dt = datetime.today().strftime("%Y/%m/%d")

if len(qrcode) == 21:
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"ë°ì½ë : {barcode}")
    with col2:
        st.write(f"ì íµê¸°í : {ex_date}")
    
    count = st.number_input("ì¶ê³  ìëì ìë ¥í´ì£¼ì¸ì.", 0, 1000)
    
    datas = {
        "ld_cd": ld_cd,
        "ld_dt": ld_dt,
        "barcode": barcode,
        "ex_dt": ex_date,
        "ld_ct": count
    }
    
    if st.button("ìë ¥"):
        res = requests.post(url=URL, json=datas)
        if res.status_code == 200:
            st.write("ì¶ê³ ìë ¥ì´ ì ìì ì¼ë¡ ìë£ëììµëë¤.")
        else:
            st.write(f"HTTP Response : {res.status_code}")
    
    
else:
    st.write("ì íí QRì½ëë¥¼ ìë ¥í´ì£¼ì¸ì. ë°ì½ë(13) + ë ì§(8) ê¸ìë¡ ì´ 21ê¸ìê° ëì´ì¼ í©ëë¤.")