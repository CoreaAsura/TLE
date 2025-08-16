import requests

# 새로운 API URL
url = "https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=tle"

try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()  # 오류 발생 시 예외 처리
    with open("active_tle.txt", "w", encoding="utf-8") as file:
        file.write(response.text)
    print("✅ TLE 데이터가 'active_tle.txt'로 저장되었습니다.")
except requests.exceptions.Timeout:
    print("⏱️ 요청 시간이 초과되었습니다. 서버 상태를 확인하세요.")
except requests.exceptions.RequestException as e:
    print(f"❌ 요청 중 오류 발생: {e}")
