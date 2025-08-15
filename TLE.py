import requests

# 주요 TLE 그룹 URL 목록
urls = [
    "https://celestrak.org/NORAD/elements/active.txt",
    "https://celestrak.org/NORAD/elements/starlink.txt",
    "https://celestrak.org/NORAD/elements/gps-ops.txt",
    "https://celestrak.org/NORAD/elements/weather.txt",
    "https://celestrak.org/NORAD/elements/iridium.txt",
    "https://celestrak.org/NORAD/elements/geo.txt",
    "https://celestrak.org/NORAD/elements/science.txt",
    "https://celestrak.org/NORAD/elements/resource.txt"
]

output_file = "celestrak_all_tle.txt"

with open(output_file, "w") as f:
    for url in urls:
        response = requests.get(url)
        response.raise_for_status()
        lines = response.text.strip().split("\n")

        # TLE는 3줄씩 구성됨: name, line1, line2
        for i in range(0, len(lines), 3):
            if i + 2 < len(lines):
                name = lines[i].strip()
                line1 = lines[i + 1].strip()
                line2 = lines[i + 2].strip()
                f.write(f"{name}\n{line1}\n{line2}\n")
