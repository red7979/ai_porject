import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(
    page_title="서울 기온 분석",
    page_icon="🌡️",
    layout="wide"
)

st.title("🌡️ 서울 기온 분석")
st.write("월과 일을 선택하면 해당 날짜의 연도별 최고기온과 최저기온을 확인할 수 있습니다.")

# -----------------------------
# 데이터 불러오기
# -----------------------------
@st.cache_data
def load_data():

    # UTF-8 → CP949 순서로 시도
    try:
        df = pd.read_csv("seoul.csv")
    except:
        df = pd.read_csv("seoul.csv", encoding="cp949")

    # 컬럼 공백 제거
    df.columns = df.columns.str.strip()

    # 날짜 컬럼 찾기
    date_col = None
    for col in df.columns:
        if "날짜" in col:
            date_col = col
            break

    if date_col is None:
        st.error("날짜 컬럼을 찾을 수 없습니다.")
        st.stop()

    # 날짜 변환
    df[date_col] = pd.to_datetime(
        df[date_col],
        errors="coerce"
    )

    df = df.dropna(subset=[date_col])

    # 기온 컬럼 찾기
    max_col = None
    min_col = None

    for col in df.columns:

        if "최고기온" in col:
            max_col = col

        if "최저기온" in col:
            min_col = col

    if max_col is None or min_col is None:
        st.error("최고기온 또는 최저기온 컬럼을 찾을 수 없습니다.")
        st.stop()

    # 숫자 변환
    df[max_col] = pd.to_numeric(
        df[max_col],
        errors="coerce"
    )

    df[min_col] = pd.to_numeric(
        df[min_col],
        errors="coerce"
    )

    # 연월일 추출
    df["연도"] = df[date_col].dt.year
    df["월"] = df[date_col].dt.month
    df["일"] = df[date_col].dt.day

    return df, max_col, min_col

df, max_col, min_col = load_data()

# -----------------------------
# 날짜 선택
# -----------------------------
st.sidebar.header("📅 날짜 선택")

month = st.sidebar.selectbox(
    "월 선택",
    list(range(1, 13))
)

day = st.sidebar.selectbox(
    "일 선택",
    list(range(1, 32))
)

# -----------------------------
# 필터링
# -----------------------------
filtered = df[
    (df["월"] == month) &
    (df["일"] == day)
].copy()

filtered = filtered.dropna(
    subset=[max_col, min_col]
)

if filtered.empty:
    st.warning("해당 날짜의 데이터가 없습니다.")
    st.stop()

filtered = filtered.sort_values("연도")

# -----------------------------
# 그래프
# -----------------------------
st.subheader(f"📈 {month}월 {day}일 연도별 최고·최저기온")

fig, ax = plt.subplots(figsize=(15, 7))

years = filtered["연도"]
highs = filtered[max_col]
lows = filtered[min_col]

# 최고기온 무지개색
rainbow_colors = plt.cm.rainbow(
    np.linspace(0, 1, len(highs))
)

for i in range(len(highs) - 1):
    ax.plot(
        years.iloc[i:i+2],
        highs.iloc[i:i+2],
        color=rainbow_colors[i],
        linewidth=3
    )

# 범례용
ax.plot(
    [],
    [],
    color="red",
    linewidth=3,
    label="최고기온"
)

# 최저기온
ax.plot(
    years,
    lows,
    color="skyblue",
    linewidth=3,
    marker="o",
    label="최저기온"
)

ax.set_xlabel("연도")
ax.set_ylabel("기온 (℃)")
ax.set_title(
    f"{month}월 {day}일의 연도별 최고기온 · 최저기온"
)

ax.grid(True, alpha=0.3)
ax.legend()

st.pyplot(fig)

# -----------------------------
# 통계
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    st.metric(
        "역대 최고기온",
        f"{highs.max():.1f}℃"
    )

with col2:
    st.metric(
        "역대 최저기온",
        f"{lows.min():.1f}℃"
    )

# -----------------------------
# 데이터 표
# -----------------------------
st.subheader("📋 데이터")

table_df = pd.DataFrame({
    "연도": years,
    "최고기온(℃)": highs,
    "최저기온(℃)": lows
})

st.dataframe(
    table_df,
    use_container_width=True
)
