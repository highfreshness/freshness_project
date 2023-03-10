# import os 
import sys
from pathlib import Path

# os.environ['DISPLAY'] = ':0'
sys.path.append(str(Path(__file__).resolve().parent.parent))

import streamlit as st
from webcam import webcam
from datetime import datetime
import requests
import re
# import pyautogui
import qrcode

from component.config import INFERENCE_SERVER_URL, AP_SERVER_URL
from component.func import ImageFile
from component.post_processing import get_expdate

PICTURE_URL = AP_SERVER_URL + "/picture/"
STOCK = AP_SERVER_URL + "/stock/"
# ๊ธฐ๋ณธ ์ค์ 
if 'last' not in st.session_state:
    st.session_state.last = None

if "button_clicked" not in st.session_state:
    st.session_state.button_clicked = False
                    
def button_clicked():
    st.session_state.button_clicked = True


st.title('๐ฅ ์๊ณ ์ฒ๋ฆฌ')

barcode = st.text_input('๋น ์นธ์ ๋ฐ์ฝ๋๋ฅผ ์๋ ฅํด์ฃผ์ธ์.', placeholder='13์๋ฆฌ๋ฅผ ์๋ ฅํด์ฃผ์ธ์', max_chars=13)

        
if len(barcode) == 13:
    check_cam = st.radio(label = '< ๋ด์ฅ์บ  / ์น์บ  > ์ ์ ํํด์ฃผ์ธ์.', options = ['Maincam', 'Webcam'])
    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
        
    if check_cam == 'Maincam': # ๋ด์ฅ ์บ ์ธ ๊ฒฝ์ฐ

        image_file = ImageFile()
        captured_image = st.camera_input('์ํ์ ์ ํต๊ธฐํ์ ์ธ์ํด์ฃผ์ธ์.')

        if captured_image is None:
            st.write('์ ๋ฉด์ผ๋ก ์ธ์๋์๋ค๋ฉด <Take Photo> ๋ฅผ ๋๋ฌ์ฃผ์ธ์.')
            
        else:
            buffered_stream = image_file.image_to_buffer(captured_image)
            upload = {'file': buffered_stream}
            print(upload)

            # ์ถ๋ก 
            inference = requests.post(url=INFERENCE_SERVER_URL, files=upload)
            exp_date = get_expdate(inference.json()["exp_date"])
            print("์ถ๋ก  ๊ฒฐ๊ณผ :", inference, inference.text)

            # ํ๋ฉด์ ํ์ํ  ์ ๋ณด
            st.write(f'< ๋ฐ์ฝ๋๋ฒํธ : {barcode}>')
            st.write('์ํ์ ๋ณด : ์ํ')
            st.write(f'์ ํต๊ธฐํ : {exp_date}')
            st.write('-------')

            # ์ฌ์ดฌ์์ธ ๊ฒฝ์ฐ ์ฌํ์ต์ฉ DB ์๋ฒ๋ก ๋ณด๋
            if st.session_state.last != None:
                buffered_stream = image_file.image_to_buffer(captured_image)
                upload = {'file': buffered_stream}
                res = requests.post(url=PICTURE_URL, files=upload)
                print("์ฌ์ดฌ์ ์ด๋ฏธ์ง ์ ์ก ๊ฒฐ๊ณผ :", res, res.text)

                st.session_state.last = buffered_stream # ๋ค์ ์ดฌ์ ์ ๋ณด๋ด๊ธฐ ์ํด ์ ์ฅ
                image_file.drop_image(buffered_stream) # ์ด๋ฏธ์ง ํ์ผ ์ญ์ 
            
            else:
                st.session_state.last = buffered_stream
            

            # ์์ธก๋ ์ ํต๊ธฐํ์ ๊ทธ๋๋ก ์ฌ์ฉํ ์ง(ํ์ธ), ์์ ํ์ฌ ์ฌ์ฉํ ์ง(์ง์ ์๋ ฅ) ์ ํ
            check_info = st.radio(label = '์ ํต๊ธฐํ ์ ๋ณด๋ฅผ ํ์ธํด์ฃผ์ธ์.', options = ['ํ์ธ', '์ง์ ์๋ ฅ'])     
            
            # ํ์ธ
            if check_info == 'ํ์ธ':
                count = st.number_input('์๋์ ์๋ ฅํด์ฃผ์ธ์.', 0, 1000)
                
                if st.button('QR ์์ฑ'):
                    exp_date_num = re.sub(r'[^0-9]', '', str(exp_date))   
                    img = qrcode.make(f"{barcode}{exp_date_num}")
                    img.save(f"./pages/qr_code/{barcode}{exp_date_num}.jpg")
                    st.image(f"./pages/qr_code/{barcode}{exp_date_num}.jpg")

                if st.button('๋ฑ๋ก'):
                    ls_dt = datetime.now()
                    ls_dt = ls_dt.strftime('%Y/%m/%d')

                    ls_cd = datetime.today().strftime("%Y%m%d%H%M%S%f")

                    data = {
                        'ls_cd': ls_cd,
                        'ls_dt': ls_dt,
                        'barcode': barcode,
                        'ex_dt': str(exp_date),
                        'ls_ct': count
                        }

                    res = requests.post(url=STOCK, json=data)
                    print("์๊ณ  DB ์ ์ก ๊ฒฐ๊ณผ :", res, res.text)
                    st.success(f' < ๋ฐ์ฝ๋๋ฒํธ : {barcode} / {count} ๊ฐ > ๋ฑ๋ก๋์์ต๋๋ค ')
                    #pyautogui.press("f5", presses=1, interval=0.2)
                
            # ์ง์  ์๋ ฅ
            else :
                ex1, co2 = st.columns(2)
                with ex1 :
                    exp_date = st.date_input('์ ํต๊ธฐํ์ ์๋ ฅํด์ฃผ์ธ์.')
                    exp_date = str(exp_date).replace('-', '/')
                with co2 :
                    count = st.number_input('์๋์ ์๋ ฅํด์ฃผ์ธ์', 0, 1000)
                    
                if st.button('QR ์์ฑ'):
                    exp_date_num = re.sub(r'[^0-9]', '', str(exp_date))   
                    img = qrcode.make(f"{barcode}{exp_date_num}")
                    img.save(f"./pages/qr_code/{barcode}{exp_date_num}.jpg")
                    st.image(f"./pages/qr_code/{barcode}{exp_date_num}.jpg")

                if st.button('๋ฑ๋ก'):
                    ls_dt = datetime.now()
                    ls_dt = ls_dt.strftime('%Y/%m/%d')

                    ls_cd = datetime.today().strftime("%Y%m%d%H%M%S%f")

                    data = {
                        'ls_cd': ls_cd,
                        'ls_dt': ls_dt,
                        'barcode': barcode,
                        'ex_dt': str(exp_date),
                        'ls_ct': count
                        }

                    res = requests.post(url=STOCK, json=data)
                    print("์๊ณ  DB ์ ์ก ๊ฒฐ๊ณผ :", res, res.text)
                    st.success(f' < ๋ฐ์ฝ๋๋ฒํธ : {barcode} / {count} ๊ฐ > ๋ฑ๋ก๋์์ต๋๋ค ')
                    #pyautogui.press("f5", presses=1, interval=0.2)

    # ์ธ์ฅ ์บ ์ธ ๊ฒฝ์ฐ           
    else:
        image_file = ImageFile()
        captured_image = webcam('์ํ์ ์ ํต๊ธฐํ์ ์ธ์ํด์ฃผ์ธ์')
        
        if captured_image is None:
            st.write('์ ๋ฉด์ผ๋ก ์ธ์๋์๋ค๋ฉด <Capture frame> ์ ๋๋ฌ์ฃผ์ธ์')
            
        else:
            buffered_stream = image_file.image_to_buffer(captured_image)
            upload = {'file': buffered_stream}

            # ์ถ๋ก 
            inference = requests.post(url=INFERENCE_SERVER_URL, files=upload)
            exp_date = get_expdate(inference.json()["exp_date"])
            print("์ถ๋ก  ๊ฒฐ๊ณผ :", inference, inference.text)

            # ํ๋ฉด์ ํ์ํ  ์ ๋ณด
            st.write(f'< ๋ฐ์ฝ๋๋ฒํธ : {barcode}>')
            st.write('์ํ์ ๋ณด : ์ํ')
            st.write(f'์ ํต๊ธฐํ : {exp_date}')
            st.write('-------')

            # ์ฌ์ดฌ์์ธ ๊ฒฝ์ฐ ์ฌํ์ต์ฉ DB ์๋ฒ๋ก ๋ณด๋
            if st.session_state.last != None:
                buffered_stream = image_file.image_to_buffer(captured_image)
                upload = {'file': buffered_stream}
                res = requests.post(url=PICTURE_URL, files=upload)
                print("์ฌ์ดฌ์ ์ด๋ฏธ์ง ์ ์ก ๊ฒฐ๊ณผ :", res, res.text)
            
                st.session_state.last = buffered_stream # ๋ค์ ์ดฌ์ ์ ๋ณด๋ด๊ธฐ ์ํด ์ ์ฅ
                image_file.drop_image(buffered_stream) # ์ด๋ฏธ์ง ํ์ผ ์ญ์ 
            
            else:
                st.session_state.last = buffered_stream

            # ์์ธก๋ ์ ํต๊ธฐํ์ ๊ทธ๋๋ก ์ฌ์ฉํ ์ง(ํ์ธ), ์์ ํ์ฌ ์ฌ์ฉํ ์ง(์ง์ ์๋ ฅ) ์ ํ
            check_info = st.radio(label = '์ ํต๊ธฐํ ์ ๋ณด๋ฅผ ํ์ธํด์ฃผ์ธ์', options = ['ํ์ธ', '์ง์ ์๋ ฅ'])
            
            # ํ์ธ
            if check_info == 'ํ์ธ':
                count = st.number_input('์๋์ ์๋ ฅํด์ฃผ์ธ์', 0, 1000)
                
                if st.button('QR ์์ฑ'):
                    exp_date_num = re.sub(r'[^0-9]', '', str(exp_date))   
                    img = qrcode.make(f"{barcode}{exp_date_num}")
                    img.save(f"./qr_code/{barcode}{exp_date_num}.jpg")
                    st.image(f"./qr_code/{barcode}{exp_date_num}.jpg")


                if st.button('๋ฑ๋ก'):
                    ls_dt = datetime.now()
                    ls_dt = ls_dt.strftime('%Y/%m/%d')

                    ls_cd = datetime.today().strftime("%Y%m%d%H%M%S%f")

                    data = {
                        'ls_cd': ls_cd,
                        'ls_dt': ls_dt,
                        'barcode': barcode,
                        'ex_dt': str(exp_date),
                        'ls_ct': count
                        }

                    res = requests.post(url=STOCK, json=data)
                    print("์๊ณ  DB ์ ์ก ๊ฒฐ๊ณผ :", res, res.text)
                    st.success(f' < ๋ฐ์ฝ๋๋ฒํธ : {barcode} / {count} ๊ฐ > ๋ฑ๋ก๋์์ต๋๋ค ')
                    #pyautogui.press("f5", presses=1, interval=0.2)

            # ์ง์  ์๋ ฅ
            else :
                ex1, co2 = st.columns(2)
                with ex1 :
                    exp_date = st.date_input('์ ํต๊ธฐํ์ ์๋ ฅํด์ฃผ์ธ์.')
                    exp_date = str(exp_date).replace('-', '/')
                with co2 :
                    count = st.number_input('์๋์ ์๋ ฅํด์ฃผ์ธ์', 0, 1000)
                    
                if st.button('QR ์์ฑ'):
                    exp_date_num = re.sub(r'[^0-9]', '', str(exp_date))   
                    img = qrcode.make(f"{barcode}{exp_date_num}")
                    img.save(f"./pages/qr_code/{barcode}{exp_date_num}.jpg")
                    st.image(f"./pages/qr_code/{barcode}{exp_date_num}.jpg")

                if st.button('๋ฑ๋ก'):
                    ls_dt = datetime.now()
                    ls_dt = ls_dt.strftime('%Y/%m/%d')

                    ls_cd = datetime.today().strftime("%Y%m%d%H%M%S%f")

                    data = {
                        'ls_cd': ls_cd,
                        'ls_dt': ls_dt,
                        'barcode': barcode,
                        'ex_dt': str(exp_date),
                        'ls_ct': count
                        }

                    res = requests.post(url=STOCK, json=data)
                    print("์๊ณ  DB ์ ์ก ๊ฒฐ๊ณผ :", res, res.text)
                    st.success(f' < ๋ฐ์ฝ๋๋ฒํธ : {barcode} / {count} ๊ฐ > ๋ฑ๋ก๋์์ต๋๋ค ')
                    # pyautogui.press("f5", presses=1, interval=0.2)