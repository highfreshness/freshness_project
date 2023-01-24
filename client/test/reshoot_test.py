import streamlit as st
from webcam import webcam # streamlit-webcam-example
import pyautogui
import requests
from func import ImageFile


if 'count' not in st.session_state:
    st.session_state.count = 0

if 'last' not in st.session_state:
    st.session_state.last = None


barcode = st.text_input("빈 칸에 바코드를 입력해주세요.")
# print(st.session_state.count)

if len(barcode) == 13:
    image_file = ImageFile()
    captured_image = st.camera_input("카메라")

    if captured_image != None:
        st.session_state.count += 1 # last 있으면 이 부분 없어도 될 듯?
        st.image(captured_image)

        if st.session_state.last == None: # 이전에 촬영된 이미지가 있는 경우 (첫 번째 촬영인 경우)
            print(f"{st.session_state.count}번째 촬영된 이미지 정보는 {captured_image} 입니다.")
        
        else: # 이전에 촬영된 이미지가 있는 경우
            buffered_stream = image_file.image_to_buffer(captured_image)
            upload = {'file': buffered_stream}
            
            # print(f"{st.session_state.count}번째 촬영된 이미지 정보는 {captured_image} 입니다.")
            # print(f"{st.session_state.count-1}번째에 촬영된 이미지 정보인 {st.session_state.last}가 전송됩니다.")
            res = requests.post(url="http://127.0.0.1:8000/test", files=upload)
            print(res)


            image_file.drop_image(buffered_stream)

        
        st.session_state.last = captured_image


if st.button('등록'):
    pyautogui.press("f5", presses=1, interval=0.2)