# app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# --------------------------------
# 페이지 설정
# --------------------------------
st.set_page_config(
    page_title="🌍 국가별 MBTI 분석기",
    page_icon="🌈",
    layout="wide"
)

# --------------------------------
# 제목
# --------------------------------
st.title("🌍 국가별 MBTI 비율 분석기")
st.markdown("국가를 선택하면 MBTI 비율을 그래프로 보여줘요 ✨")

# --------------------------------
# 데이터 불러오기
# --------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("countriesMBTI_16types.csv")

    # 컬럼 공백 제거
    df.columns = df.columns.str.strip()

    return df

df = load_data()

# --------------------------------
# MBTI 컬럼 목록
# --------------------------------
mbti_types = [
    "INFJ", "ISFJ", "INTP", "ISFP",
    "ENTP", "INFP", "ENTJ", "ISTP",
    "INTJ", "ESFP", "ESTJ", "ENFP",
    "ESTP", "ISTJ", "ENFJ", "ESFJ"
]

# --------------------------------
# 국가 선택
# --------------------------------
countries = sorted(df["Country"].unique())

selected_country = st.selectbox(
    "🌎 국가를 선택하세요",
    countries
)

# --------------------------------
# 선택 국가 데이터
# --------------------------------
country_row = df[df["Country"] == selected_country]

if country_row.empty:
    st.error("국가 데이터를 찾을 수 없습니다.")
    st.stop()

country_data = country_row.iloc[0]

# --------------------------------
# 값 가져오기
# --------------------------------
values = []

for mbti in mbti_types:

    if mbti in df.columns:
        values.append(float(country_data[mbti]) * 100)
    else:
        values.append(0)

# --------------------------------
# 최고값 찾기
# --------------------------------
max_index = np.argmax(values)

# --------------------------------
# 색상 설정
# 1등 = 노란색
# 나머지 = 하늘색 그라데이션
# --------------------------------
blue_gradient = plt.cm.Blues(
    np.linspace(0.35, 0.85, len(values))
)

colors = []

for i in range(len(values)):

    if i == max_index:
        colors.append("#FFD700")  # 노란색
    else:
        colors.append(blue_gradient[i])

# --------------------------------
# 그래프 생성
# --------------------------------
fig, ax = plt.subplots(figsize=(14, 7))

bars = ax.bar(
    mbti_types,
    values,
    color=colors,
    edgecolor="black"
)

# 값 표시
for bar in bars:

    height = bar.get_height()

    ax.text(
        bar.get_x() + bar.get_width() / 2,
        height + 0.2,
        f"{height:.1f}%",
        ha="center",
        fontsize=10
    )

# --------------------------------
# 그래프 꾸미기
# --------------------------------
ax.set_title(
    f"{selected_country} MBTI 비율 분석 🌈",
    fontsize=22,
    fontweight="bold"
)

ax.set_xlabel("MBTI 유형", fontsize=14)
ax.set_ylabel("비율 (%)", fontsize=14)

ax.set_ylim(0, max(values) + 5)

plt.xticks(rotation=45)

# --------------------------------
# Streamlit 출력
# --------------------------------
st.pyplot(fig)

# --------------------------------
# 최고 MBTI 표시
# --------------------------------
top_mbti = mbti_types[max_index]
top_value = values[max_index]

st.success(
    f"🏆 {selected_country}의 최고 MBTI는 "
    f"{top_mbti} ({top_value:.2f}%) 입니다!"
)
