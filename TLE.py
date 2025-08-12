import streamlit as st
import requests

st.title("🔐 Space-Track 로그인 테스트")

# 로그인 정보 가져오기
username = st.secrets["username"]
password = st.secrets["password"]

# 로그인 요청
LOGIN_URL = "https://www.space-track.org/ajaxauth/login"
credentials = {
    "identity": username,
    "password": password
}

session = requests.Session()
response = session.post(LOGIN_URL, data=credentials)

# 응답 상태 출력
st.subheader("📡 로그인 응답 상태")
st.write(f"Status Code: {response.status_code}")
st.write(response.text)

# 로그인 성공 여부 확인
if response.status_code == 200 and "authenticated" in response.text.lower():
    st.success("✅ 로그인 성공!")
else:
    st.error("❌ 로그인 실패. 로그인 정보를 다시 확인하세요.")
