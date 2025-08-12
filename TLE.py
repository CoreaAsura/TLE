import streamlit as st
import requests
from datetime import datetime, timedelta

# 로그인 정보
USERNAME = st.secrets["username"]
PASSWORD = st.secrets["password"]

# 날짜 필터: 지난 15일
today = datetime.utcnow().date()
start_date = today - timedelta(days=15)
end_date = today - timedelta(days=1)
start_date_str = start_date.isoformat()
end_date_str = end_date.isoformat()

# Space-Track API URL
LOGIN_URL = "https://www.space-track.org/ajaxauth/login"
TLE_JSON_URL = (
    f"https://www.space-track.org/basicspacedata/query/class/gp/"
    f"epoch>%3D{start_date_str},epoch<%3D{end_date_str}/orderby/NORAD_CAT_ID asc/format/json"
)

st.set_page_config(page_title="TLE Downloader", layout="centered")
st.title("🌌 지난 15일 TLE 다운로드 (위성 이름 포함)")

if st.button("📡 TLE 가져오기"):
    session = requests.Session()
    login_response = session.post(LOGIN_URL, data={"identity": USERNAME, "password": PASSWORD})

    if login_response.status_code == 200:
        try:
            tle_response = session.get(TLE_JSON_URL)
            tle_response.raise_for_status()

            if "application/json" in tle_response.headers.get("Content-Type", ""):
                tle_data = tle_response.json()

                if not tle_data:
                    st.warning("🚫 지난 15일간 TLE 데이터가 없습니다.")
                else:
                    formatted_tle = ""
                    for sat in tle_data:
                        name = sat.get("OBJECT_NAME", "Unknown Satellite").strip()
                        line1 = sat.get("TLE_LINE1", "").strip()
                        line2 = sat.get("TLE_LINE2", "").strip()

                        if line1.startswith("1 ") and line2.startswith("2 "):
                            formatted_tle += f"{name}\n{line1}\n{line2}\n"

                    st.success(f"✅ TLE 데이터 {len(tle_data)}개 가져오기 성공!")
                    st.download_button(
                        label="📥 Download TLE as TXT",
                        data=formatted_tle,
                        file_name="named_tle_last15days.txt",
                        mime="text/plain"
                    )
            else:
                st.error("❌ 응답이 JSON 형식이 아닙니다. 로그인 세션이 유지되지 않았을 수 있습니다.")
        except requests.exceptions.RequestException as e:
            st.error(f"❌ TLE 요청 중 오류 발생: {e}")
    else:
        st.error("❌ 로그인 실패. 사용자 정보 또는 서버 상태를 확인하세요.")
