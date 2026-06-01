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
st.markdown("월과 일을 선택하면 해당 날짜의 연도별 최고기온과 최저기온을 확인할 수 있습니다.")

# 데이터 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv("seoul.csv", encoding="cp949")

    # 컬럼명 공백 제거
    df.columns = df.columns.str.strip()

    # 날짜 변환
    df["날짜"] = pd.to_datetime(df["날짜"])

    # 연도, 월, 일 추출
    df["연도"] = df["날짜"].dt.year
    df["월"] = df["날짜"].dt.month
    df["일"] = df["날짜"].dt.day

    return df

df = load_data()

# 사이드바
st.sidebar.header("📅 날짜 선택")

month = st.sidebar.selectbox(
    "월 선택",
    range(1, 13)
)

day = st.sidebar.selectbox(
    "일 선택",
    range(1, 32)
)

# 데이터 필터링
filtered = df[
    (df["월"] == month) &
    (df["일"] == day)
].copy()

# 결측 제거
filtered = filtered.dropna(
    subset=["최고기온(℃)", "최저기온(℃)"]
)

if filtered.empty:
    st.warning("선택한 날짜의 데이터가 없습니다.")
    st.stop()

# 정렬
filtered = filtered.sort_values("연도")

st.subheader(f"📈 {month}월 {day}일의 연도별 기온 변화")

# 그래프 생성
fig, ax = plt.subplots(figsize=(14, 7))

# 최고기온 (무지개색)
years = filtered["연도"]
highs = filtered["최고기온(℃)"]

colors = plt.cm.rainbow(
    np.linspace(0, 1, len(highs))
)

for i in range(len(highs) - 1):
    ax.plot(
        years.iloc[i:i+2],
        highs.iloc[i:i+2],
        color=colors[i],
        linewidth=2.5
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
    filtered["연도"],
    filtered["최저기온(℃)"],
    color="skyblue",
    linewidth=2.5,
    marker="o",
    label="최저기온"
)

ax.set_xlabel("연도")
ax.set_ylabel("기온(℃)")
ax.set_title(f"{month}월 {day}일의 연도별 최고·최저기온")

ax.grid(True, alpha=0.3)
ax.legend()

st.pyplot(fig)

# 데이터 테이블
st.subheader("📋 데이터")

show_df = filtered[
    ["연도", "최고기온(℃)", "최저기온(℃)"]
].reset_index(drop=True)

st.dataframe(
    show_df,
    use_container_width=True
)

# 통계
st.subheader("📊 통계")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "역대 최고기온",
        f"{filtered['최고기온(℃)'].max():.1f}℃"
    )

with col2:
    st.metric(
        "역대 최저기온",
        f"{filtered['최저기온(℃)'].min():.1f}℃"
    )
