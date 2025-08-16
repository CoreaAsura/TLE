import streamlit as st
import requests

def fetch_all_tle():
    url = "https://satdb.ethz.ch/api/satellitedata"
    params = {
        "start-datetime": "20000101T0000",
        "end-datetime": "20300101T0000",
        "without-frequency-data": True
    }

    all_tle = []
    try:
        response = requests.get(url, params=params)
        data = response.json()
        all_tle.extend(data["results"])
        next_url = data["next"]

        while next_url:
            response = requests.get(next_url)
            data = response.json()
            all_tle.extend(data["results"])
            next_url = data["next"]

        return all_tle

    except Exception as e:
        st.error(f"오류 발생: {e}")
        return []

def format_tle(tle_list):
    formatted = ""
    for item in tle_list:
        name = item["satellite"]
        tle = item["norad_str"]
        formatted += f"{name}\n{tle}\n"
    return formatted

st.set_page_config(page_title="전체 TLE 다운로드", layout="centered")
st.title("📡 ETH Zurich 전체 TLE 다운로드")

if st.button("TLE 가져오기"):
    with st.spinner("TLE 데이터를 수집 중입니다..."):
        tle_data = fetch_all_tle()
        if tle_data:
            formatted_text = format_tle(tle_data)
            st.success(f"{len(tle_data)}개의 TLE 데이터를 가져왔습니다.")
            st.download_button(
                label="📥 TLE 파일 다운로드",
                data=formatted_text,
                file_name="ethz_tle_all.txt",
                mime="text/plain"
            )
