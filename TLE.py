import streamlit as st
import requests

# 페이지 설정
st.set_page_config(page_title="CelesTrak LEO TLE Downloader", page_icon="🛰️")
st.title("🛰️ CelesTrak LEO TLE 다운로드")

# 설명 텍스트
st.markdown("""
이 앱은 [CelesTrak](https://celestrak.org)에서 제공하는 **LEO (Low Earth Orbit)** TLE 데이터를 실시간으로 가져와 `.txt` 파일로 다운로드할 수 있도록 합니다.

> ⚠️ LEO 그룹에는 활성 위성뿐만 아니라 비활성 위성 및 우주쓰레기도 포함될 수 있습니다.
""")

# TLE 데이터 URL (LEO 기준)
leo_url = "https://celestrak.org/NORAD/elements/gp.php?GROUP=leo&FORMAT=tle"

# 버튼 클릭 시 동작
if st.button("🔄 LEO TLE 데이터 가져오기"):
    try:
        with st.spinner("LEO TLE 데이터를 가져오는 중입니다. 잠시만 기다려주세요..."):
            response = requests.get(leo_url, timeout=10)
            response.raise_for_status()
            tle_data = response.text

        st.success("✅ LEO TLE 데이터 가져오기 완료!")
        st.download_button(
            label="📥 LEO TLE 데이터 다운로드",
            data=tle_data,
            file_name="leo_tle.txt",
            mime="text/plain"
        )
    except requests.exceptions.Timeout:
        st.error("⏱️ 서버 응답 시간이 초과되었습니다. 나중에 다시 시도해주세요.")
    except requests.exceptions.ConnectionError:
        st.error("🌐 서버에 연결할 수 없습니다. 인터넷 연결을 확인해주세요.")
    except requests.exceptions.HTTPError as e:
        st.error(f"📡 서버 오류 발생: {e.response.status_code}")
    except requests.exceptions.RequestException as e:
        st.error(f"🚫 데이터를 가져오는 데 실패했습니다: {e}")
