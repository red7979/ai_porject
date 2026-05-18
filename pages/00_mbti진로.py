import streamlit as st

st.set_page_config(
    page_title="✨ MBTI 진로 추천기",
    page_icon="💼",
    layout="centered"
)

# MBTI별 진로 데이터
mbti_jobs = {
    "INTJ": [
        {
            "job": "🧠 데이터 분석가",
            "major": "컴퓨터공학과, 통계학과",
            "personality": "분석적이고 계획 세우는 걸 좋아하는 사람!",
            "salary": "평균 연봉 약 4,500만 원"
        },
        {
            "job": "🔬 연구원",
            "major": "자연과학계열, 생명과학과",
            "personality": "집중력이 높고 탐구심이 강한 사람!",
            "salary": "평균 연봉 약 5,000만 원"
        }
    ],

    "INTP": [
        {
            "job": "💻 프로그래머",
            "major": "소프트웨어학과, 컴퓨터공학과",
            "personality": "논리적이고 새로운 걸 만드는 걸 좋아하는 사람!",
            "salary": "평균 연봉 약 4,800만 원"
        },
        {
            "job": "🧪 과학자",
            "major": "물리학과, 화학과",
            "personality": "호기심 많고 탐구를 좋아하는 사람!",
            "salary": "평균 연봉 약 5,200만 원"
        }
    ],

    "ENTJ": [
        {
            "job": "📈 CEO",
            "major": "경영학과",
            "personality": "리더십 있고 목표 지향적인 사람!",
            "salary": "평균 연봉 약 7,000만 원 이상"
        },
        {
            "job": "⚖️ 변호사",
            "major": "법학과",
            "personality": "판단력이 좋고 자신감 있는 사람!",
            "salary": "평균 연봉 약 8,000만 원"
        }
    ],

    "ENTP": [
        {
            "job": "🎤 마케팅 기획자",
            "major": "광고홍보학과",
            "personality": "아이디어가 많고 말하는 걸 좋아하는 사람!",
            "salary": "평균 연봉 약 4,300만 원"
        },
        {
            "job": "🚀 창업가",
            "major": "경영학과",
            "personality": "도전 정신이 강한 사람!",
            "salary": "수입 차이가 크지만 성공 시 매우 높음!"
        }
    ],

    "INFJ": [
        {
            "job": "🩺 심리상담사",
            "major": "심리학과",
            "personality": "공감 능력이 뛰어나고 배려심 많은 사람!",
            "salary": "평균 연봉 약 4,000만 원"
        },
        {
            "job": "✍️ 작가",
            "major": "문예창작과",
            "personality": "감수성이 풍부하고 상상력이 좋은 사람!",
            "salary": "수입 차이가 있음"
        }
    ],

    "INFP": [
        {
            "job": "🎨 일러스트레이터",
            "major": "디자인학과",
            "personality": "창의적이고 감성적인 사람!",
            "salary": "평균 연봉 약 3,500만 원"
        },
        {
            "job": "🎬 영상 제작자",
            "major": "영상학과",
            "personality": "자기 표현을 좋아하는 사람!",
            "salary": "평균 연봉 약 4,000만 원"
        }
    ],

    "ENFJ": [
        {
            "job": "👩‍🏫 교사",
            "major": "교육학과",
            "personality": "사람을 잘 이끌고 친절한 사람!",
            "salary": "평균 연봉 약 5,000만 원"
        },
        {
            "job": "🤝 HR 담당자",
            "major": "경영학과",
            "personality": "사람들과 소통하는 걸 좋아하는 사람!",
            "salary": "평균 연봉 약 4,500만 원"
        }
    ],

    "ENFP": [
        {
            "job": "📺 방송인",
            "major": "방송연예과",
            "personality": "에너지 넘치고 밝은 사람!",
            "salary": "수입 차이가 큼"
        },
        {
            "job": "✈️ 여행 기획자",
            "major": "관광학과",
            "personality": "자유롭고 활동적인 사람!",
            "salary": "평균 연봉 약 3,800만 원"
        }
    ],

    "ISTJ": [
        {
            "job": "🏦 회계사",
            "major": "회계학과",
            "personality": "꼼꼼하고 책임감 강한 사람!",
            "salary": "평균 연봉 약 6,000만 원"
        },
        {
            "job": "👮 경찰관",
            "major": "경찰행정학과",
            "personality": "원칙을 중요하게 생각하는 사람!",
            "salary": "평균 연봉 약 4,500만 원"
        }
    ],

    "ISFJ": [
        {
            "job": "💉 간호사",
            "major": "간호학과",
            "personality": "배려심 많고 성실한 사람!",
            "salary": "평균 연봉 약 4,700만 원"
        },
        {
            "job": "🏫 사회복지사",
            "major": "사회복지학과",
            "personality": "남을 돕는 걸 좋아하는 사람!",
            "salary": "평균 연봉 약 3,500만 원"
        }
    ],

    "ESTJ": [
        {
            "job": "📊 공무원",
            "major": "행정학과",
            "personality": "체계적이고 책임감 있는 사람!",
            "salary": "평균 연봉 약 4,500만 원"
        },
        {
            "job": "🏢 관리자",
            "major": "경영학과",
            "personality": "리더십 있고 추진력 있는 사람!",
            "salary": "평균 연봉 약 5,500만 원"
        }
    ],

    "ESFJ": [
        {
            "job": "🎓 유치원 교사",
            "major": "유아교육과",
            "personality": "친절하고 사교적인 사람!",
            "salary": "평균 연봉 약 3,500만 원"
        },
        {
            "job": "💄 뷰티 컨설턴트",
            "major": "미용학과",
            "personality": "사람 꾸미는 걸 좋아하는 사람!",
            "salary": "평균 연봉 약 3,800만 원"
        }
    ],

    "ISTP": [
        {
            "job": "🔧 엔지니어",
            "major": "기계공학과",
            "personality": "손재주 좋고 문제 해결을 좋아하는 사람!",
            "salary": "평균 연봉 약 5,000만 원"
        },
        {
            "job": "🚗 자동차 정비사",
            "major": "자동차학과",
            "personality": "실습과 기계를 좋아하는 사람!",
            "salary": "평균 연봉 약 4,000만 원"
        }
    ],

    "ISFP": [
        {
            "job": "📸 사진작가",
            "major": "사진학과",
            "personality": "감각적이고 자유로운 사람!",
            "salary": "평균 연봉 약 3,500만 원"
        },
        {
            "job": "🎵 음악가",
            "major": "실용음악과",
            "personality": "예술 감각이 뛰어난 사람!",
            "salary": "수입 차이가 큼"
        }
    ],

    "ESTP": [
        {
            "job": "🏀 스포츠 트레이너",
            "major": "체육학과",
            "personality": "활동적이고 에너지 넘치는 사람!",
            "salary": "평균 연봉 약 4,000만 원"
        },
        {
            "job": "💼 영업 전문가",
            "major": "경영학과",
            "personality": "사람 만나는 걸 좋아하는 사람!",
            "salary": "평균 연봉 약 5,000만 원"
        }
    ],

    "ESFP": [
        {
            "job": "🎤 연예인",
            "major": "연극영화과",
            "personality": "끼 많고 밝은 사람!",
            "salary": "수입 차이가 큼"
        },
        {
            "job": "☕ 바리스타",
            "major": "호텔조리학과",
            "personality": "사람들과 어울리는 걸 좋아하는 사람!",
            "salary": "평균 연봉 약 3,300만 원"
        }
    ]
}

# 제목
st.title("✨ MBTI 진로 추천기 💼")
st.write("내 MBTI에 어울리는 직업이 궁금하다면?! 😎")
st.write("아래에서 MBTI를 선택해봐! 👇")

# 선택
selected_mbti = st.selectbox(
    "🧩 MBTI를 골라주세요!",
    list(mbti_jobs.keys())
)

# 결과 출력
if selected_mbti:
    st.success(f"🎉 {selected_mbti} 유형에게 추천하는 진로야!")

    jobs = mbti_jobs[selected_mbti]

    for idx, job in enumerate(jobs, start=1):
        st.subheader(f"{idx}. {job['job']}")

        st.write(f"📚 **추천 학과** : {job['major']}")
        st.write(f"💖 **잘 맞는 성격** : {job['personality']}")
        st.write(f"💰 **평균 연봉** : {job['salary']}")

        st.divider()

st.caption("🌈 재미로 보는 추천이니까 너무 진지하게만 보진 말기!")
