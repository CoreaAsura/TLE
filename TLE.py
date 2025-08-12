import streamlit as st
import requests

st.title("🔐 Space-Track 로그인 테스트 (세션 기반)")

username = st.secrets["username"]
password = st.secrets["password"]

LOGIN_URL = "https://www.space-track.org/ajaxauth/login"
TLE_URL = "https://www.space-track.org/basicspacedata/query/class/gp/orderby/NORAD_CAT_ID asc/format/tle"

session = requests.Session()
login_response = session.post(LOGIN_URL, data={"identity": username, "password": password})

# 세션 쿠키 확인
cookies = session.cookies.get_dict()
st.subheader("🍪 세션 쿠키 상태")
st.write(cookies)

if "cookie" in cookies or len(cookies) > 0:
    st.success("✅ 로그인 성공! 세션 쿠키가 설정되었습니다.")
    
    # TLE 요청 테스트
    tle_response = session.get(TLE_URL)
    if tle_response.status_code == 200 and tle_response.text.strip():
        st.success("📡 TLE 데이터 요청 성공!")
        st.download_button(
            label="📥 Download TLE as TXT",
            data=tle_response.text,
            file_name="tle_data.txt",
            mime="text/plain"
        )
    else:
        st.error("❌ TLE 데이터를 가져오지 못했습니다.")
else:
    st.error("❌ 로그인 실패. 세션 쿠키가 설정되지 않았습니다.")
