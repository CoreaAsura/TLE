import requests
import os

# 📂 저장 경로 및 파일명 설정
output_dir = r"C:\tip"
output_file = os.path.join(output_dir, "TLE.txt")

# 🔗 주요 TLE 그룹 리스트 (추가 가능)
groups = [
    "active", "weather", "resource", "cubesat", "iridium", "engineering", "geosynchronous", "visual",
    "science", "tdrss", "galileo", "beidou", "glonass"
]

# 📥 TLE 수집 및 저장
os.makedirs(output_dir, exist_ok=True)

with open(output_file, "w", encoding="utf-8") as f:
    for group in groups:
        url = f"https://celestrak.org/NORAD/elements/gp.php?GROUP={group}&FORMAT=tle"
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                lines = response.text.strip().split("\n")
                for i in range(0, len(lines), 3):
                    try:
                        f.write(lines[i].strip() + "\n")     # 위성 이름
                        f.write(lines[i+1].strip() + "\n")   # TLE Line 1
                        f.write(lines[i+2].strip() + "\n")   # TLE Line 2
                    except IndexError:
                        continue  # 누락된 TLE는 건너뜀
            else:
                print(f"❌ {group} 그룹 요청 실패 (HTTP {response.status_code})")
        except Exception as e:
            print(f"⚠️ {group} 그룹 다운로드 중 오류: {e}")

print(f"✅ 전체 TLE 데이터를 '{output_file}' 에 저장 완료했습니다.")
