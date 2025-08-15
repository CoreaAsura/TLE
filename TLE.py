import requests

# Space-Track 로그인 정보
username = 'your_username'
password = 'your_password'

# 오늘 날짜 (UTC 기준)
start_date = '2025-08-15'
end_date = '2025-08-15'

# 요청 URL
url = f'https://www.space-track.org/basicspacedata/query/class/tle_latest/format/json/EPOCH>={start_date},EPOCH<={end_date}/orderby/NORAD_CAT_ID asc'

# 세션 생성 및 로그인
session = requests.Session()
login_url = 'https://www.space-track.org/ajaxauth/login'
login_data = {'identity': username, 'password': password}
session.post(login_url, data=login_data)

# 데이터 요청
response = session.get(url)

# 결과 출력
if response.status_code == 200:
    tle_data = response.json()
    print(f"총 {len(tle_data)}개의 TLE 데이터를 가져왔습니다.")
else:
    print(f"오류 발생: {response.status_code}")
