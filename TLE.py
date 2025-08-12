import streamlit as st
import requests

st.set_page_config(page_title="Space-Track TLE Downloader", layout="centered")
st.title("🌌 Space-Track TLE Downloader")

st.markdown("이 앱은 Space-Track 로그인 정보를 이용해 전체 TLE 데이터를 다운로드합니다.")

username = st.text_input("👤 Space-Track Username")
password = st.text_input("🔒 Space-Track Password", type="password")

if st.button("📡 Fetch TLE Data"):
    with requests.Session() as session:
        login_url = "https://www.space-track.org/ajaxauth/login"
        tle_url = "https://www.space-track.org/basicspacedata/query/class/gp/orderby/NORAD_CAT_ID asc/format/tle"

        login_response = session.post(login_url, data={"identity": username, "password": password})

        if login_response.status_code == 200 and "cookie" in session.cookies.get_dict():
            tle_response = session.get(tle_url)
            if tle_response.status_code == 200:
                st.success("✅ TLE 데이터 가져오기 성공!")
                st.download_button(
                    label="📥 Download TLE as TXT",
                    data=tle_response.text,
                    file_name="tle_data.txt",
                    mime="text/plain"
                )
            else:
                st.error("❌ TLE 데이터를 가져오지 못했습니다.")
        else:
            st.error("❌ 로그인 실패. 아이디/비밀번호를 확인해주세요.")
