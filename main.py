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
st.sidebar.info("구역별로 다양한 시간 축 기반 그래프가 추가되는 중입니다.")

# -------------------------------------------------------------------
# 구역 1: 개별 영화의 날짜별 일관객 변화
# -------------------------------------------------------------------
st.header("1. 개별 영화의 일관객수 추이")

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
    labels={'날짜': '날짜', '일관객': '일일 관객 수(명)'}
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
# 구역 2: 상위 5개 영화의 일관객수 비교
# -------------------------------------------------------------------
st.header("2. 기간 내 일관객 합계 상위 5개 영화 비교")

# 일관객 합계가 가장 큰 5개 영화 추출
top5_movies = df.groupby('영화명')['일관객'].sum().nlargest(5).index.tolist()

# 상위 5개 영화 데이터 필터링
top5_df = df[df['영화명'].isin(top5_movies)].sort_values('날짜')

# 플롯리 멀티 선 그래프 생성 (영화명으로 색상 구분)
fig2 = px.line(
    top5_df,
    x='날짜',
    y='일관객',
    color='영화명',
    title=f"일관객 합계 TOP 5 영화 날짜별 비교 ({', '.join(top5_movies)})",
    labels={'날짜': '날짜', '일관객': '일일 관객 수(명)', '영화명': '영화 제목'}
)

# 호버 레이아웃 커스텀
fig2.update_traces(
    hovertemplate="<b>영화:</b> %{fullData.name}<br><b>날짜:</b> %{x|%Y-%m-%d}<br><b>일관객수:</b> %{y:,}명<extra></extra>"
)

fig2.update_layout(
    xaxis_title="날짜",
    yaxis_title="일관객 수 (명)",
    legend_title_text="영화 목록 (클릭하여 토글)",
    hovermode="x"
)

st.plotly_chart(fig2, use_container_width=True)

# 그래프 분석 문구 위치
st.caption("💡 **이 그래프로 알 수 있는 것:** 해당 기간 일관객 수가 가장 많았던 Top 5 영화 간의 개봉 시기별 흥행 경쟁 상황과 최대 흥행 화력(피크 관객수) 차이를 한눈에 비교해볼 수 있습니다.")

st.divider()

# -------------------------------------------------------------------
# 구역 3: 날짜별 10위권 일관객 합계 추이 (영역 그래프)
# -------------------------------------------------------------------
st.header("3. 날짜별 TOP 10 박스오피스 전체 관객 수 추이")

# 날짜별 일관객 합계 계산
daily_total = df.groupby('날짜')['일관객'].sum().reset_index().sort_values('날짜')

# 관객 수 합계가 가장 컸던 상위 3개 날짜 추출
top3_days = daily_total.nlargest(3, '일관객')

# 영역 그래프 생성
fig3 = px.area(
    daily_total,
    x='날짜',
    y='일관객',
    title="날짜별 TOP 10 박스오피스 일관객 합계 추이",
    labels={'날짜': '날짜', '일관객': '총 일관객 수(명)'}
)

fig3.update_traces(
    hovertemplate="<b>날짜:</b> %{x|%Y-%m-%d}<br><b>TOP 10 일관객 합계:</b> %{y:,}명<extra></extra>"
)

# 상위 3일 날짜 및 데이터 주석(Annotation) 추가
for idx, row in top3_days.iterrows():
    date_str = row['날짜'].strftime('%Y-%m-%d')
    audience = row['일관객']
    fig3.add_annotation(
        x=row['날짜'],
        y=audience,
        text=f"<b>TOP {top3_days.index.get_loc(idx)+1}</b><br>{date_str}<br>({audience:,}명)",
        showarrow=True,
        arrowhead=2,
        arrowsize=1,
        arrowwidth=2,
        arrowcolor="red",
        ax=0,
        ay=-40,
        bgcolor="rgba(255, 255, 255, 0.8)",
        bordercolor="red",
        borderwidth=1,
        borderpad=4
    )

fig3.update_layout(
    xaxis_title="날짜",
    yaxis_title="총 관객 수 (명)",
    hovermode="x unified"
)

st.plotly_chart(fig3, use_container_width=True)

# 그래프 분석 문구 위치
top3_dates_text = ", ".join([row['날짜'].strftime('%Y-%m-%d') for _, row in top3_days.iterrows()])
st.caption(f"💡 **이 그래프로 알 수 있는 것:** 극장가 전체 시장의 흥행 성수기와 비수기 흐름을 파악할 수 있으며, 일관객 합계가 가장 높았던 상위 3일({top3_dates_text})은 명절 연휴나 대형 신작 개봉 주말 등 극장 피크 시즌에 해당합니다.")

st.divider()

# -------------------------------------------------------------------
# 구역 4: 기간 내 관객 수 TOP 10 영화 (가로 막대그래프)
# -------------------------------------------------------------------
st.header("4. 기간 내 관객 수 TOP 10 영화 비교")

# 체크박스를 통해 정렬/추출 기준 선택
use_max_cumulative = st.checkbox("누적관객수 기준으로 보기 (체크 해제 시 일관객 합계 기준)", value=True)

