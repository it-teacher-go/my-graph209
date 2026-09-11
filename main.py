import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 페이지 설정 및 제목
st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 영화 데이터 그래프 도감 1 - 시간")
st.markdown("KOBIS 일별 박스오피스 데이터를 바탕으로 시간에 따른 영화 관객 수 및 흥행 추이를 시각화합니다.")

# 2. 데이터 불러오기 및 전처리
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"
    df = pd.read_csv(url)
    
    # 날짜 열을 datetime 형식으로 변환 (YYYYMMDD -> YYYY-MM-DD)
    df['날짜'] = pd.to_datetime(df['날짜'].astype(str), format='%Y%m%d')
    
    # 숫자 데이터 형변환 (혹시 모를 문자열 방지)
    numeric_cols = ['순위', '일관객', '누적관객', '스크린수', '상영횟수']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            
    return df

with st.spinner("데이터를 불러오는 중입니다..."):
    df = load_data()

st.sidebar.header("📌 목차 및 안내")
st.sidebar.info("구역별로 다양한 시간 축 기반 그래프가 추가될 예정입니다.")

# -------------------------------------------------------------------
# 구역 1: 개별 영화의 날짜별 일관객 변화
# -------------------------------------------------------------------
st.header("1. 영화별 일관객수 추이")

# 영화 선택 드롭다운 (누적관객수가 많은 순으로 정렬하여 제공)
top_movies = df.groupby('영화명')['누적관객'].max().sort_values(ascending=False).index.tolist()
selected_movie = st.selectbox("영화를 선택하세요:", top_movies)

# 선택한 영화 데이터 필터링
movie_df = df[df['영화명'] == selected_movie].sort_values('날짜')

# 플롯리 선 그래프 생성
fig1 = px.line(
    movie_df,
    x='날짜',
    y='일관객',
    title=f"[{selected_movie}] 날짜별 일관객 수 변화",
    markers=True,
    labels={'날짜': '날짜', '일관객': '일일 관객 수(명)'},
    hover_data={'날짜': "|%Y-%m-%d", '일관객': ':,d'}
)

# 호버 레이아웃 커스텀
fig1.update_traces(
    hovertemplate="<b>날짜:</b> %{x|%Y-%m-%d}<br><b>일관객수:</b> %{y:,}명<extra></extra>"
)

fig1.update_layout(
    xaxis_title="날짜",
    yaxis_title="일관객 수 (명)",
    hovermode="x unified"
)

st.plotly_chart(fig1, use_container_width=True)

# 그래프 분석 문구 위치
st.caption(f"💡 **이 그래프로 알 수 있는 것:** {selected_movie}은(는) 상영 기간 동안 특정 주말이나 개봉 초기에 관객 수가 집중되는 경향을 확인할 수 있습니다.")

st.divider()

# -------------------------------------------------------------------
# 구역 2: 추후 추가될 그래프 구역 (예시)
# -------------------------------------------------------------------
st.header("2. 추가 시각화 구역 (준비 중)")
st.text("앞으로 새로운 시간 기반 시각화 그래프가 이 구역에 지속적으로 추가될 예정입니다.")

# 예시 틀
# st.subheader("2.1 상위 5개 영화의 누적관객 증가 추이")
# ...
# st.caption("💡 **이 그래프로 알 수 있는 것:** ...")
