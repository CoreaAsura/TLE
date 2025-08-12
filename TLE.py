import streamlit as st
import requests

# 로그인 정보는 secrets.toml에서 불러옴
USERNAME = st.secrets["username"]
PASSWORD = st.secrets["password"]

st.set_page_config(page_title="TLE Downloader", layout="centered")
st.title("🌌 최신 TLE 전체 다운로드")

if st.button("📡 최신 TLE 가져오기"):
    with requests.Session() as session:
        login_url = "https://www.space-track.org/ajaxauth/login"
        tle_url = "https://www.space-track.org/basicspacedata/query/class/gp/orderby/NORAD_CAT_ID asc/format/tle"

        login_response = session.post(login_url, data={"identity": USERNAME, "password": PASSWORD})

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
            st.error("❌ 로그인 실패. 로그인 정보가 올바른지 확인하세요.")
