import streamlit as st
import folium
from streamlit_folium import st_folium

# 페이지 설정
st.set_page_config(
    page_title="서울 관광지",
    page_icon="🌏",
    layout="wide"
)

# 제목
st.title("🌏 외국인이 좋아하는 서울 관광지 TOP10")
st.write("서울의 대표 관광지를 지도에서 확인해보세요!")

# 서울 중심 지도 생성
m = folium.Map(
    location=[37.5665, 126.9780],
    zoom_start=11
)

# 관광지 리스트
tourist_spots = [
    ["경복궁 🏯", 37.5796, 126.9770],
    ["남산서울타워 🗼", 37.5512, 126.9882],
    ["명동 🛍️", 37.5636, 126.9827],
    ["북촌한옥마을 🏡", 37.5826, 126.9830],
    ["홍대 🎵", 37.5563, 126.9220],
    ["롯데월드 🎡", 37.5110, 127.0980],
    ["DDP ✨", 37.5665, 127.0092],
    ["한강공원 🚲", 37.5207, 126.9390],
    ["인사동 🎨", 37.5740, 126.9850],
    ["코엑스 📚", 37.5125, 127.0588]
]

# 마커 추가
for name, lat, lon in tourist_spots:
    folium.Marker(
        location=[lat, lon],
        popup=name,
        tooltip=name,
        icon=folium.Icon(color="blue")
    ).add_to(m)

# 지도 출력
st_folium(
    m,
    width=1200,
    height=700
)

# 하단 문구
st.markdown("---")
st.caption("Made with ❤️ using Streamlit & Folium")
