import streamlit as st
import requests

st.set_page_config(page_title="ETH Zurich 전체 TLE 가져오기", layout="wide")
st.title("🌐 ETH Zurich Satellite Database - 전체 TLE 수집기")

# TLE 가져오기 함수
def fetch_all_tle():
    url = "https://satdb.ethz.ch/api/satellitedata"
    params = {
        "start-datetime": "20000101T0000",  # 아주 오래전부터 시작
        "end-datetime": "20300101T0000",    # 미래까지 포함
        "without-frequency-data": True
    }

    all_tle = []
    try:
        response = requests.get(url, params=params)
        data = response.json()
        all_tle.extend(data["results"])
        next_url = data["next"]

        # 페이지네이션 처리
        while next_url:
            response = requests.get(next_url)
            data = response.json()
            all_tle.extend(data["results"])
            next_url = data["next"]

        return None, all_tle

    except Exception as e:
        return f"오류 발생: {e}", None

# 실행 버튼
if st.button("전체 TLE 가져오기"):
    with st.spinner("TLE 데이터를 수집 중입니다..."):
        error, tle_list = fetch_all_tle()
        if error:
            st.error(error)
        else:
            st.success(f"{len(tle_list)}개의 TLE 데이터를 가져왔습니다.")
            for item in tle_list:
                name = item["satellite"]
                tle = item["norad_str"]
                with st.expander(name):
                    st.code(tle, language="text")
