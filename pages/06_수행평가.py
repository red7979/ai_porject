import streamlit as st
import pandas as pd

# -----------------------------
# 페이지 설정
# -----------------------------
st.set_page_config(
    page_title="🦖 공룡 분석 프로젝트",
    page_icon="🦕",
    layout="wide"
)

# -----------------------------
# 공룡 풍선 효과 🦖
# -----------------------------
st.markdown("""
<style>
.dino {
    position: fixed;
    bottom: -80px;
    font-size: 40px;
    animation: rise 8s linear infinite;
    z-index: 999;
}

.d1 { left: 10%; animation-delay: 0s; }
.d2 { left: 25%; animation-delay: 2s; }
.d3 { left: 40%; animation-delay: 4s; }
.d4 { left: 60%; animation-delay: 1s; }
.d5 { left: 80%; animation-delay: 3s; }

@keyframes rise {
    0% {
        transform: translateY(0);
        opacity: 1;
    }
    100% {
        transform: translateY(-120vh);
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

# -----------------------------
# 공룡 데이터
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
        "안킬로사우루스",
        "파라사우롤로푸스",
        "디플로도쿠스"
    ],
    "몸길이(m)": [
        12, 9, 25, 2, 9,
        15, 12, 8, 10, 27
    ],
    "몸무게(t)": [
        8, 12, 50, 0.02, 5,
        7, 2, 6, 3, 15
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

# -----------------------------
# 제목
# -----------------------------
st.title("🦖 공룡 분석 프로젝트")
st.markdown("### 🌎 공룡의 세계에 오신 것을 환영합니다!")

st.info("🦕 공룡 이름을 선택하면 몸길이, 몸무게, 시대를 확인할 수 있어요!")

# -----------------------------
# 공룡 선택
# -----------------------------
selected = st.selectbox(
    "🦖 공룡을 선택하세요!",
    df["공룡 이름"]
)

row = df[df["공룡 이름"] == selected].iloc[0]

# -----------------------------
# 결과 출력
# -----------------------------
st.divider()

st.subheader(f"🦕 {selected}")

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

# -----------------------------
# 설명
# -----------------------------
st.divider()

st.success(
    f"✨ {selected}의 몸길이는 {row['몸길이(m)']}m, "
    f"몸무게는 {row['몸무게(t)']}t이며 "
    f"{row['시대']}에 살았어요!"
)

# -----------------------------
# 공룡 상식
# -----------------------------
st.divider()

st.subheader("🤩 공룡 상식")

st.write("""
🦖 티라노사우루스는 강력한 턱을 가진 육식 공룡이에요.

🦕 브라키오사우루스는 긴 목을 이용해 높은 나뭇잎을 먹었어요.

☄️ 약 6600만 년 전 소행성 충돌 이후 대부분의 공룡이 멸종했어요.

🐦 현재의 새들은 공룡의 후손으로 알려져 있어요.
""")

# -----------------------------
# 전체 데이터 보기
# -----------------------------
with st.expander("📚 전체 공룡 데이터 보기"):
    st.dataframe(df, use_container_width=True)

st.success("🚀 공룡 탐험 완료! 다른 공룡도 선택해 보세요!")
