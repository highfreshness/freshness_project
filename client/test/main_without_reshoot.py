import streamlit as st
from webcam import webcam
import pyautogui
import requests
from PIL import Image
from post_processing import text_postprocessing
from func import ImageFile

st.markdown("<h1 style='text-align: center; color: blue;'>선 도 관 리</h1>", unsafe_allow_html=True)
option = st.selectbox("진행할 작업을 선택해주세요.", ("입고처리", "출고처리", "재고조회"))


if option == "입고처리":
    barcode = st.text_input("빈 칸에 바코드를 입력해주세요.")
    pyautogui.press("tab", presses=1, interval=0.2)
    st.header("")

    if len(barcode) == 13:
        # Create Radio Buttons
        check_cam = st.radio(label = '내장카메라 / 웹캠 여부를 선택하세요!!', options = ['Maincam', "Webcam"])
        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
        
        image_file = ImageFile()

        if check_cam == 'Maincam': # 내장 캠인 경우
            captured_image = st.camera_input("카메라") # type : streamlit.runtime.uploaded_file_manager.UploadedFile
            
            if captured_image is None:
                st.write("Waiting for capture...")
            else:
                st.image(captured_image)
                buffered_stream = image_file.image_to_buffer(captured_image)
                upload = {'file': buffered_stream}

                res = requests.post(url="http://127.0.0.1:8000/exp_date", files=upload)
                image_file.drop_image(buffered_stream)
                
        else: # 외장 캠인 경우
            captured_image = webcam("카메라")  # type : PIL.Image.Image
            
            if captured_image is None:
                st.write("Waiting for capture...")
            else:
                st.image(captured_image)
                buffered_stream = image_file.image_to_buffer(captured_image)
                upload = {'file': buffered_stream}

                res = requests.post(url="http://127.0.0.1:8000/exp_date", files=upload)
                image_file.drop_image(buffered_stream)

        # result = text_postprocessing(res)
        # print(result)