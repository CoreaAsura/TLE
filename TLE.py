import requests

# ETH Zurich TLE API endpoint
url = "https://satdb.ethz.ch/api/tle/latest"

# 요청 보내기
response = requests.get(url)
response.raise_for_status()
data = response.json()

# TXT 파일로 저장
with open("latest_tle.txt", "w") as f:
    for sat in data:
        name = sat.get("name", "UNKNOWN")
        line1 = sat.get("line1", "")
        line2 = sat.get("line2", "")
        f.write(f"{name}\n{line1}\n{line2}\n")
