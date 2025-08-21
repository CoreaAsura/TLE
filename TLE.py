import io
import re
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

import pandas as pd
import streamlit as st
from dateutil import parser as dateparser
from zoneinfo import ZoneInfo

st.set_page_config(page_title="Space-Track TIP → CSV", page_icon="🛰️", layout="wide")

st.title("🛰️ Space-Track TIP → CSV")
st.write(
    "Space-Track TIP 메시지(텍스트 또는 CSV/TSV)를 입력하면 **예상 추락(재돌입) 시각**, **좌표(위도/경도)**, **비행방향**을 계산해 CSV로 내보내는 웹앱입니다.\n\n"
    "- 입력: 붙여넣기 텍스트 / 파일 업로드(CSV, TSV).\n"
    "- 출력: 정규화된 테이블, 지도 표시, CSV 다운로드.\n"
)

# ---------------------------------------------
# Parsing helpers
# ---------------------------------------------

TIP_COLUMNS = [
    "NORAD_CAT_ID", "MSG_EPOCH", "INSERT_EPOCH", "DECAY_EPOCH", "WINDOW", "REV",
    "DIRECTION", "LAT", "LON", "INCL", "NEXT_REPORT", "ID", "HIGH_INTEREST", "OBJECT_NUMBER"
]

HEADER_HINTS = {c: re.compile(rf"\b{re.escape(c)}\b", re.I) for c in TIP_COLUMNS}


def _looks_like_header(line: str) -> bool:
    if not line:
        return False
    score = sum(1 for c, pat in HEADER_HINTS.items() if pat.search(line))
    return score >= 3  # at least 3 known columns appear


def parse_window_to_minutes(value: Any) -> Optional[float]:
    """
    Accepts numeric minutes (e.g., "42"), or HH:MM:SS (e.g., "00:42:00").
    Returns total minutes as float, or None.
    """
    if value is None:
        return None
    s = str(value).strip()
    if not s:
        return None
    # Try integer/float minutes
    try:
        return float(s)
    except Exception:
        pass
    # Try HH:MM:SS
    m = re.match(r"^(\d{1,2}):(\d{2})(?::(\d{2}))?$", s)
    if m:
        hh = int(m.group(1))
        mm = int(m.group(2))
        ss = int(m.group(3)) if m.group(3) else 0
        return (hh * 60.0) + (mm) + (ss / 60.0)
    # Try HHH:MM:SS (sometimes window can be > 99h)
    m2 = re.match(r"^(\d+):(\d{2}):(\d{2})$", s)
    if m2:
        hh = int(m2.group(1))
        mm = int(m2.group(2))
        ss = int(m2.group(3))
        return (hh * 60.0) + (mm) + (ss / 60.0)
    return None


def safe_parse_datetime(val: Any) -> Optional[datetime]:
    if val is None or (isinstance(val, float) and pd.isna(val)):
        return None
    s = str(val).strip()
    if not s:
        return None
    # Accepts ISO-like strings, Space-Track formats, or already-datetime
    try:
        if isinstance(val, datetime):
            return val
        dt = dateparser.parse(s)
        # Force to naive UTC if timezone-aware, then set tz
        if dt.tzinfo is not None:
            return dt.astimezone(ZoneInfo("UTC")).replace(tzinfo=ZoneInfo("UTC"))
        return dt.replace(tzinfo=ZoneInfo("UTC"))
    except Exception:
        return None


def normalize_direction(d: Any) -> Optional[str]:
    if d is None or (isinstance(d, float) and pd.isna(d)):
        return None
    s = str(d).strip().upper()
    if s in {"ASC", "A", "ASCENDING"}:
        return "Ascending (northbound)"
    if s in {"DESC", "D", "DESCENDING"}:
        return "Descending (southbound)"
    return s or None


