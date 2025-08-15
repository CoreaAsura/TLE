import streamlit as st
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="TLE 정보 보기", layout="wide")
st.title("🌍 TLE 정보 실시간 확인")

# TLE 데이터 가져오기
def fetch_tle():
    try:
        url = "https://tle.info/"
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # TLE 테이블 찾기
        table = soup.find("table")
        if not table:
            return "TLE 테이블을 찾을 수 없습니다.", None

        rows = table.find_all("tr")[1:]  # 헤더 제외
        tle_data = []
        for row in rows:
            cols = row.find_all("td")
            if len(cols) >= 3:
                name = cols[0].text.strip()
                line1 = cols[1].text.strip()
                line2 = cols[2].text.strip()
                tle_data.append((name, line1, line2))
        return None, tle_data

    except Exception as e:
        return f"오류 발생: {e}", None

# 데이터 출력
error, tle_list = fetch_tle()
if error:
    st.error(error)
else:
    st.success(f"{len(tle_list)}개의 TLE 데이터를 가져왔습니다.")
    for name, line1, line2 in tle_list:
        with st.expander(name):
            st.code(f"{line1}\n{line2}", language="text")
