import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import platform

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
    return pd.read_csv("population.csv", encoding="cp949")

df = load_data()

# ---------------------------
# 행정구 컬럼
# ---------------------------
region_col = df.columns[0]

# ---------------------------
# 나이 컬럼 찾기
# ---------------------------
age_columns = []

for col in df.columns:
    if "세" in col:
        age_columns.append(col)

# ---------------------------
# 나이 숫자 추출
# ---------------------------
ages = []

for col in age_columns:
    num = ''.join(filter(str.isdigit, col))

    if num == "":
        ages.append(100)
    else:
        ages.append(int(num))

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

population_values = selected_row[age_columns].iloc[0]

# 숫자 변환
population_values = [
    int(str(v).replace(",", ""))
    for v in population_values
]

# ---------------------------
# 꺾은선 그래프
# ---------------------------
fig, ax = plt.subplots(figsize=(16, 6))

ax.plot(
    ages,
    population_values,
    linestyle="-",       # 선 연결
    marker="o",          # 점 표시
    markersize=4,
    linewidth=2.5,
    color="hotpink"
)

# 제목
ax.set_title(
    f"{selected_region} 연령별 인구수",
    fontsize=20,
    fontweight="bold"
)

# 축 라벨
ax.set_xlabel("나이", fontsize=14)
ax.set_ylabel("인구수", fontsize=14)

# x축 10살 단위
ax.set_xticks(range(0, 101, 10))

# 세로 구분선
ax.grid(
    axis="x",
    linestyle="--",
    alpha=0.6
)

# 전체 격자
ax.grid(
    True,
    linestyle=":",
    alpha=0.3
)

# Streamlit 출력
st.pyplot(fig)

# ---------------------------
# 데이터 표
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
