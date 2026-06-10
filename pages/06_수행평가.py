import streamlit as st
import pandas as pd
import random

# -----------------------------
# 페이지 설정
# -----------------------------
st.set_page_config(
    page_title="🦖 공룡 도감",
    page_icon="🦕",
    layout="wide"
)

# -----------------------------
# 제목
# -----------------------------
st.title("🦖 공룡 도감 탐험")
st.markdown("### 🌎 공룡 친구들을 만나보자!")

st.info("💡 공룡 이름을 선택하면 몸길이, 몸무게, 시대 정보를 확인할 수 있어요!")

# -----------------------------
# 데이터 불러오기
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("aaa(1).csv")
    return df

df = load_data()

# -----------------------------
# 컬럼 찾기
# -----------------------------
name_col = None
size_col = None
weight_col = None
period_col = None

for col in df.columns:
    c = str(col)

    if "한글명" in c:
        name_col = col

    if "크기" in c:
        size_col = col

    if "체중" in c:
        weight_col = col

    if "생존시기" in c:
        period_col = col

# -----------------------------
# 검색
# -----------------------------
search = st.text_input(
    "🔍 공룡 이름 검색",
    placeholder="예) 티라노사우루스"
)

filtered_df = df.copy()

if search:
    filtered_df = filtered_df[
        filtered_df[name_col].astype(str).str.contains(search, case=False)
    ]

# -----------------------------
# 공룡 선택
# -----------------------------
dino_list = filtered_df[name_col].dropna().tolist()

if len(dino_list) == 0:
    st.warning("😢 검색 결과가 없어요!")
    st.stop()

selected = st.selectbox(
    "🦕 공룡을 선택해보세요!",
    dino_list
)

row = filtered_df[filtered_df[name_col] == selected].iloc[0]

# -----------------------------
# 정보 표시
# -----------------------------
st.subheader(f"🦖 {selected}")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "📏 몸길이",
        str(row[size_col])
    )

with col2:
    st.metric(
        "⚖️ 몸무게",
        str(row[weight_col])
    )

with col3:
    st.metric(
        "⏳ 시대",
        str(row[period_col])
    )

# -----------------------------
# 랜덤 추천
# -----------------------------
st.divider()

if st.button("🎲 랜덤 공룡 추천받기"):
    random_dino = random.choice(df[name_col].dropna().tolist())
    st.success(f"✨ 오늘의 추천 공룡은 **{random_dino}** 입니다!")

# -----------------------------
# 시대별 공룡 수
# -----------------------------
st.divider()

st.subheader("📊 시대별 공룡 수")

period_count = (
    df[period_col]
    .value_counts()
    .sort_values(ascending=False)
)

st.bar_chart(period_count)

# -----------------------------
# 전체 데이터 보기
# -----------------------------
with st.expander("📚 전체 공룡 목록 보기"):
    st.dataframe(
        df[[name_col, size_col, weight_col, period_col]],
        use_container_width=True
    )

st.success("🚀 마음에 드는 공룡을 골라서 탐험해보자!")
