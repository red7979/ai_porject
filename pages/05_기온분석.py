import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="서울 기온 분석",
    page_icon="🌡️",
    layout="wide"
)

plt.rcParams["axes.unicode_minus"] = False

st.title("🌡️ 서울 기온 분석")
st.markdown("월·일을 선택하면 해당 날짜의 연도별 최고기온과 최저기온을 확인하고 미래 최고기온을 예측합니다.")

# -----------------------------
# 데이터 불러오기
# -----------------------------
@st.cache_data
def load_data():

    try:
        df = pd.read_csv("seoul.csv")
    except:
        df = pd.read_csv("seoul.csv", encoding="cp949")

    df.columns = df.columns.str.strip()

    date_col = None
    max_col = None
    min_col = None

    for col in df.columns:
        if "날짜" in col:
            date_col = col
        elif "최고기온" in col:
            max_col = col
        elif "최저기온" in col:
            min_col = col

    if date_col is None:
        st.error("날짜 컬럼을 찾을 수 없습니다.")
        st.stop()

    df[date_col] = pd.to_datetime(
        df[date_col],
        errors="coerce",
        format="mixed"
    )

    df = df.dropna(subset=[date_col])

    df[max_col] = pd.to_numeric(df[max_col], errors="coerce")
    df[min_col] = pd.to_numeric(df[min_col], errors="coerce")

    df["연도"] = df[date_col].dt.year
    df["월"] = df[date_col].dt.month
    df["일"] = df[date_col].dt.day

    return df, max_col, min_col

df, max_col, min_col = load_data()

# -----------------------------
# 사이드바
# -----------------------------
st.sidebar.header("📅 날짜 선택")

month = st.sidebar.selectbox(
    "월 선택",
    range(1, 13)
)

day = st.sidebar.selectbox(
    "일 선택",
    range(1, 32)
)

future_year = st.sidebar.number_input(
    "🔮 미래 연도 선택",
    min_value=2020,
    max_value=2200,
    value=2050
)

# -----------------------------
# 데이터 필터링
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

years = filtered["연도"]
highs = filtered[max_col]
lows = filtered[min_col]

# -----------------------------
# 미래 최고기온 예측
# -----------------------------
if len(filtered) >= 10:

    coef = np.polyfit(
        years.values,
        highs.values,
        2
    )

    pred_temp = np.polyval(
        coef,
        future_year
    )

    trend_years = np.append(
        years.values,
        future_year
    )

    trend_pred = np.polyval(
        coef,
        trend_years
    )

else:
    pred_temp = None

# -----------------------------
# 예측 결과
# -----------------------------
st.subheader("🔮 미래 최고기온 예측")

if pred_temp is not None:

    st.success(
        f"{future_year}년 {month}월 {day}일 예상 최고기온 : "
        f"{pred_temp:.1f}℃"
    )

else:
    st.warning("예측에 필요한 데이터가 부족합니다.")

# -----------------------------
# 그래프
# -----------------------------
st.subheader(
    f"📈 {month}월 {day}일 연도별 최고·최저기온"
)

fig, ax = plt.subplots(
    figsize=(20, 10)
)

# 최고기온 무지개색
colors = plt.cm.rainbow(
    np.linspace(0, 1, len(highs))
)

for i in range(len(highs)-1):
    ax.plot(
        years.iloc[i:i+2],
        highs.iloc[i:i+2],
        color=colors[i],
        linewidth=3
    )

ax.scatter(
    years,
    highs,
    c=colors,
    s=30
)

# 범례용 최고기온
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
    color="#87CEFA",
    linewidth=3,
    marker="o",
    markersize=4,
    label="최저기온"
)

# 미래 예측 표시
if pred_temp is not None:

    ax.scatter(
        future_year,
        pred_temp,
        s=250,
        marker="*",
        label=f"{future_year} 예측 최고기온"
    )

    ax.plot(
        trend_years,
        trend_pred,
        linestyle="--",
        linewidth=2,
        label="예측 추세선"
    )

# 촘촘한 연도 표시
step = max(1, len(years) // 20)

ax.set_xticks(
    years.iloc[::step]
)

ax.tick_params(
    axis="x",
    rotation=45
)

ax.set_xlabel("연도")
ax.set_ylabel("기온(℃)")

ax.grid(
    True,
    linestyle="--",
    alpha=0.4
)

ax.legend()

plt.tight_layout()

st.pyplot(fig)

# -----------------------------
# 통계
# -----------------------------
st.subheader("📊 통계")

col1, col2, col3 = st.columns(3)

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

with col3:
    if pred_temp is not None:
        st.metric(
            f"{future_year}년 예측",
            f"{pred_temp:.1f}℃"
        )

# -----------------------------
# 데이터 표
# -----------------------------
st.subheader("📋 데이터")

result = pd.DataFrame({
    "연도": years,
    "최고기온(℃)": highs,
    "최저기온(℃)": lows
})

st.dataframe(
    result,
    use_container_width=True,
    height=500
)