def coerce_float(val: Any) -> Optional[float]:
    if val is None or (isinstance(val, float) and pd.isna(val)):
        return None
    s = str(val).strip()
    if not s:
        return None
    try:
        return float(s)
    except Exception:
        # Try with N/E/S/W suffixes like 34.2N 128.9E
        m = re.match(r"^([+-]?\d+(?:\.\d+)?)([NnSsEeWw])$", s)
        if m:
            num = float(m.group(1))
            hemi = m.group(2).upper()
            if hemi == "S":
                num = -abs(num)
            if hemi == "W":
                num = -abs(num)
            return num
        return None


def parse_tip_text_block(text: str) -> pd.DataFrame:
    """Attempt to parse a paste-in TIP block. Supports:
    - Clean CSV/TSV with header row
    - Space/comma separated with header row
    - Key=Value pairs per line or blob
    Returns DataFrame with 0..n rows.
    """
    text = text.strip()
    if not text:
        return pd.DataFrame(columns=TIP_COLUMNS)

    # 1) Try pandas inference (CSV/TSV with header)
    try:
        df_try = pd.read_csv(io.StringIO(text), sep=None, engine="python")
        # If it looks like TIP columns (≥3 known columns), accept
        if any(col in df_try.columns for col in TIP_COLUMNS):
            return df_try
    except Exception:
        pass

    # 2) Try detect a header + one or more data lines (space/comma separated)
    lines = [ln for ln in text.splitlines() if ln.strip()]
    header_idx = next((i for i, ln in enumerate(lines) if _looks_like_header(ln)), None)
    if header_idx is not None and header_idx < len(lines) - 1:
        header = re.split(r"[\s,\t]+", lines[header_idx].strip())
        records = []
        for ln in lines[header_idx + 1 : ]:
            parts = re.split(r"[\s,\t]+", ln.strip())
            if len(parts) >= min(3, len(header)):
                row = {header[i]: parts[i] for i in range(min(len(header), len(parts)))}
                records.append(row)
        if records:
            return pd.DataFrame(records)

    # 3) Fallback: key=value (or key: value) pairs inside text
    #    Split text into blocks per object (blank-line separated)
    blocks: List[str] = re.split(r"\n\s*\n+", text)
    recs: List[Dict[str, Any]] = []
    for blk in blocks:
        kvs = dict(re.findall(r"([A-Z_]+)\s*[:=]\s*([^\n,]+)", blk, flags=re.I))
        if kvs:
            recs.append(kvs)
    if recs:
        return pd.DataFrame(recs)

    # Nothing recognized
    return pd.DataFrame(columns=TIP_COLUMNS)


# ---------------------------------------------
# Data normalization and enrichment
# ---------------------------------------------

