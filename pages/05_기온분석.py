import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression

st.set_page_config(
    page_title="서울 기온 분석",
    page_icon="🌡️",
    layout="wide"
)

plt.rcParams["axes.unicode_minus"] = False

st.title("🌡️ 서울 기온 분석 및 미래 최고기온 예측")

@st.cache_data
def load_data():

    try:
        df = pd.read_csv("seoul.csv")
    except:
        df = pd.read_csv("seoul.csv", encoding="cp949")

    df.columns = df.columns.str.strip()

    date_col = [c for c in df.columns if "날짜" in c][0]
    max_col = [c for c in df.columns if "최고기온" in c][0]
    min_col = [c for c in df.columns if "최저기온" in c][0]

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

# --------------------
# 선택 영역
# --------------------
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
    "🔮 미래 연도",
    min_value=2020,
    max_value=2200,
    value=2050,
    step=1
)

filtered = df[
    (df["월"] == month) &
    (df["일"] == day)
].copy()

filtered = filtered.dropna(
    subset=[max_col, min_col]
)

if len(filtered) < 5:
    st.warning("예측에 필요한 데이터가 부족합니다.")
    st.stop()

filtered = filtered.sort_values("연도")

years = filtered["연도"]
highs = filtered[max_col]
lows = filtered[min_col]

# --------------------
# AI 예측
# --------------------
X = years.values.reshape(-1, 1)
y = highs.values

model = LinearRegression()
model.fit(X, y)

pred_temp = model.predict([[future_year]])[0]

st.subheader("🔮 미래 최고기온 예측")

st.success(
    f"{month}월 {day}일의 {future_year}년 예상 최고기온은 "
    f"{pred_temp:.1f}℃ 입니다."
)

# --------------------
# 그래프
# --------------------
fig, ax = plt.subplots(figsize=(22, 10))

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
    s=40
)

ax.plot(
    years,
    lows,
    color="#87CEFA",
    linewidth=3,
    marker="o",
    label="최저기온"
)

# 미래 예측점
ax.scatter(
    future_year,
    pred_temp,
    s=250,
    marker="*",
    label=f"{future_year} 예측 최고기온"
)

# 추세선
trend_years = np.append(years.values, future_year)
trend_pred = model.predict(
    trend_years.reshape(-1, 1)
)

ax.plot(
    trend_years,
    trend_pred,
    linestyle="--",
    linewidth=2,
    label="예측 추세선"
)

ax.set_title(
    f"{month}월 {day}일 연도별 기온 및 미래 최고기온 예측",
    fontsize=16
)

ax.set_xlabel("연도")
ax.set_ylabel("기온(℃)")
ax.grid(True, alpha=0.3)

ax.legend()

plt.tight_layout()

st.pyplot(fig)

# --------------------
# 통계
# --------------------
st.subheader("📊 통계")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "역대 최고기온",
        f"{highs.max():.1f}℃"
    )

with c2:
    st.metric(
        "역대 최저기온",
        f"{lows.min():.1f}℃"
    )

with c3:
    st.metric(
        f"{future_year}년 예측",
        f"{pred_temp:.1f}℃"
    )

# --------------------
# 데이터 표
# --------------------
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
