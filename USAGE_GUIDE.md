# Hướng dẫn Sử dụng Chi tiết

## Giới thiệu
Dashboard Google Trends này giúp phân tích xu hướng du lịch tại Việt Nam theo 3 khu vực: Bắc, Trung, Nam.

## Các Bước Sử dụng

### 1. Khởi động Ứng dụng
```bash
streamlit run app.py
```

### 2. Sử dụng Bộ lọc

#### Chọn Từ khóa
- **Từ khóa có sẵn**: Chọn từ dropdown (du lịch, Đà Nẵng, Phú Quốc, Nha Trang, v.v.)
- **Từ khóa tùy chỉnh**: Nhập bất kỳ từ khóa nào vào ô "Hoặc nhập từ khóa tùy chỉnh"

#### Chọn Khoảng thời gian
- **Khoảng có sẵn**: 7 ngày, 30 ngày, 90 ngày, 6 tháng, 1 năm
- **Tùy chỉnh**: Chọn ngày bắt đầu và kết thúc cụ thể

### 3. Đọc hiểu Biểu đồ

#### 📊 Tổng quan
- Hiển thị 4 metrics chính
- So sánh nhanh giữa các khu vực

#### 📈 Xu hướng Tìm kiếm theo Thời gian
- **Line chart**: Theo dõi biến động theo ngày
- **Tương tác**: Hover để xem chi tiết, zoom in/out
- **Xem thống kê**: Click "Xem thống kê chi tiết" để xem bảng số liệu

#### 🗺️ So sánh theo Khu vực
- **Bar chart**: So sánh trực quan giữa 3 khu vực
- **Pie chart**: Xem tỷ lệ phần trăm
- **Heatmap**: Phân tích xu hướng theo thời gian và khu vực

#### 🔗 Từ khóa Liên quan
- Top 10 từ khóa được sắp xếp theo điểm số
- Sử dụng để tối ưu SEO và chiến lược marketing

#### 💡 Insights & Khuyến nghị
- Tự động phân tích và đưa ra gợi ý
- Xác định khu vực tiềm năng
- Tìm thời điểm cao điểm

## Tính năng Nâng cao

### Tải xuống Biểu đồ
- Click icon 📷 ở góc phải trên mỗi biểu đồ
- Lưu dưới dạng PNG

### Zoom và Pan
- Sử dụng các nút zoom trên biểu đồ
- Kéo thả để di chuyển

### Fullscreen
- Click nút fullscreen để xem biểu đồ toàn màn hình

## Ví dụ Phân tích

### Phân tích Điểm đến Du lịch
1. Chọn từ khóa: "Đà Nẵng"
2. Chọn thời gian: "6 tháng qua"
3. Quan sát:
   - Khu vực nào quan tâm nhiều nhất?
   - Xu hướng tăng hay giảm?
   - Từ khóa liên quan là gì?

### So sánh Nhiều Điểm đến
1. Phân tích "Phú Quốc" - ghi chú kết quả
2. Phân tích "Nha Trang" - ghi chú kết quả
3. So sánh insights giữa hai điểm đến

## Tips & Tricks

### Tối ưu Hiệu suất
- Dữ liệu được cache tự động
- Chọn khoảng thời gian phù hợp với mục đích phân tích

### Phân tích Hiệu quả
- Kết hợp nhiều khoảng thời gian để thấy xu hướng dài hạn
- Sử dụng từ khóa liên quan để mở rộng nghiên cứu
- Lưu ý các spike trong dữ liệu (sự kiện đặc biệt, lễ hội)

### Xuất Báo cáo
- Chụp màn hình dashboard
- Tải các biểu đồ dạng PNG
- Ghi chú insights từ phần "💡 Insights & Khuyến nghị"

## Câu hỏi Thường gặp (FAQ)

**Q: Dữ liệu có thực không?**
A: Ứng dụng này sử dụng dữ liệu thực từ Google Trends qua `pytrends` (nếu môi trường được cấu hình và có kết nối).
   LƯU Ý: Google có thể rate-limit (HTTP 429) nếu nhiều request cùng lúc hoặc IP bị chặn. Nếu gặp lỗi 429, hãy thử một trong các cách sau:
   - Chạy ứng dụng trên máy cá nhân (IP mới) thay vì môi trường CI/container.
   - Sử dụng proxy: đặt biến môi trường `GOOGLE_TRENDS_PROXY` với giá trị là một URL proxy (ví dụ `http://user:pass@host:port`) hoặc một JSON object map cho `http`/`https` (ví dụ `{"http": "http://...", "https": "http://..."}`).
   - Giảm tốc độ gọi (thêm delays) hoặc phân tán yêu cầu.

**Q: Làm sao thêm từ khóa mới?**
A: Chỉnh sửa hàm `get_popular_keywords()` trong file `data_simulation.py`.

**Q: Dashboard có hoạt động offline không?**
A: Có, chỉ cần Python và các dependencies đã cài đặt.

**Q: Có thể xuất dữ liệu sang Excel không?**
A: Hiện tại chưa có tính năng này. Có thể thêm bằng cách sử dụng `to_excel()` của pandas.

## Hỗ trợ

Nếu gặp vấn đề:
1. Kiểm tra tất cả dependencies đã được cài đặt
2. Xem lại README.md
3. Mở issue trên GitHub
