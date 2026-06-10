import streamlit as st
import pandas as pd

# -------------------------
# 페이지 설정
# -------------------------
st.set_page_config(
    page_title="🦖 공룡 도감",
    page_icon="🦕",
    layout="wide"
)

# -------------------------
# 제목
# -------------------------
st.title("🦖 공룡 도감")
st.markdown("### 🌟 공룡을 선택하면 몸길이, 몸무게, 시대를 알려줘요!")

# -------------------------
# 데이터 불러오기
# -------------------------
@st.cache_data
def load_data():
    try:
        return pd.read_csv("aaa.csv", encoding="utf-8")
    except:
        return pd.read_csv("aaa.csv", encoding="cp949")

df = load_data()

# -------------------------
# 컬럼명 자동 찾기
# -------------------------
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
    st.error("❌ CSV 컬럼을 찾을 수 없습니다.")
    st.write("현재 컬럼 목록")
    st.write(df.columns.tolist())
    st.stop()

# -------------------------
# 공룡 선택
# -------------------------
dino_name = st.selectbox(
    "🦕 공룡 이름 선택",
    sorted(df[name_col].dropna().unique())
)

selected = df[df[name_col] == dino_name].iloc[0]

# -------------------------
# 정보 출력
# -------------------------
st.divider()

st.subheader(f"🦖 {dino_name}")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "📏 몸길이",
        f"{selected[size_col]}"
    )

with col2:
    st.metric(
        "⚖️ 몸무게",
        f"{selected[weight_col]}"
    )

with col3:
    st.metric(
        "⏳ 시대",
        f"{selected[period_col]}"
    )

# -------------------------
# 설명 출력
# -------------------------
st.divider()

st.success(
    f"✨ {dino_name}의 몸길이는 {selected[size_col]}, "
    f"몸무게는 {selected[weight_col]}, "
    f"생존 시기는 {selected[period_col]} 입니다!"
)

# -------------------------
# 시대별 분포
# -------------------------
st.divider()

st.subheader("📊 시대별 공룡 수")

period_count = df[period_col].value_counts()

st.bar_chart(period_count)

# -------------------------
# 전체 데이터
# -------------------------
with st.expander("📚 전체 공룡 목록 보기"):
    st.dataframe(
        df[[name_col, size_col, weight_col, period_col]],
        use_container_width=True
    )

st.balloons()

st.markdown(
    """
    ---
    🦕 재미있는 공룡 탐험 끝!
    
    다른 공룡도 선택해 보세요 😎
    """
)
