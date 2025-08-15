import streamlit as st
import requests

st.set_page_config(page_title="ETH Zurich TLE 조회기", layout="wide")
st.title("🛰️ ETH Zurich Satellite Database 기반 TLE 조회")

# 사용자 입력
norad_id = st.text_input("NORAD ID 입력", value="25544")  # 예: ISS
start_date = st.date_input("시작 날짜", value=None)
end_date = st.date_input("종료 날짜", value=None)
before_days = st.slider("시작 이전 일수 포함", 0, 10, 3)
after_days = st.slider("종료 이후 일수 포함", 0, 10, 3)

# 날짜 포맷 변환
def format_date(dt):
    return dt.strftime("%Y%m%dT0000")

# TLE 가져오기 함수
def fetch_tle(norad_id, start, end, before, after):
    url = "https://satdb.ethz.ch/api/satellitedata"
    params = {
        "norad-id": int(norad_id),
        "start-datetime": format_date(start),
        "end-datetime": format_date(end),
        "before": before,
        "after": after,
        "without-frequency-data": True
    }

    tle_list = []
    try:
        response = requests.get(url, params=params)
        data = response.json()
        tle_list.extend(data["results"])
        next_url = data["next"]

        # 페이지네이션 처리
        while next_url:
            response = requests.get(next_url)
            data = response.json()
            tle_list.extend(data["results"])
            next_url = data["next"]

        return None, tle_list

    except Exception as e:
        return f"오류 발생: {e}", None

# 실행 버튼
if st.button("TLE 조회"):
    if not start_date or not end_date:
        st.warning("시작 날짜와 종료 날짜를 모두 선택해주세요.")
    else:
        error, results = fetch_tle(norad_id, start_date, end_date, before_days, after_days)
        if error:
            st.error(error)
        else:
            st.success(f"{len(results)}개의 TLE 데이터를 가져왔습니다.")
            for item in results:
                name = item["satellite"]
                tle = item["norad_str"]
                with st.expander(name):
                    st.code(tle, language="text")
