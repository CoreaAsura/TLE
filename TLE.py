import requests

session = requests.Session()

login_ok = session.post(LOGIN_URL, data={"identity": username, "password": password})
if login_ok.status_code == 200 and "Set-Cookie" in login_ok.headers:
    tle_response = session.get(TLE_JSON_QUERY)
    if "application/json" in tle_response.headers.get("Content-Type", ""):
        tle_data = tle_response.json()
        # TLE 처리 코드...
    else:
        st.error("응답이 JSON이 아닙니다. 로그인 세션이 유지되지 않았을 수 있습니다.")
else:
    st.error("로그인 실패. 사용자 정보 또는 서버 상태를 확인하세요.")
