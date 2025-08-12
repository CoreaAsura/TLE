import streamlit as st
import requests

LOGIN_URL = "https://www.space-track.org/ajaxauth/login"
TLE_JSON_QUERY = "https://www.space-track.org/basicspacedata/query/class/gp/epoch>%3D2020-01-01/orderby/NORAD_CAT_ID asc/format/json"

username = st.secrets["username"]
password = st.secrets["password"]

session = requests.Session()
session.post(LOGIN_URL, data={"identity": username, "password": password})
tle_response = session.get(TLE_JSON_QUERY)

tle_data = tle_response.json()

formatted_tle = ""
for sat in tle_data:
    name = sat.get("OBJECT_NAME", "Unknown Satellite")
    line1 = sat.get("TLE_LINE1", "")
    line2 = sat.get("TLE_LINE2", "")
    
    if line1.startswith("1 ") and line2.startswith("2 "):
        formatted_tle += f"{name}\n{line1}\n{line2}\n"

st.download_button(
    label="📥 Download Named TLE",
    data=formatted_tle,
    file_name="named_tle.txt",
    mime="text/plain"
)
