# Google Trends - Phân tích Xu hướng Du lịch Việt Nam ✈️

Web Application Streamlit để phân tích thói quen du lịch từ dữ liệu Google Trends cho Vietravel R&D.

## 📋 Mục tiêu

Phân tích thói quen du lịch từ dữ liệu Google Trends với các tính năng:
- ✅ Phân tích chia theo 3 khu vực: **Bắc, Trung, Nam**
- ✅ Dashboard tương tác với bộ lọc từ khóa và thời gian
- ✅ Visualization đa dạng: xu hướng theo thời gian, so sánh khu vực, từ khóa liên quan
- ✅ Dữ liệu mô phỏng sẵn sàng để chạy ngay

## 🚀 Cài đặt và Chạy

### Yêu cầu hệ thống
- Python 3.8 trở lên
- pip (Python package manager)

### Các bước cài đặt

1. **Clone repository:**
```bash
git clone https://github.com/ThuongLuu2603/Googletrends.git
cd Googletrends
```

2. **Tạo môi trường ảo (khuyến nghị):**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Cài đặt dependencies:**
```bash
pip install -r requirements.txt
```

4. **Chạy ứng dụng:**
```bash
streamlit run app.py
```

5. **Mở trình duyệt:**
- Ứng dụng sẽ tự động mở tại: `http://localhost:8501`
- Nếu không tự động mở, truy cập link trên trong trình duyệt

## 📊 Tính năng Dashboard

### 1. Input/Bộ lọc
- **Chọn từ khóa:** Danh sách từ khóa du lịch phổ biến (Đà Nẵng, Phú Quốc, Nha Trang, v.v.)
- **Nhập từ khóa tùy chỉnh:** Cho phép tìm kiếm bất kỳ từ khóa nào
- **Chọn khoảng thời gian:** 7 ngày, 30 ngày, 90 ngày, 6 tháng, 1 năm, hoặc tùy chỉnh

### 2. Visualization

#### 📈 Xu hướng theo Thời gian
- Biểu đồ đường (line chart) hiển thị xu hướng tìm kiếm theo thời gian
- Phân tích riêng cho 3 khu vực: Bắc, Trung, Nam
- Màu sắc phân biệt rõ ràng cho mỗi khu vực
- Thống kê chi tiết: trung bình, tối đa, tối thiểu, độ lệch chuẩn

#### 🗺️ So sánh theo Khu vực (Bắc-Trung-Nam)
- **Biểu đồ cột:** So sánh mức độ quan tâm giữa các khu vực
- **Biểu đồ tròn:** Tỷ lệ phân bố mức độ quan tâm
- **Bản đồ nhiệt (Heatmap):** Xu hướng theo khu vực và thời gian

#### 🔗 Từ khóa Liên quan
- Top 10 từ khóa liên quan với điểm số
- Biểu đồ thanh ngang hiển thị mức độ liên quan
- Danh sách chi tiết với progress bar

#### 💡 Insights & Khuyến nghị
- Khu vực tiềm năng nhất
- Thời điểm cao điểm
- Top từ khóa nổi bật cho SEO
- Xu hướng tăng/giảm gần đây

## 🛠️ Cấu trúc Project

```
Googletrends/
├── app.py                  # Ứng dụng Streamlit chính
├── data_simulation.py      # Module mô phỏng dữ liệu Google Trends
├── requirements.txt        # Dependencies
├── .gitignore             # Git ignore file
└── README.md              # Tài liệu hướng dẫn
```

## 📦 Dependencies

- **streamlit:** Framework để xây dựng web app
- **pandas:** Xử lý và phân tích dữ liệu
- **plotly:** Tạo biểu đồ tương tác
- **numpy:** Tính toán số học

## 🎯 Kỹ thuật Sử dụng

### Module `data_simulation.py`
Cung cấp các hàm mô phỏng dữ liệu Google Trends:

- `generate_trend_data(keyword, start_date, end_date, regions)`: Tạo dữ liệu xu hướng theo thời gian
- `generate_regional_comparison(keyword, date)`: Tạo dữ liệu so sánh khu vực
- `generate_related_keywords(main_keyword)`: Tạo danh sách từ khóa liên quan
- `get_popular_keywords()`: Lấy danh sách từ khóa phổ biến

### Tính năng mô phỏng dữ liệu
- **Seasonal pattern:** Xu hướng du lịch cao vào hè và lễ tết
- **Weekend effect:** Tăng tìm kiếm vào cuối tuần
- **Regional multiplier:** Mỗi khu vực có đặc điểm riêng
- **Realistic noise:** Thêm nhiễu ngẫu nhiên để dữ liệu chân thực

## 📸 Screenshots

Sau khi chạy ứng dụng, bạn sẽ thấy:
- Dashboard với sidebar bộ lọc bên trái
- Các biểu đồ tương tác có thể zoom, pan
- Metrics tổng quan ở đầu trang
- Insights và khuyến nghị ở cuối trang

## 🔧 Tùy chỉnh

### Thêm từ khóa mới
Chỉnh sửa hàm `get_popular_keywords()` trong `data_simulation.py`

### Thêm từ khóa liên quan
Cập nhật `related_keywords_map` trong hàm `generate_related_keywords()`

### Thay đổi giao diện
Chỉnh sửa CSS trong phần `st.markdown()` của `app.py`

## 📝 Ghi chú

- Ứng dụng sử dụng **dữ liệu mô phỏng** để demo
- Để sử dụng dữ liệu thực từ Google Trends, cần tích hợp thêm API `pytrends`
- Dữ liệu được cache để tăng hiệu suất

## 🤝 Đóng góp

Mọi đóng góp đều được chào đón! Vui lòng tạo pull request hoặc mở issue.

## 📄 License

MIT License

## 👥 Tác giả

Phát triển cho Vietravel R&D - Phân tích xu hướng du lịch Việt Nam