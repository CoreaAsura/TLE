import requests
import os

# 📁 저장 경로 설정
output_dir = r"C:\tip"
output_file = os.path.join(output_dir, "TLE_All.txt")
os.makedirs(output_dir, exist_ok=True)

# 🔍 전체 그룹 리스트 가져오기
group_list_url = "https://celestrak.org/NORAD/elements/groups.json"
try:
    resp = requests.get(group_list_url, timeout=10)
    groups = [item['GROUP'] for item in resp.json()]
except Exception as e:
    print(f"❌ 그룹 리스트 로딩 실패: {e}")
    groups = []  # 에러 시 빈 리스트로 진행

# 🛰️ 그룹별 TLE 수집 및 병합
with open(output_file, "w", encoding="utf-8") as f:
    for group in groups:
        tle_url = f"https://celestrak.org/NORAD/elements/gp.php?GROUP={group}&FORMAT=tle"
        try:
            response = requests.get(tle_url, timeout=10)
            if response.status_code == 200:
                lines = response.text.strip().split("\n")
                for i in range(0, len(lines), 3):
                    try:
                        f.write(lines[i].strip() + "\n")     # 이름
                        f.write(lines[i+1].strip() + "\n")   # TLE Line 1
                        f.write(lines[i+2].strip() + "\n")   # TLE Line 2
                    except:
                        continue
            else:
                print(f"⚠️ {group} 그룹 요청 실패: HTTP {response.status_code}")
        except Exception as e:
            print(f"⚠️ {group} 그룹 다운로드 오류: {e}")

print(f"✅ 모든 그룹 TLE를 '{output_file}' 에 저장 완료했습니다.")
