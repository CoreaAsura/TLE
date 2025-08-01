import streamlit as st
import requests

st.title("CelesTrak TLE 통합 도구")

# 그룹 입력 받기
default_groups = ['active', 'weather', 'resource', 'cubesat']
groups_input = st.text_input("TLE 그룹 리스트 (쉼표로 구분)", ','.join(default_groups))
groups = [g.strip() for g in groups_input.split(',') if g.strip()]

if st.button("TLE 다운로드 및 저장"):
    url_template = 'https://celestrak.org/NORAD/elements/gp.php?GROUP={group}&FORMAT=tle'
    tle_data = ""
    for group in groups:
        url = url_template.format(group=group)
        response = requests.get(url)
        if response.status_code == 200:
            lines = response.text.strip().split('\n')
            for i in range(0, len(lines), 3):
                try:
                    tle_data += lines[i].strip() + '\n'
                    tle_data += lines[i+1].strip() + '\n'
                    tle_data += lines[i+2].strip() + '\n'
                except IndexError:
                    continue
        else:
            st.warning(f"❌ 그룹 {group} 요청 실패")

    # 결과 표시 및 다운로드 제공
    st.success(f"{len(tle_data.splitlines())//3}개 위성의 TLE 저장 완료")
    st.download_button("TLE 파일 다운로드", tle_data, file_name="celestrak_tle.txt")
