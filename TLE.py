import requests
import zipfile
import io

# 1. ZIP 파일 다운로드
zip_url = "https://celestrak.org/NORAD/elements/gpzips/current.zip"
response = requests.get(zip_url)
zip_data = zipfile.ZipFile(io.BytesIO(response.content))

# 2. 모든 TLE 파일 파싱
all_tles = []

for file_name in zip_data.namelist():
    if file_name.endswith(".txt"):
        with zip_data.open(file_name) as f:
            lines = f.read().decode("utf-8").strip().splitlines()
            for i in range(0, len(lines), 3):
                if i + 2 < len(lines):
                    tle = f"{lines[i]}\n{lines[i+1]}\n{lines[i+2]}"
                    all_tles.append(tle)

# 3. 저장
with open("all_tles.txt", "w") as f:
    f.write("\n".join(all_tles))

print(f"✅ 총 {len(all_tles)}개의 TLE가 저장되었습니다.")
