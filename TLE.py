import streamlit as st
import requests

st.set_page_config(page_title="☄️ TLE 통합 도구", layout="centered")
st.title("☄️ CelesTrak 전체 TLE 통합 웹앱")
st.markdown("CelesTrak에서 대표적인 TLE 그룹을 병합하여 하나의 파일로 저장하고 다운로드할 수 있습니다.")

# Streamlit Cloud에서는 현재 디렉터리 기준으로 저장
output_file = "TLE.txt"

# 대표 그룹 리스트 직접 지정
group_list = [
    "active", "amateur", "cubesat", "engineering", "geostationary",
    "science", "station", "weather"
]

if st.button("🛰️ 전체 TLE 다운로드 시작"):
    count = 0
    with open(output_file, "w", encoding="utf-8") as f:
        for group in group_list:
            tle_url = f"https://celestrak.org/NORAD/elements/gp.php?GROUP={group}&FORMAT=tle"
            try:
                r = requests.get(tle_url, timeout=10)
                if r.status_code == 200:
                    lines = r.text.strip().split("\n")
                    for i in range(0, len(lines), 3):
                        try:
                            f.write(lines[i].strip() + "\n")
                            f.write(lines[i+1].strip() + "\n")
                            f.write(lines[i+2].strip() + "\n")
                            count += 1
                        except IndexError:
                            continue
                else:
                    st.warning(f"⚠️ 그룹 '{group}' 요청 실패 (HTTP {r.status_code})")
            except Exception as e:
                st.warning(f"⚠️ 그룹 '{group}' 오류 발생: {e}")

    st.success(f"✅ 총 {count}개의 위성 TLE를 '{output_file}'에 저장했습니다.")
    st.download_button("📥 TLE.txt 파일 다운로드", data=open(output_file, "rb").read(), file_name="TLE.txt")
