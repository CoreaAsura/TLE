import requests

# Celestrak active 그룹 TLE URL
url = "https://celestrak.org/NORAD/elements/active.txt"

# 요청 보내기
response = requests.get(url)

# 응답 확인 및 저장
if response.status_code == 200:
    with open("active_tle.txt", "w") as file:
        file.write(response.text)
    print("TLE 데이터가 'active_tle.txt'로 저장되었습니다.")
else:
    print(f"데이터를 가져오지 못했습니다. 상태 코드: {response.status_code}")
