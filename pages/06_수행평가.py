import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="🦖 공룡 분석 프로젝트",
    page_icon="🦕",
    layout="wide"
)

# -----------------------------
# 공룡 배경
# -----------------------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(to bottom, #87CEEB, #E8F5E9);
}

.dino-bg {
    position: fixed;
    bottom: 0;
    width: 100%;
    opacity: 0.08;
    font-size: 80px;
    text-align: center;
    z-index: -1;
}
</style>

<div class="dino-bg">
🦕 🌴 🦖 🌴 🦕 🌴 🦖
</div>
""", unsafe_allow_html=True)

# -----------------------------
# 데이터
# -----------------------------
data = {
    "공룡 이름": [
        "티라노사우루스",
        "트리케라톱스",
        "브라키오사우루스",
        "벨로시랩터",
        "스테고사우루스",
        "스피노사우루스",
        "알로사우루스",
        "안킬로사우루스"
    ],
    "몸길이(m)": [12, 9, 25, 2, 9, 15, 12, 8],
    "몸무게(t)": [8, 12, 50, 0.02, 5, 7, 2, 6],
    "시대": [
        "후기 백악기",
        "후기 백악기",
        "후기 쥐라기",
        "후기 백악기",
        "후기 쥐라기",
        "후기 백악기",
        "후기 쥐라기",
        "후기 백악기"
    ]
}

df = pd.DataFrame(data)

# -----------------------------
# 제목
# -----------------------------
st.title("🦖 공룡 분석 프로젝트")
st.markdown("### 🌎 1억 년 전부터 현재까지 공룡 탐험!")

# -----------------------------
# 공룡 선택
# -----------------------------
selected = st.selectbox(
    "🦕 공룡을 선택하세요",
    df["공룡 이름"]
)

row = df[df["공룡 이름"] == selected].iloc[0]

c1, c2, c3 = st.columns(3)

with c1:
    st.metric("📏 몸길이", f"{row['몸길이(m)']} m")

with c2:
    st.metric("⚖️ 몸무게", f"{row['몸무게(t)']} t")

with c3:
    st.metric("⏳ 시대", row["시대"])

# -----------------------------
# 시대별 공룡 분포
# -----------------------------
st.divider()
st.subheader("📊 시대별 공룡 분포")

period_count = df["시대"].value_counts()

fig1, ax1 = plt.subplots(figsize=(4, 2.5))
ax1.bar(period_count.index, period_count.values)
ax1.set_title("시대별 공룡 수")
ax1.set_ylabel("수")

st.pyplot(fig1)

# -----------------------------
# 1억년 전 ~ 현재
# -----------------------------
st.divider()
st.subheader("📈 1억 년 전부터 현재까지")

timeline = pd.DataFrame({
    "백만 년 전": [100, 80, 66, 0],
    "공룡 다양성": [70, 95, 100, 0]
})

fig2, ax2 = plt.subplots(figsize=(4, 2.5))
ax2.plot(
    timeline["백만 년 전"],
    timeline["공룡 다양성"],
    marker="o"
)

ax2.set_title("공룡 다양성 변화")
ax2.set_xlabel("백만 년 전")
ax2.set_ylabel("다양성")

st.pyplot(fig2)

# -----------------------------
# 설명
# -----------------------------
st.info("""
🦖 약 1억 년 전 공룡은 매우 번성했어요.

🌟 약 8천만 년 전에는 다양한 종류가 등장했어요.

☄️ 약 6,600만 년 전 소행성 충돌 이후 대부분 멸종했어요.

🐦 오늘날 새는 공룡의 후손으로 알려져 있어요.
""")

# -----------------------------
# 전체 데이터
# -----------------------------
with st.expander("📚 전체 공룡 데이터"):
    st.dataframe(df, use_container_width=True)

st.success("🚀 공룡 탐험 완료!")
