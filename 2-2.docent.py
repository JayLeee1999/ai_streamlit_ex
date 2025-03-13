# # st, openai (gpt 사용할때 사용), dotenv (env 파일에 저장된 변수 가져오기)
# # os (폴더,파일 다루거나, 환경변수 불러오거나 시스템 정보가져오는 기능 등)
# from openai import OpenAI
# import streamlit as st
# from dotenv import load_dotenv
# import os

# # .env 파일 경로 지정 / override=True 덮어쓰기 허용
# load_dotenv(override=True)

# # Open AI API 키 설정하기 / os에서 api key를 가져옴 (단순 환경변수)
# api_key = os.getenv('OPENAI_API_KEY')

# # OpenAI 객체 생성 / openai 접속 허가증
# client = OpenAI(api_key = api_key)

# # 주어진 이미지 주소로부터 GPT4V의 설명을 얻는 함수.
# def ai_describe(image_url):   # 함수 정의 순서는 상관 없지만.. 보통 모듈설정 다음 함수 정의 함


# lib 설치 ###########
# pip install openai
# pip install streamlit
# pip install python-dotenv
# 실행 ###############
# streamlit run 2-2.docent_img_url.py
######################

from openai import OpenAI
import streamlit as st
from dotenv import load_dotenv
import os
import base64
from io import BytesIO
from PIL import Image  # PIL 라이브러리 필요


# .env 파일 경로 지정 
load_dotenv(override=True)

# Open AI API 키 설정하기
api_key = os.getenv('OPENAI_API_KEY')

# OpenAI 객체 생성
client = OpenAI(api_key = api_key)

# 주어진 이미지 주소로부터 GPT4V의 설명을 얻는 함수.
def ai_describe(image_url):
    response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
        "role": "user",
        "content": [
            {"type": "text", "text": "이 이미지에 대해서 자세하게 설명해 주세요."},
            {"type": "image_url",
                "image_url": {"url": image_url,},
            },
        ],
        }
    ],
    max_tokens=1024,
    )
    result = response.choices[0].message.content
    print("결과 >> ", result)
    return result

# 웹 사이트 상단에 노출될 웹 사이트 제목.
st.title("AI 도슨트: 이미지를 설명해드려요!")


import streamlit as st

tab1, tab2 = st.tabs(["Cat", "Dog"])

with tab1:

    # st.text_area()는 사용자의 입력을 받는 커다란 텍스트 칸을 만든다. height는 이 텍스트 칸의 높이.
    input_url = st.text_area("여기에 이미지 주소를 입력하세요", height=70)

    # st.button()을 클릭하는 순간 st.button()의 값은 True가 되면서 if문 실행
    if st.button("해설"):

        # st.text_area()의 값이 존재하면 input_url의 값이 True가 되면서 if문 실행
        if input_url:
            try:
                # st.image()는 기본적으로 이미지 주소로부터 이미지를 웹 사이트 화면에 생성됨
                st.image(input_url, width=300)
                
                # describe() 함수는 GPT4V의 출력 결과를 반환함
                result = ai_describe(input_url)

                # st.success()는 텍스트를 웹 사이트 화면에 출력하되, 초록색 배경에 출력
                st.success(result)
            except:
                st.error("요청 오류가 발생했습니다!")
        else:
            st.warning("텍스트를 입력하세요!") # 화면 상으로 노란색 배경으로 출력


with tab2:

    # 이미지를 Base64로 변환하는 함수
    # Base64 인코딩은 바이너리 데이터를 ASCII 문자열로 변환하는 표준 방식
    def encode_image(image):
        buffered = BytesIO()
        image.save(buffered, format="PNG")  # PNG 형식으로 변환
        return base64.b64encode(buffered.getvalue()).decode("utf-8")

    # 이미지 파일을 분석하여 설명을 반환하는 함수
    def ai_describe(image):
        try:
            base64_image = encode_image(image)  # 이미지를 Base64로 변환
            
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "이 이미지에 대해서 자세하게 설명해 주세요."},
                            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}},
                        ],
                    }
                ],
                max_tokens=1024,
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"오류 발생: {str(e)}"


    # 파일 업로드 위젯
    uploaded_file = st.file_uploader("이미지를 업로드하세요", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # 업로드된 이미지 표시
        st.image(uploaded_file, width=300)
        
        # 이미지 설명 요청 버튼
        if st.button("해설"):
            image = Image.open(uploaded_file)  # PIL 이미지 열기
            
            # GPT-4V를 이용한 이미지 분석 수행
            result = ai_describe(image)
            st.success(result)
