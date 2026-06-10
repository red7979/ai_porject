import streamlit as st
import pandas as pd
import random

st.set_page_config(
    page_title="🦖 공룡 도감",
    page_icon="🦕",
    layout="wide"
)

st.title("🦖 공룡 도감 탐험")
st.markdown("### 🌟 공룡 정보를 쉽고 재미있게 알아보자!")

st.info("📁 먼저 CSV 파일을 업로드해주세요!")

uploaded_file = st.file_uploader(
    "🦕 공룡 CSV 파일 선택",
    type=["csv"]
)

if uploaded_file is None:
    st.stop()

# CSV 읽기
try:
    df = pd.read_csv(uploaded_file, encoding="utf-8")
except:
    try:
        df = pd.read_csv(uploaded_file, encoding="cp949")
    except:
        st.error("❌ CSV 파일을 읽을 수 없습니다.")
        st.stop()

# 컬럼 자동 찾기
name_col = None
size_col = None
weight_col = None
period_col = None

for col in df.columns:
    col_str = str(col)

    if "한글명" in col_str:
        name_col = col

    if "크기" in col_str:
        size_col = col

    if "체중" in col_str:
        weight_col = col

    if "생존시기" in col_str:
        period_col = col

# 컬럼 확인
if None in [name_col, size_col, weight_col, period_col]:
    st.error("❌ 필요한 컬럼을 찾을 수 없습니다.")
    st.write("현재 컬럼 목록")
    st.write(df.columns.tolist())
    st.stop()

# 검색
search = st.text_input(
    "🔍 공룡 이름 검색",
    placeholder="예) 티라노사우루스"
)

filtered_df = df.copy()

if search:
    filtered_df = filtered_df[
        filtered_df[name_col]
        .astype(str)
        .str.contains(search, case=False, na=False)
    ]

if len(filtered_df) == 0:
    st.warning("😢 검색 결과가 없습니다.")
    st.stop()

# 공룡 선택
selected = st.selectbox(
    "🦖 공룡을 선택하세요!",
    filtered_df[name_col].tolist()
)

dino = filtered_df[
    filtered_df[name_col] == selected
].iloc[0]

st.divider()

st.subheader(f"🦕 {selected}")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "📏 몸길이(m)",
        str(dino[size_col])
    )

with col2:
    st.metric(
        "⚖️ 몸무게(t)",
        str(dino[weight_col])
    )

with col3:
    st.metric(
        "⏳ 시대",
        str(dino[period_col])
    )

st.divider()

# 랜덤 추천
if st.button("🎲 랜덤 공룡 추천"):
    random_dino = random.choice(
        df[name_col].dropna().tolist()
    )

    st.success(
        f"🌟 오늘의 추천 공룡은 **{random_dino}** 입니다!"
    )

st.divider()

# 시대별 개수
st.subheader("📊 시대별 공룡 분포")

period_count = (
    df[period_col]
    .value_counts()
)

st.bar_chart(period_count)

st.divider()

# 전체 목록
with st.expander("📚 전체 공룡 데이터 보기"):
    st.dataframe(
        df[
            [
                name_col,
                size_col,
                weight_col,
                period_col
            ]
        ],
        use_container_width=True
    )

st.success("🚀 공룡 탐험 완료! 다른 공룡도 찾아보자!")
