import streamlit as st





# 1. 사용자에게 보여지는 부분 구현
# - 타이틀
st.title("이미지 표시")
st.title("내가만든 그림은 :blue[cool] :sunglasses:")
# - 이미지표시
st.image("images/robot.jpg", caption="Cute Robot")
# - 설명 텍스트 출력
st.write("Hello, *World!* :sunglasses:")
st.write("원하는 그림을 tell me :sunglasses:")
# - textarea: 영어로 그림 그리기 설명 프롬프트 입력
txt = st.text_area(
    "Text to analyze",
)
# - 버튼: 그림을 요청하기 gpt 에게
st.button("Reset", type="primary")
if st.button("Say hello"):
    st.write("Why hello there")
else:
    st.write("Goodbye")

if st.button("Aloha", type="tertiary"):
    st.write("Ciao")