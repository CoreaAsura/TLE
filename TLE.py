import streamlit as st
import requests
import os

st.set_page_config(page_title="☄️ TLE 통합 도구", layout="centered")
st.title("☄️ CelesTrak 전체 TLE 통합 웹앱")
st.markdown("CelesTrak의 모든 TLE 그룹을 병합해 하나의 텍스트 파일로 저장합니다.")

# 저장 위치 (Streamlit Cloud에서는 현재 디렉터리 사용)
output_file = "TLE.txt"

# 버튼 실행
if st.button("🛰️ 전체 TLE 다운로드 시작"):
    group_url = "https://celestrak.org/NORAD/elements/groups.json"
    try:
        resp = requests.get(group_url, timeout=10)
        group_list = [g["GROUP"] for g in resp.json()]
    except Exception as e:
        st.error(f"❌ 그룹 리스트 가져오기 실패: {e}")
        group_list = []

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
                    st.warning(f"⚠️ {group} 그룹 요청 실패 (HTTP {r.status_code})")
            except Exception as e:
                st.warning(f"⚠️ {group} 그룹 오류: {e}")

    st.success(f"✅ {count}개 위성의 TLE를 '{output_file}'에 저장 완료했습니다.")
    st.download_button("📥 TLE.txt 파일 다운로드", data=open(output_file, "rb").read(), file_name="TLE.txt")
