
from openai import OpenAI
import streamlit as st

# --- 비밀번호 확인 함수 ---
def check_password():
    """비밀번호가 맞으면 True를, 틀리면 False를 반환합니다."""
    if "password_correct" not in st.session_state:
        # 세션 상태에 비밀번호 정확성 여부가 없으면 초기화
        st.session_state["password_correct"] = False

    # st.secrets를 통해 저장된 비밀번호를 가져옵니다.
    # 이 부분은 Streamlit Community Cloud의 Secrets에 설정된 값을 사용합니다.
    correct_password = st.secrets["password"]

    if st.session_state["password_correct"]:
        return True

    # 폼을 사용하여 비밀번호 입력 필드와 버튼을 만듭니다.
    with st.form("password_form"):
        password = st.text_input("비밀번호를 입력하세요", type="password")
        submitted = st.form_submit_button("확인")

        if submitted:
            if password == correct_password:
                st.session_state["password_correct"] = True
                st.rerun()  # 비밀번호가 맞으면 앱을 새로고침하여 챗봇을 표시
            else:
                st.error("비밀번호가 틀렸습니다.")
    return False

# --- 메인 챗봇 로직 ---

# 비밀번호 확인 함수를 먼저 호출합니다.
if check_password():
    st.title("닷컴달콤 연수 챗봇")

    client = OpenAI() # OpenAI API 키는 st.secrets["OPENAI_API_KEY"] 등으로 설정하는 것이 좋습니다.

    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-4.1"

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
