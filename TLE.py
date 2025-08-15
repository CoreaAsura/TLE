import requests
from bs4 import BeautifulSoup

url = "https://tle.info/"
response = requests.get(url)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")
pre_tags = soup.find_all("pre")  # TLE 데이터는 <pre> 태그 안에 있음

output_file = "tle_info_data.txt"

with open(output_file, "w") as f:
    for pre in pre_tags:
        lines = pre.text.strip().split("\n")
        for i in range(0, len(lines), 3):
            if i + 2 < len(lines):
                name = lines[i].strip()
                line1 = lines[i + 1].strip()
                line2 = lines[i + 2].strip()
                f.write(f"{name}\n{line1}\n{line2}\n")
