import streamlit as st
import requests

st.set_page_config(page_title="CelesTrak TLE Downloader", page_icon="🛰️")
st.title("🛰️ CelesTrak Active TLE 다운로드")

st.markdown("""
이 앱은 [CelesTrak](https://celestrak.org)에서 제공하는 Active TLE 데이터를 실시간으로 가져와 `.txt` 파일로 다운로드할 수 있도록 합니다.
""")

url = "https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=tle"

# 충분한 시간 여유를 두고 요청
try:
    with st.spinner("🔄 데이터를 가져오는 중입니다. 잠시만 기다려주세요..."):
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        tle_data = response.text

    st.success("✅ 데이터 가져오기 완료!")
    st.download_button(
        label="📥 TLE 데이터 다운로드",
        data=tle_data,
        file_name="active_tle.txt",
        mime="text/plain"
    )
except requests.exceptions.Timeout:
    st.error("⏱️ 요청 시간이 초과되었습니다. CelesTrak 서버가 느리거나 연결이 제한되었을 수 있습니다.")
except requests.exceptions.RequestException as e:
    st.error(f"🚫 데이터를 가져오는 데 실패했습니다: {e}")
