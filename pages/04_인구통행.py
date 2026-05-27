import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import platform
import re

# ---------------------------
# 페이지 설정
# ---------------------------
st.set_page_config(
    page_title="서울 인구 분석",
    page_icon="📊",
    layout="wide"
)

st.title("📊 서울 행정구별 연령 인구 꺾은선 그래프")

# ---------------------------
# 한글 폰트 설정
# ---------------------------
system_name = platform.system()

if system_name == "Windows":
    plt.rc("font", family="Malgun Gothic")
elif system_name == "Darwin":
    plt.rc("font", family="AppleGothic")
else:
    plt.rc("font", family="NanumGothic")

plt.rcParams["axes.unicode_minus"] = False

# ---------------------------
# 데이터 불러오기
# ---------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("population.csv", encoding="cp949")
    return df

df = load_data()

# ---------------------------
# 행정구 컬럼
# ---------------------------
region_col = df.columns[0]

# ---------------------------
# 연령 컬럼 추출
# ---------------------------
age_columns = []
ages = []

for col in df.columns:

    col_str = str(col)

    # "0세", "1세" 등 포함된 컬럼만 선택
    if re.search(r'(\d+)세', col_str):

        age = int(re.search(r'(\d+)세', col_str).group(1))

        # 중복 제거
        if age not in ages:
            age_columns.append(col)
            ages.append(age)

# ---------------------------
# 행정구 선택
# ---------------------------
regions = df[region_col].tolist()

selected_region = st.selectbox(
    "행정구를 선택하세요",
    regions
)

# ---------------------------
# 선택 데이터
# ---------------------------
selected_row = df[df[region_col] == selected_region]

population_values = []

for col in age_columns:

    value = selected_row[col].iloc[0]

    # 숫자 변환
    value = str(value).replace(",", "")

    try:
        value = int(value)
    except:
        value = 0

    population_values.append(value)

# ---------------------------
# 그래프 생성
# ---------------------------
fig, ax = plt.subplots(figsize=(18, 7))

ax.plot(
    ages,
    population_values,
    color="hotpink",
    linewidth=3,
    marker="o",
    markersize=4
)

# ---------------------------
# 제목
# ---------------------------
ax.set_title(
    f"{selected_region} 연령별 인구수",
    fontsize=22,
    fontweight="bold"
)

# ---------------------------
# 축 라벨
# ---------------------------
ax.set_xlabel("나이", fontsize=15)
ax.set_ylabel("인구수", fontsize=15)

# ---------------------------
# x축 설정
# ---------------------------
ax.set_xticks(range(0, 101, 10))
ax.set_xlim(0, 100)

# ---------------------------
# 격자
# ---------------------------
ax.grid(
    axis="x",
    linestyle="--",
    alpha=0.7
)

ax.grid(
    True,
    linestyle=":",
    alpha=0.3
)

# ---------------------------
# Streamlit 출력
# ---------------------------
st.pyplot(fig)

# ---------------------------
# 데이터 테이블
# ---------------------------
st.subheader("📋 연령별 인구 데이터")

result_df = pd.DataFrame({
    "나이": ages,
    "인구수": population_values
})

st.dataframe(
    result_df,
    use_container_width=True
)
