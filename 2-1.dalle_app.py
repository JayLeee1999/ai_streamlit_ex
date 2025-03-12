import streamlit as st

# openai key 값 로딩, 환경변수 .env에 저장, git에 업로딩은 안되도록
from openai import OpenAI
from dotenv import load_dotenv
import base64
import io
from PIL import Image
import os
# .env 파일의 환경변수를 메모리에 로딩
load_dotenv(override = True)
openai_key = os.environ.get('openai_api_key')
client = OpenAI(api_key=openai_key)
# openai에 이미지 생성 요청 함수 정의
# return 값이 생성 url
def get_image(user_prompt):
    response = client.images.generate(
            model='dall-e-3',
            prompt= user_prompt,
            size = '1024x1024',
            quality='standard',
            response_format='b64_json',
            n=1,
        )
    response = response.data[0].b64_json # DALLE로부터 Base64 형태의 이미지를 얻음.
    image_data = base64.b64decode(response) # Base64로 쓰여진 데이터를 이미지 형태로 변환
    image = Image.open(io.BytesIO(image_data)) # '파일처럼' 만들어진 이미지 데이터를 컴퓨터에서 볼 수 있도록 Open
    return image

    # image_url = response.data[0].url
    # # print(image_url)
    # return image_url
# openai key 값 프린트 해보기
# print(openai_key)



# openai key 값 프린트 해보기
# print(openai_key)
# 1. 사용자에게 보여지는 부분 구현
# - 타이틀
st.title("이미지 표시")
st.title("내가만든 그림은 :blue[cool] :sunglasses:")
# - 이미지표시
st.image("images/robot.jpg", caption="Cute Robot")

# - 설명 텍스트 출력
st.write("원하는 그림을 tell me :sunglasses:")

# - textarea: 영어로 그림 그리기 설명 프롬프트 입력
user_prompt = st.text_area("원하는 그림?", height=100)


# 버튼: 그림을 요청하기 gpt 에게
if st.button('painting'):
    # 텍스트 에리어 박스에 입력한 값을 받기 (user_prompt)
    print('user_prompt:', user_prompt)
    if user_prompt:
        # openAI에 그림 그리기 메시지를 보내기
        image = get_image(user_prompt)
        st.image(image, caption="Your paint!")
    else:
        st.write('텍스트 박스에 그리실 그림을 영어로 설명해주세요!')