# 영화별 일관객 합계, 누적관객 최댓값 및 10위권 진입 일수 계산
top10_summary = df.groupby('영화명').agg(
    총일관객=('일관객', 'sum'),
    최대누적관객=('누적관객', 'max'),
    차트진입일수=('날짜', 'count')
).reset_index()

if use_max_cumulative:
    target_col = '최대누적관객'
    metric_label = '최대 누적관객 수(명)'
    chart_title = "기간 내 최대 누적관객 수 TOP 10 영화"
else:
    target_col = '총일관객'
    metric_label = '총 일관객 수(명)'
    chart_title = "기간 내 일관객 합계 TOP 10 영화"

# 관객 수 기준 상위 10개 영화 선택 및 오름차순 정렬 (Plotly 가로 막대는 아래에서 위로 그려짐)
top10_movies_df = top10_summary.nlargest(10, target_col).sort_values(target_col, ascending=True)

# 가로 막대 그래프 생성
fig4 = px.bar(
    top10_movies_df,
    x=target_col,
    y='영화명',
    orientation='h',
    title=f"{chart_title} (10위권 차트인 일수 포함)",
    labels={target_col: metric_label, '영화명': '영화 제목', '차트진입일수': '10위권 유지 일수'},
    hover_data={'차트진입일수': True, target_col: ':,d'}
)

# 호버 레이아웃 커스텀
fig4.update_traces(
    hovertemplate=f"<b>영화명:</b> %{{y}}<br><b>{metric_label}:</b> %{{x:,}}명<br><b>10위권 유지 일수:</b> %{{customdata[0]}}일<extra></extra>"
)

fig4.update_layout(
    xaxis_title=metric_label,
    yaxis_title="영화 제목",
    showlegend=False
)

st.plotly_chart(fig4, use_container_width=True)

# 그래프 분석 문구 위치
if use_max_cumulative:
    st.caption("💡 **이 그래프로 알 수 있는 것:** 해당 1년 데이터 기간 동안 기록된 최대 누적관객수 기준 상위 10개 영화를 보여줍니다. 이전 연도부터 개봉해 누적 관객을 쌓아온 대형 흥행작의 전체 스케일을 파악하기 적합합니다.")
else:
    st.caption("💡 **이 그래프로 알 수 있는 것:** 해당 1년 데이터 기간 내에서 순수하게 발생한 일관객의 합계 기준 TOP 10 영화입니다. 이 기간 동안 실제로 극장가에서 가장 많은 관객을 끌어모은 실질적 흥행작을 비교할 수 있습니다.")

st.divider()

# -------------------------------------------------------------------
# 구역 5: 월×요일별 일관객 합계 히트맵
# -------------------------------------------------------------------
st.header("5. 월×요일별 관객 수 집계 (히트맵)")

# 날짜 데이터에서 월과 요일 추출
df_heatmap = df.copy()
df_heatmap['월'] = df_heatmap['날짜'].dt.month.astype(str) + "월"
df_heatmap['요일'] = df_heatmap['날짜'].dt.day_name()

# 요일 한글 변환 및 정렬 순서 지정 (월요일 ~ 일요일)
day_map = {
    'Monday': '월요일',
    'Tuesday': '화요일',
    'Wednesday': '수요일',
    'Thursday': '목요일',
    'Friday': '금요일',
    'Saturday': '토요일',
    'Sunday': '일요일'
}
df_heatmap['요일'] = df_heatmap['요일'].map(day_map)

# 월과 요일 정렬 기준 설정
months_order = [f"{i}월" for i in sorted(df_heatmap['날짜'].dt.month.unique())]
days_order = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일']

# 월 및 요일별 일관객 합계 피벗 테이블 생성
pivot_df = df_heatmap.pivot_table(
    index='월',
    columns='요일',
    values='일관객',
    aggfunc='sum'
).reindex(index=months_order, columns=days_order).fillna(0)

# 히트맵 생성 (관객 수가 많을수록 진한 색상)
fig5 = px.imshow(
    pivot_df,
    labels=dict(x="요일", y="월", color="총 관객 수(명)"),
    x=days_order,
    y=months_order,
    color_continuous_scale="Reds",
    title="월×요일별 일관객 합계 히트맵"
)

# 호버 커스텀 및 텍스트 라이팅
fig5.update_traces(
    hovertemplate="<b>월:</b> %{y}<br><b>요일:</b> %{x}<br><b>총 일관객수:</b> %{z:,}명<extra></extra>"
)

fig5.update_layout(
    xaxis_title="요일",
    yaxis_title="월",
    coloraxis_colorbar=dict(title="총 관객 수")
)

st.plotly_chart(fig5, use_container_width=True)

# 그래프 분석 문구 위치
st.caption("💡 **이 그래프로 알 수 있는 것:** 몇 월의 무슨 요일에 극장 관객이 가장 몰리는지 한눈에 파악할 수 있으며, 주말(토/일) 피크 및 특정 달의 명절·휴일 효과가 요일별 관객 수에 어떤 영향을 미쳤는지 직관적으로 비교할 수 있습니다.")

st.divider()

# -------------------------------------------------------------------
# 구역 6: 추후 추가될 그래프 구역
# -------------------------------------------------------------------
st.header("6. 추가 시각화 구역 (준비 중)")
st.text("앞으로 새로운 시간 기반 시각화 그래프가 이 구역에 지속적으로 추가될 예정입니다.")
