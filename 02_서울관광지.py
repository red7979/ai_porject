import streamlit as st
    zoom_start=11
)

# 관광지 데이터
places = [
    {
        "name": "경복궁 🏯",
        "location": [37.5796, 126.9770],
        "description": "조선 시대의 대표 궁궐"
    },
    {
        "name": "남산서울타워 🗼",
        "location": [37.5512, 126.9882],
        "description": "서울 야경 명소"
    },
    {
        "name": "명동 🛍️",
        "location": [37.5636, 126.9827],
        "description": "쇼핑과 길거리 음식의 천국"
    },
    {
        "name": "북촌한옥마을 🏡",
        "location": [37.5826, 126.9830],
        "description": "전통 한옥이 모여 있는 마을"
    },
    {
        "name": "홍대 🎵",
        "location": [37.5563, 126.9220],
        "description": "젊음과 예술의 거리"
    },
    {
        "name": "롯데월드 🎡",
        "location": [37.5110, 127.0980],
        "description": "서울 대표 테마파크"
    },
    {
        "name": "동대문디자인플라자(DDP) ✨",
        "location": [37.5665, 127.0092],
        "description": "미래형 건축 랜드마크"
    },
    {
        "name": "한강공원 🚲",
        "location": [37.5207, 126.9390],
        "description": "서울 시민들의 휴식 공간"
    },
    {
        "name": "인사동 🎨",
        "location": [37.5740, 126.9850],
        "description": "전통 문화 거리"
    },
    {
        "name": "코엑스 & 별마당도서관 📚",
        "location": [37.5125, 127.0588],
        "description": "쇼핑과 문화가 함께하는 공간"
    }
]

# 마커 추가
for place in places:
    folium.Marker(
        location=place["location"],
        popup=f"<b>{place['name']}</b><br>{place['description']}",
        tooltip=place["name"],
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(seoul_map)

# 지도 출력
st_folium(seoul_map, width=1200, height=700)

st.markdown("---")
st.caption("Made with ❤️ using Streamlit & Folium")
