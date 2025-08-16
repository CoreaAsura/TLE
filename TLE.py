import requests

def fetch_all_tle():
    url = "https://satdb.ethz.ch/api/satellitedata"
    params = {
        "start-datetime": "20000101T0000",
        "end-datetime": "20300101T0000",
        "without-frequency-data": True
    }

    all_tle = []
    try:
        response = requests.get(url, params=params)
        data = response.json()
        all_tle.extend(data["results"])
        next_url = data["next"]

        while next_url:
            response = requests.get(next_url)
            data = response.json()
            all_tle.extend(data["results"])
            next_url = data["next"]

        return all_tle

    except Exception as e:
        print(f"오류 발생: {e}")
        return []

def save_tle_to_txt(tle_list, filename="tle_data.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        for item in tle_list:
            name = item["satellite"]
            tle = item["norad_str"]
            f.write(f"{name}\n{tle}\n\n")

if __name__ == "__main__":
    print("TLE 데이터를 가져오는 중...")
    tle_data = fetch_all_tle()
    print(f"{len(tle_data)}개의 TLE 데이터를 저장합니다...")
    save_tle_to_txt(tle_data)
    print("저장이 완료되었습니다: tle_data.txt")
