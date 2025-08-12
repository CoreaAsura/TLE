import streamlit as st
import requests

# 로그인 정보 (Streamlit Cloud의 Secrets 메뉴에서 설정)
USERNAME = st.secrets["username"]
PASSWORD = st.secrets["password"]

# Space-Track API URL
LOGIN_URL = "https://www.space-track.org/ajaxauth/login"
TLE_JSON_URL = "https://www.space-track.org/basicspacedata/query/class/gp/epoch>%3D2020-01-01/orderby/NORAD_CAT_ID asc/format/json"

st.set_page_config(page_title="TLE Downloader", layout="centered")
st.title("🌌 최신 TLE 전체 다운로드 (위성 이름 포함)")

if st.button("📡 최신 TLE 가져오기"):
    session = requests.Session()
    login_response = session.post(LOGIN_URL, data={"identity": USERNAME, "password": PASSWORD})

    if login_response.status_code == 200 and "Set-Cookie" in login_response.headers:
        tle_response = session.get(TLE_JSON_URL)

        # 응답이 JSON인지 확인
        if "application/json" in tle_response.headers.get("Content-Type", ""):
            try:
                tle_data = tle_response.json()
                formatted_tle = ""

                for sat in tle_data:
                    name = sat.get("OBJECT_NAME", "Unknown Satellite").strip()
                    line1 = sat.get("TLE_LINE1", "").strip()
                    line2 = sat.get("TLE_LINE2", "").strip()

                    if line1.startswith("1 ") and line2.startswith("2 "):
                        formatted_tle += f"{name}\n{line1}\n{line2}\n"

                st.success("✅ TLE 데이터 가져오기 성공!")
                st.download_button(
                    label="📥 Download TLE as TXT",
                    data=formatted_tle,
                    file_name="named_tle.txt",
                    mime="text/plain"
                )
            except Exception as e:
                st.error(f"❌ JSON 파싱 오류: {e}")
        else:
            st.error("❌ 응답이 JSON 형식이 아닙니다. 로그인 세션이 유지되지 않았을 수 있습니다.")
            st.text(tle_response.text)
    else:
        st.error("❌ 로그인 실패. 사용자 정보 또는 서버 상태를 확인하세요.")
