# app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# -----------------------------------
# 페이지 설정
# -----------------------------------
st.set_page_config(
    page_title="🦖 국가별 MBTI 분석기",
    page_icon="🦖",
    layout="wide"
)

# -----------------------------------
# 공룡 배너
# -----------------------------------
st.markdown("""
<h1 style='text-align:center;'>
🦖🌋 국가별 MBTI 분석기 🌋🦕
</h1>

<h4 style='text-align:center;'>
국가별 MBTI 비율과 MBTI별 국가 순위를 확인해보세요 ✨
</h4>

<hr>
""", unsafe_allow_html=True)

# -----------------------------------
# 데이터 불러오기
# -----------------------------------
@st.cache_data
def load_data():

    df = pd.read_csv("countriesMBTI_16types.csv")

    df.columns = df.columns.str.strip()

    return df

df = load_data()

# -----------------------------------
# MBTI 목록
# -----------------------------------
mbti_types = [
    "INFJ", "ISFJ", "INTP", "ISFP",
    "ENTP", "INFP", "ENTJ", "ISTP",
    "INTJ", "ESFP", "ESTJ", "ENFP",
    "ESTP", "ISTJ", "ENFJ", "ESFJ"
]

# -----------------------------------
# 탭 생성
# -----------------------------------
tab1, tab2 = st.tabs(
    [
        "🌎 국가별 MBTI 분석",
        "🏆 MBTI 국가 순위"
    ]
)

# =====================================================
# TAB 1
# =====================================================
with tab1:

    st.subheader("🌎 국가별 MBTI 비율")

    countries = sorted(df["Country"].unique())

    selected_country = st.selectbox(
        "국가를 선택하세요",
        countries,
        key="country_select"
    )

    country_data = df[df["Country"] == selected_country].iloc[0]

    values = []

    for mbti in mbti_types:
        values.append(float(country_data[mbti]) * 100)

    graph_df = pd.DataFrame({
        "MBTI": mbti_types,
        "비율": values
    })

    # 높은 순 정렬
    graph_df = graph_df.sort_values(
        by="비율",
        ascending=False
    )

    # 초록 그라데이션
    green_colors = plt.cm.Greens(
        np.linspace(0.35, 0.85, len(graph_df))
    )

    colors = []

    for i in range(len(graph_df)):

        if i == 0:
            colors.append("#00C853")
        else:
            colors.append(green_colors[i])

    fig, ax = plt.subplots(
        figsize=(14, 7)
    )

    ax.set_navigate(False)

    bars = ax.bar(
        graph_df["MBTI"],
        graph_df["비율"],
        color=colors,
        edgecolor="black"
    )

    for bar in bars:

        height = bar.get_height()

        ax.text(
            bar.get_x() + bar.get_width()/2,
            height + 0.2,
            f"{height:.1f}%",
            ha="center"
        )

    ax.set_title(
        f"{selected_country} MBTI 순위",
        fontsize=20,
        fontweight="bold"
    )

    ax.set_xlabel("MBTI")
    ax.set_ylabel("비율 (%)")

    plt.xticks(rotation=45)

    st.pyplot(
        fig,
        clear_figure=True,
        use_container_width=True
    )

    st.success(
        f"🥇 1위 MBTI : {graph_df.iloc[0]['MBTI']} "
        f"({graph_df.iloc[0]['비율']:.2f}%)"
    )

    st.dataframe(
        graph_df,
        use_container_width=True
    )

# =====================================================
# TAB 2
# =====================================================
with tab2:

    st.subheader("🏆 MBTI별 국가 TOP10")

    selected_mbti = st.selectbox(
        "MBTI 선택",
        mbti_types,
        key="mbti_select"
    )

    rank_df = df[
        ["Country", selected_mbti]
    ].copy()

    rank_df[selected_mbti] = (
        rank_df[selected_mbti] * 100
    )

    rank_df = rank_df.sort_values(
        by=selected_mbti,
        ascending=False
    )

    top10 = rank_df.head(10)

    green_colors = plt.cm.Greens(
        np.linspace(0.35, 0.85, len(top10))
    )

    colors = []

    for i in range(len(top10)):

        if i == 0:
            colors.append("#00C853")
        else:
            colors.append(green_colors[i])

    fig2, ax2 = plt.subplots(
        figsize=(14, 7)
    )

    ax2.set_navigate(False)

    bars2 = ax2.bar(
        top10["Country"],
        top10[selected_mbti],
        color=colors,
        edgecolor="black"
    )

    for bar in bars2:

        height = bar.get_height()

        ax2.text(
            bar.get_x() + bar.get_width()/2,
            height + 0.2,
            f"{height:.1f}%",
            ha="center"
        )

    ax2.set_title(
        f"{selected_mbti} 비율 국가 TOP10",
        fontsize=20,
        fontweight="bold"
    )

    ax2.set_xlabel("국가")
    ax2.set_ylabel("비율 (%)")

    plt.xticks(rotation=30)

    st.pyplot(
        fig2,
        clear_figure=True,
        use_container_width=True
    )

    st.success(
        f"🥇 1위 국가 : "
        f"{top10.iloc[0]['Country']} "
        f"({top10.iloc[0][selected_mbti]:.2f}%)"
    )

    top10_display = top10.copy()

    top10_display.index = range(
        1,
        len(top10_display) + 1
    )

    top10_display.index.name = "순위"

    st.dataframe(
        top10_display,
        use_container_width=True
    )
