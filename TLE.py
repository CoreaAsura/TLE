import streamlit as st
import requests

# 앱 제목
st.title("🛰 CelesTrak Active TLE 다운로드")

# 설명
st.markdown("""
이 앱은 [CelesTrak](https://celestrak.org)에서 제공하는 Active TLE 데이터를 가져와 `.txt` 파일로 다운로드할 수 있도록 합니다.
""")

# 다운로드 버튼
url = "https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=tle"
response = requests.get(url)

if response.status_code == 200:
    tle_data = response.text
    st.download_button(
        label="📥 TLE 데이터 다운로드",
        data=tle_data,
        file_name="active_tle.txt",
        mime="text/plain"
    )
else:
    st.error("데이터를 가져오는 데 실패했습니다. CelesTrak 서버 상태를 확인해주세요.")
