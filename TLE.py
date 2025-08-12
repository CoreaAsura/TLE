import streamlit as st
import requests

LOGIN_URL = "https://www.space-track.org/ajaxauth/login"
TLE_QUERY = "https://www.space-track.org/basicspacedata/query/class/gp/orderby/NORAD_CAT_ID asc/format/tle"

username = st.secrets["username"]
password = st.secrets["password"]

session = requests.Session()
session.post(LOGIN_URL, data={"identity": username, "password": password})
tle_response = session.get(TLE_QUERY)

tle_lines = tle_response.text.strip().splitlines()

# 줄 간격 없이 TLE 재구성
formatted_tle = ""
for i in range(0, len(tle_lines), 2):
    line1 = tle_lines[i]
    line2 = tle_lines[i+1] if i+1 < len(tle_lines) else ""
    sat_name = f"Satellite {i//2 + 1}"
    formatted_tle += f"{sat_name}\n{line1}\n{line2}\n"

st.download_button(
    label="📥 Download Compact TLE",
    data=formatted_tle,
    file_name="compact_tle.txt",
    mime="text/plain"
)
