import streamlit as st
import folium
from streamlit_folium import st_folium

# 페이지 설정
st.set_page_config(
    page_title="서울 관광지 TOP10",
    page_icon="🌏",
    layout="wide"
)

# 제목
st.title("🌏 외국인이 좋아하는 서울 관광지 TOP10")
st.write("서울의 대표 관광지를 지도에서 확인해보세요! ✨")

# 서울 지도 생성
seoul_map = folium.Map(
    location=[37.5665, 126.9780],
    zoom_start=11
)

# 관광지 리스트
places = [
    {
        "name": "경복궁 🏯",
        "lat": 37.5796,
        "lon": 126.9770,
        "desc": "조선 시대의 대표 궁궐"
    },
    {
        "name": "남산서울타워 🗼",
        "lat": 37.5512,
        "lon": 126.9882,
        "desc": "서울 야경 명소"
    },
    {
        "name": "명동 🛍️",
        "lat": 37.5636,
        "lon": 126.9827,
        "desc": "쇼핑과 길거리 음식의 천국"
    },
    {
        "name": "북촌한옥마을 🏡",
        "lat": 37.5826,
        "lon": 126.9830,
        "desc": "전통 한옥 마을"
    },
    {
        "name": "홍대 🎵",
        "lat": 37.5563,
        "lon": 126.9220,
        "desc": "젊음과 예술의 거리"
    },
    {
        "name": "롯데월드 🎡",
        "lat": 37.5110,
        "lon": 127.0980,
        "desc": "서울 대표 테마파크"
    },
    {
        "name": "DDP ✨",
        "lat": 37.5665,
        "lon": 127.0092,
        "desc": "동대문디자인플라자"
    },
    {
        "name": "한강공원 🚲",
        "lat": 37.5207,
        "lon": 126.9390,
        "desc": "서울 시민들의 휴식 공간"
    },
    {
        "name": "인사동 🎨",
        "lat": 37.5740,
        "lon": 126.9850,
        "desc": "전통 문화 거리"
    },
    {
        "name": "코엑스 별마당도서관 📚",
        "lat": 37.5125,
        "lon": 127.0588,
        "desc": "유명 대형 도서관"
    }
]

# 마커 추가
for place in places:
    folium.Marker(
        location=[place["lat"], place["lon"]],
        popup=f"""
        <b>{place['name']}</b><br>
        {place['desc']}
        """,
        tooltip=place["name"],
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(seoul_map)

# 지도 출력
st_folium(seoul_map, width=1200, height=700)

# 하단 문구
st.markdown("---")
st.caption("Made with ❤️ using Streamlit & Folium")
