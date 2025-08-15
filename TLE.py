import streamlit as st
import requests
from datetime import datetime

# 사용자 정보 입력
st.title("오늘의 TLE 데이터 조회")
username = st.text_input("Space-Track 사용자 이름")
password = st.text_input("Space-Track 비밀번호", type="password")

# 오늘 날짜 설정
today = datetime.utcnow().strftime("%Y-%m-%d")

# API 요청 함수
def fetch_tle_data(username, password, date):
    login_url = "https://www.space-track.org/ajaxauth/login"
    query_url = f"https://www.space-track.org/basicspacedata/query/class/tle_latest/format/json/EPOCH>={date},EPOCH<={date}/orderby/NORAD_CAT_ID asc"

    session = requests.Session()
    try:
        login_response = session.post(login_url, data={"identity": username, "password": password})
        login_response.raise_for_status()

        response = session.get(query_url)
        response.raise_for_status()

        return response.json()
    except Exception as e:
        st.error(f"오류 발생: {e}")
        return None

# 버튼 클릭 시 실행
if st.button("TLE 데이터 가져오기"):
    if username and password:
        st.info(f"{today} 날짜의 TLE 데이터를 조회 중입니다...")
        tle_data = fetch_tle_data(username, password, today)

        if tle_data:
            st.success(f"총 {len(tle_data)}개의 TLE 데이터를 가져왔습니다.")
            st.json(tle_data)
        else:
            st.warning("데이터를 가져오지 못했습니다. 날짜를 바꾸거나 나중에 다시 시도해보세요.")
    else:
        st.warning("사용자 이름과 비밀번호를 입력해주세요.")
