import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import platform

# ---------------------------
# 페이지 설정
# ---------------------------
st.set_page_config(
    page_title="서울 인구 분석",
    page_icon="📊",
    layout="wide"
)

st.title("📊 서울 행정구별 연령 인구 분석")

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
# 컬럼 정리
# ---------------------------
# 행정구 이름 컬럼 찾기
region_col = df.columns[0]

# 나이 컬럼 추출
age_columns = []

for col in df.columns:
    if "세" in col:
        age_columns.append(col)

# 나이 숫자만 추출
ages = []

for col in age_columns:
    number = ''.join(filter(str.isdigit, col))

    if number == '':
        ages.append(100)
    else:
        ages.append(int(number))

# ---------------------------
# 행정구 선택
# ---------------------------
regions = df[region_col].tolist()

selected_region = st.selectbox(
    "행정구를 선택하세요",
    regions
)

# ---------------------------
# 선택한 행정구 데이터
# ---------------------------
selected_data = df[df[region_col] == selected_region]

population_values = selected_data[age_columns].iloc[0].values

# 문자열 숫자 처리
population_values = [
    int(str(v).replace(",", ""))
    for v in population_values
]

# ---------------------------
# 그래프 생성
# ---------------------------
fig, ax = plt.subplots(figsize=(15, 6))

ax.plot(
    ages,
    population_values,
    color="hotpink",
    linewidth=3
)

# 제목
ax.set_title(
    f"{selected_region} 연령별 인구수",
    fontsize=18,
    fontweight="bold"
)

# 축 라벨
ax.set_xlabel("나이", fontsize=13)
ax.set_ylabel("인구수", fontsize=13)

# 10살 단위 구분선
ax.set_xticks(range(0, 101, 10))

# 세로 구분선
ax.grid(
    axis="x",
    linestyle="--",
    alpha=0.6
)

# 전체 그리드
ax.grid(
    True,
    linestyle=":",
    alpha=0.3
)

st.pyplot(fig)

# ---------------------------
# 데이터 표 보기
# ---------------------------
st.subheader("📋 연령별 인구 데이터")

chart_df = pd.DataFrame({
    "나이": ages,
    "인구수": population_values
})

st.dataframe(chart_df, use_container_width=True)