def normalize_tip_df(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df

    # Standardize columns
    cols_lower = {c.lower(): c for c in df.columns}
    rename_map = {}
    for std in TIP_COLUMNS:
        for c in df.columns:
            if c.strip().lower() == std.lower():
                rename_map[c] = std
    df = df.rename(columns=rename_map)

    # Add missing columns
    for c in TIP_COLUMNS:
        if c not in df.columns:
            df[c] = None

    # Parse types
    df["WINDOW_MIN"] = df["WINDOW"].apply(parse_window_to_minutes)
    df["DECAY_DT_UTC"] = df["DECAY_EPOCH"].apply(safe_parse_datetime)

    # Compute window start/end (assume WINDOW is **total width**, so ±window/2)
    def _win_start(dt: Optional[datetime], wmin: Optional[float]) -> Optional[datetime]:
        if dt and wmin is not None:
            return dt - timedelta(minutes=wmin/2.0)
        return None

    def _win_end(dt: Optional[datetime], wmin: Optional[float]) -> Optional[datetime]:
        if dt and wmin is not None:
            return dt + timedelta(minutes=wmin/2.0)
        return None

    df["WINDOW_START_UTC"] = [ _win_start(dt, w) for dt, w in zip(df["DECAY_DT_UTC"], df["WINDOW_MIN"]) ]
    df["WINDOW_END_UTC"]   = [ _win_end(dt, w)   for dt, w in zip(df["DECAY_DT_UTC"], df["WINDOW_MIN"]) ]

    # Coordinates and direction
    df["LAT"] = df["LAT"].apply(coerce_float)
    df["LON"] = df["LON"].apply(coerce_float)
    df["FLIGHT_DIRECTION"] = df["DIRECTION"].apply(normalize_direction)

    # Reorder useful columns for output
    order = [
        "NORAD_CAT_ID", "ID", "OBJECT_NUMBER", "DECAY_EPOCH", "DECAY_DT_UTC", "WINDOW",
        "WINDOW_MIN", "WINDOW_START_UTC", "WINDOW_END_UTC", "LAT", "LON",
        "DIRECTION", "FLIGHT_DIRECTION", "INCL", "REV", "MSG_EPOCH", "INSERT_EPOCH",
        "NEXT_REPORT", "HIGH_INTEREST"
    ]
    # Keep only columns that exist
    order = [c for c in order if c in df.columns]
    df = df[order]

    return df


# ---------------------------------------------
# UI - Inputs
# ---------------------------------------------

with st.sidebar:
    st.header("입력")
    tz_name = st.selectbox("표시 타임존", ["UTC", "Asia/Seoul"], index=1)
    st.caption("CSV에는 UTC 시각도 함께 포함됩니다.")

uploaded = st.file_uploader("TIP CSV/TSV 파일 업로드 (선택)", type=["csv", "tsv", "txt"])
text_input = st.text_area(
    "또는 TIP 메시지를 그대로 붙여넣기",
    height=220,
    placeholder=(
        "예)\n"
        "NORAD_CAT_ID,MSG_EPOCH,INSERT_EPOCH,DECAY_EPOCH,WINDOW,REV,DIRECTION,LAT,LON,INCL,NEXT_REPORT,ID,HIGH_INTEREST,OBJECT_NUMBER\n"
        "62123,2025-08-20T12:00:00Z,2025-08-20T12:05:00Z,2025-08-21T03:14:00Z,00:20:00,12345,ASC,12.3N,45.6E,51.6,2025-08-21T02:30:00Z,TI-1234,N,2024-220A"
    ),
)

# Parse input
source_df = pd.DataFrame()
if uploaded is not None:
    content = uploaded.read().decode("utf-8", errors="ignore")
    source_df = parse_tip_text_block(content)
elif text_input.strip():
    source_df = parse_tip_text_block(text_input)

# Show raw parse
st.subheader("1) 원본 파싱 결과")
if source_df.empty:
    st.info("파일을 업로드하거나 텍스트를 붙여넣으면 여기 표시됩니다.")
else:
    st.dataframe(source_df, use_container_width=True)

# Normalize and enrich
st.subheader("2) 표준화 및 계산 결과")
if source_df.empty:
    st.stop()

norm_df = normalize_tip_df(source_df.copy())

# Timezone-converted view (display only)
if tz_name != "UTC":
    tz = ZoneInfo(tz_name)
    def to_tz(dt: Optional[datetime]) -> Optional[datetime]:
        if dt is None:
            return None
        return dt.astimezone(tz)
    view_df = norm_df.copy()
    for c in ["DECAY_DT_UTC", "WINDOW_START_UTC", "WINDOW_END_UTC"]:
        if c in view_df.columns:
            view_df[c.replace("_UTC", f"_{tz_name}")] = view_df[c].apply(to_tz)
else:
    view_df = norm_df.copy()

st.dataframe(view_df, use_container_width=True)

# Map
st.subheader("3) 지도")
coords = norm_df[["LAT", "LON"]].dropna()
if not coords.empty:
    coords = coords.rename(columns={"LAT": "lat", "LON": "lon"})
    st.map(coords, use_container_width=True)
else:
    st.caption("지도를 표시하려면 LAT/LON 값이 필요합니다.")

# CSV Download
st.subheader("4) CSV 다운로드")
csv_bytes = norm_df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="정규화 CSV 다운로드",
    data=csv_bytes,
    file_name="tip_normalized.csv",
    mime="text/csv",
)

st.caption(
    "참고: WINDOW 값은 **총 폭(total width)** 으로 가정하여, DECAY_EPOCH 기준 ±(WINDOW/2)로 시작/종료 시각을 계산합니다."
)