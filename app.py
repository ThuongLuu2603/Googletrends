"""
Streamlit Web App - Google Trends Travel Analysis
Phân tích thói quen du lịch từ dữ liệu Google Trends cho Vietravel R&D
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from data_simulation import (
    generate_trend_data,
    generate_regional_comparison,
    generate_related_keywords,
    get_popular_keywords
)


# Cấu hình trang
st.set_page_config(
    page_title="Google Trends - Phân tích Du lịch VN",
    page_icon="✈️",
    layout="wide"
)

# CSS tùy chỉnh
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2c3e50;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<p class="main-header">✈️ Google Trends - Phân tích Xu hướng Du lịch Việt Nam</p>', unsafe_allow_html=True)
st.markdown("---")

# Sidebar - Bộ lọc
st.sidebar.title("🔍 Bộ lọc")
st.sidebar.markdown("---")

# Chọn từ khóa
popular_keywords = get_popular_keywords()
keyword = st.sidebar.selectbox(
    "Chọn từ khóa du lịch:",
    options=popular_keywords,
    index=0
)

# Cho phép nhập từ khóa tùy chỉnh
custom_keyword = st.sidebar.text_input("Hoặc nhập từ khóa tùy chỉnh:")
if custom_keyword:
    keyword = custom_keyword

# Chọn khoảng thời gian
st.sidebar.markdown("### 📅 Chọn khoảng thời gian")
time_range = st.sidebar.selectbox(
    "Khoảng thời gian:",
    ["7 ngày qua", "30 ngày qua", "90 ngày qua", "6 tháng qua", "1 năm qua", "Tùy chỉnh"]
)

# Xác định ngày bắt đầu và kết thúc
end_date = datetime.now()
if time_range == "7 ngày qua":
    start_date = end_date - timedelta(days=7)
elif time_range == "30 ngày qua":
    start_date = end_date - timedelta(days=30)
elif time_range == "90 ngày qua":
    start_date = end_date - timedelta(days=90)
elif time_range == "6 tháng qua":
    start_date = end_date - timedelta(days=180)
elif time_range == "1 năm qua":
    start_date = end_date - timedelta(days=365)
else:  # Tùy chỉnh
    col1, col2 = st.sidebar.columns(2)
    with col1:
        start_date = st.date_input("Từ ngày:", end_date - timedelta(days=30))
    with col2:
        end_date = st.date_input("Đến ngày:", end_date)
    start_date = datetime.combine(start_date, datetime.min.time())
    end_date = datetime.combine(end_date, datetime.min.time())

st.sidebar.markdown("---")
st.sidebar.info(f"**Từ khóa đang phân tích:** {keyword}")
st.sidebar.info(f"**Thời gian:** {start_date.strftime('%d/%m/%Y')} - {end_date.strftime('%d/%m/%Y')}")

# Tạo dữ liệu mô phỏng
@st.cache_data
def load_data(keyword, start_date, end_date):
    """Load và cache dữ liệu"""
    return generate_trend_data(keyword, start_date, end_date)

trend_data = load_data(keyword, start_date, end_date)

# Phần 1: Tổng quan
st.markdown('<p class="sub-header">📊 Tổng quan</p>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    avg_all = trend_data['value'].mean()
    st.metric("Mức độ quan tâm trung bình", f"{avg_all:.1f}/100")

with col2:
    avg_north = trend_data[trend_data['region'] == 'Bắc']['value'].mean()
    st.metric("Trung bình - Bắc", f"{avg_north:.1f}/100")

with col3:
    avg_central = trend_data[trend_data['region'] == 'Trung']['value'].mean()
    st.metric("Trung bình - Trung", f"{avg_central:.1f}/100")

with col4:
    avg_south = trend_data[trend_data['region'] == 'Nam']['value'].mean()
    st.metric("Trung bình - Nam", f"{avg_south:.1f}/100")

st.markdown("---")

# Phần 2: Xu hướng theo Thời gian
st.markdown('<p class="sub-header">📈 Xu hướng Tìm kiếm theo Thời gian</p>', unsafe_allow_html=True)

fig_timeline = px.line(
    trend_data,
    x='date',
    y='value',
    color='region',
    title=f'Xu hướng tìm kiếm "{keyword}" theo thời gian',
    labels={
        'date': 'Ngày',
        'value': 'Mức độ quan tâm (0-100)',
        'region': 'Khu vực'
    },
    color_discrete_map={
        'Bắc': '#FF6B6B',
        'Trung': '#4ECDC4',
        'Nam': '#45B7D1'
    }
)

fig_timeline.update_layout(
    hovermode='x unified',
    height=500,
    xaxis_title="Thời gian",
    yaxis_title="Mức độ quan tâm",
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    )
)

st.plotly_chart(fig_timeline, use_container_width=True)

# Thêm thống kê chi tiết
with st.expander("📋 Xem thống kê chi tiết"):
    stats_df = trend_data.groupby('region')['value'].agg([
        ('Trung bình', 'mean'),
        ('Tối đa', 'max'),
        ('Tối thiểu', 'min'),
        ('Độ lệch chuẩn', 'std')
    ]).round(2)
    st.dataframe(stats_df, use_container_width=True)

st.markdown("---")

# Phần 3: So sánh theo Khu vực (Bắc - Trung - Nam)
st.markdown('<p class="sub-header">🗺️ So sánh theo Khu vực (Bắc - Trung - Nam)</p>', unsafe_allow_html=True)

# Tính toán giá trị trung bình cho mỗi khu vực
regional_avg = trend_data.groupby('region')['value'].mean().reset_index()
regional_avg = regional_avg.sort_values('value', ascending=True)

col1, col2 = st.columns(2)

with col1:
    # Biểu đồ cột
    fig_bar = px.bar(
        regional_avg,
        x='region',
        y='value',
        title='So sánh mức độ quan tâm giữa các khu vực',
        labels={
            'region': 'Khu vực',
            'value': 'Mức độ quan tâm trung bình'
        },
        color='region',
        color_discrete_map={
            'Bắc': '#FF6B6B',
            'Trung': '#4ECDC4',
            'Nam': '#45B7D1'
        },
        text='value'
    )
    fig_bar.update_traces(texttemplate='%{text:.1f}', textposition='outside')
    fig_bar.update_layout(showlegend=False, height=400)
    st.plotly_chart(fig_bar, use_container_width=True)

with col2:
    # Biểu đồ tròn
    fig_pie = px.pie(
        regional_avg,
        values='value',
        names='region',
        title='Tỷ lệ phân bố mức độ quan tâm',
        color='region',
        color_discrete_map={
            'Bắc': '#FF6B6B',
            'Trung': '#4ECDC4',
            'Nam': '#45B7D1'
        }
    )
    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
    fig_pie.update_layout(height=400)
    st.plotly_chart(fig_pie, use_container_width=True)

# Bản đồ nhiệt theo thời gian và khu vực
st.markdown("#### 🔥 Bản đồ nhiệt - Xu hướng theo Khu vực và Thời gian")

# Pivot dữ liệu cho heatmap
pivot_data = trend_data.pivot_table(
    values='value',
    index='region',
    columns=trend_data['date'].dt.strftime('%Y-%m-%d'),
    aggfunc='mean'
)

fig_heatmap = px.imshow(
    pivot_data,
    labels=dict(x="Ngày", y="Khu vực", color="Mức độ quan tâm"),
    x=pivot_data.columns,
    y=pivot_data.index,
    color_continuous_scale="RdYlBu_r",
    aspect="auto"
)

fig_heatmap.update_layout(height=300)
fig_heatmap.update_xaxes(side="bottom")

st.plotly_chart(fig_heatmap, use_container_width=True)

st.markdown("---")

# Phần 4: Từ khóa Liên quan
st.markdown('<p class="sub-header">🔗 Từ khóa Liên quan</p>', unsafe_allow_html=True)

related_keywords_df = generate_related_keywords(keyword)

col1, col2 = st.columns([2, 1])

with col1:
    # Biểu đồ thanh ngang
    fig_related = px.bar(
        related_keywords_df,
        x='score',
        y='keyword',
        orientation='h',
        title='Top 10 từ khóa liên quan',
        labels={
            'score': 'Điểm liên quan',
            'keyword': 'Từ khóa'
        },
        color='score',
        color_continuous_scale='Blues',
        text='score'
    )
    fig_related.update_traces(texttemplate='%{text}', textposition='outside')
    fig_related.update_layout(
        height=500,
        yaxis={'categoryorder': 'total ascending'},
        showlegend=False
    )
    st.plotly_chart(fig_related, use_container_width=True)

with col2:
    st.markdown("#### 📝 Danh sách chi tiết")
    for idx, row in related_keywords_df.iterrows():
        st.markdown(f"**{idx + 1}. {row['keyword']}**")
        st.progress(row['score'] / 100)
        st.caption(f"Điểm: {row['score']}/100")

st.markdown("---")

# Phần 5: Insights và Khuyến nghị
st.markdown('<p class="sub-header">💡 Insights & Khuyến nghị</p>', unsafe_allow_html=True)

# Tìm khu vực có mức độ quan tâm cao nhất
top_region = regional_avg.iloc[-1]['region']
top_value = regional_avg.iloc[-1]['value']

col1, col2 = st.columns(2)

with col1:
    st.info(f"""
    **🎯 Khu vực tiềm năng nhất:**
    - Khu vực **{top_region}** có mức độ quan tâm cao nhất ({top_value:.1f}/100)
    - Nên tập trung marketing và phát triển sản phẩm du lịch tại khu vực này
    """)
    
    # Tìm ngày có mức độ quan tâm cao nhất
    peak_date = trend_data.loc[trend_data['value'].idxmax(), 'date']
    peak_value = trend_data['value'].max()
    st.success(f"""
    **📅 Thời điểm cao điểm:**
    - {peak_date.strftime('%d/%m/%Y')} ghi nhận mức độ quan tâm cao nhất ({peak_value:.1f}/100)
    - Đây là thời điểm tốt để tăng cường quảng bá và ưu đãi
    """)

with col2:
    # Top 3 từ khóa liên quan
    top_3_keywords = related_keywords_df.head(3)
    st.warning(f"""
    **🔑 Top 3 từ khóa liên quan nổi bật:**
    1. {top_3_keywords.iloc[0]['keyword']} ({top_3_keywords.iloc[0]['score']}/100)
    2. {top_3_keywords.iloc[1]['keyword']} ({top_3_keywords.iloc[1]['score']}/100)
    3. {top_3_keywords.iloc[2]['keyword']} ({top_3_keywords.iloc[2]['score']}/100)
    
    Nên tích hợp các từ khóa này vào chiến lược SEO
    """)
    
    # Xu hướng tăng/giảm
    recent_trend = trend_data[trend_data['date'] >= (end_date - timedelta(days=7))]
    trend_change = recent_trend.groupby('region')['value'].mean() - trend_data.groupby('region')['value'].mean()
    
    if trend_change.mean() > 0:
        st.success(f"📈 Xu hướng tăng {trend_change.mean():.1f}% trong 7 ngày gần đây")
    else:
        st.error(f"📉 Xu hướng giảm {abs(trend_change.mean()):.1f}% trong 7 ngày gần đây")

st.markdown("---")

# Footer
st.markdown("""
<div style='text-align: center; color: #7f8c8d; padding: 2rem;'>
    <p>📊 <b>Google Trends Travel Analysis Dashboard</b></p>
    <p>Phát triển bởi Vietravel R&D | Dữ liệu mô phỏng cho mục đích phân tích</p>
    <p><i>Sử dụng Streamlit, Pandas, và Plotly</i></p>
</div>
""", unsafe_allow_html=True)
