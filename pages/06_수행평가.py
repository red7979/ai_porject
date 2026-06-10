import streamlit as st
import pandas as pd

# -----------------------
# 페이지 설정
# -----------------------
st.set_page_config(
    page_title="🦖 공룡 도감",
    page_icon="🦕",
    layout="centered"
)

# -----------------------
# 공룡 데이터
# -----------------------
data = {
    "공룡 이름": [
        "티라노사우루스",
        "트리케라톱스",
        "브라키오사우루스",
        "벨로시랩터",
        "스테고사우루스",
        "스피노사우루스",
        "알로사우루스",
        "파라사우롤로푸스",
        "안킬로사우루스",
        "디플로도쿠스"
    ],
    "몸길이(m)": [
        12, 9, 25, 2, 9, 15, 12, 10, 8, 27
    ],
    "몸무게(t)": [
        8, 12, 50, 0.02, 5, 7, 2, 3, 6, 15
    ],
    "시대": [
        "후기 백악기",
        "후기 백악기",
        "후기 쥐라기",
        "후기 백악기",
        "후기 쥐라기",
        "후기 백악기",
        "후기 쥐라기",
        "후기 백악기",
        "후기 백악기",
        "후기 쥐라기"
    ]
}

df = pd.DataFrame(data)

# -----------------------
# 제목
# -----------------------
st.title("🦖 공룡 도감")
st.write("좋아하는 공룡을 선택해 보세요! 🌟")

# -----------------------
# 공룡 선택
# -----------------------
selected = st.selectbox(
    "🦕 공룡 이름 선택",
    df["공룡 이름"]
)

# 선택된 공룡 정보
row = df[df["공룡 이름"] == selected].iloc[0]

st.divider()

st.subheader(f"🦖 {selected}")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "📏 몸길이",
        f"{row['몸길이(m)']} m"
    )

with col2:
    st.metric(
        "⚖️ 몸무게",
        f"{row['몸무게(t)']} t"
    )

with col3:
    st.metric(
        "⏳ 시대",
        row["시대"]
    )

st.divider()

st.success(
    f"✨ {selected}의 몸길이는 {row['몸길이(m)']}m, "
    f"몸무게는 {row['몸무게(t)']}t 입니다!"
)

st.divider()

st.subheader("📊 시대별 공룡 수")

st.bar_chart(df["시대"].value_counts())

with st.expander("📚 전체 공룡 목록 보기"):
    st.dataframe(df, use_container_width=True)

st.balloons()
