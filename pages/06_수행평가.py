import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="🦖 공룡 분석 프로젝트",
    page_icon="🦕",
    layout="wide"
)

# 공룡 올라오는 효과
st.markdown("""
<style>
.dino {
    position: fixed;
    bottom: -50px;
    font-size: 40px;
    animation: rise 6s linear infinite;
}

.d1 { left: 10%; animation-delay: 0s; }
.d2 { left: 30%; animation-delay: 2s; }
.d3 { left: 50%; animation-delay: 4s; }
.d4 { left: 70%; animation-delay: 1s; }
.d5 { left: 90%; animation-delay: 3s; }

@keyframes rise {
    from {
        transform: translateY(0);
        opacity: 1;
    }
    to {
        transform: translateY(-110vh);
        opacity: 0;
    }
}
</style>

<div class="dino d1">🦖</div>
<div class="dino d2">🦕</div>
<div class="dino d3">🦖</div>
<div class="dino d4">🦕</div>
<div class="dino d5">🦖</div>
""", unsafe_allow_html=True)

# 데이터
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

st.title("🦖 공룡 분석 프로젝트")
st.markdown("### 🌎 공룡의 세계로 떠나보자!")

selected = st.selectbox(
    "🦕 공룡을 선택하세요",
    df["공룡 이름"]
)

row = df[df["공룡 이름"] == selected].iloc[0]

st.subheader(f"🦖 {selected}")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric("📏 몸길이", f"{row['몸길이(m)']} m")

with c2:
    st.metric("⚖️ 몸무게", f"{row['몸무게(t)']} t")

with c3:
    st.metric("⏳ 시대", row["시대"])

st.divider()

st.subheader("📊 시대별 공룡 수")

period_count = df["시대"].value_counts()

# 기본 그래프 (드래그/확대 기능 없음)
st.bar_chart(period_count)

st.divider()

st.subheader("📈 1억 년 전부터 현재까지")

timeline = pd.DataFrame({
    "연도(백만 년 전)": [100, 80, 66, 0],
    "공룡 다양성 지수": [70, 95, 100, 0]
})

st.line_chart(
    timeline.set_index("연도(백만 년 전)")
)

st.info("""
🦖 약 1억 년 전 공룡은 매우 번성했어요.

☄️ 약 6600만 년 전 소행성 충돌 이후 대부분 멸종했어요.

🐦 오늘날의 새는 공룡의 후손으로 알려져 있어요.
""")

with st.expander("📚 전체 공룡 데이터 보기"):
    st.dataframe(df, use_container_width=True)

st.success("🚀 공룡 탐험 완료!")
