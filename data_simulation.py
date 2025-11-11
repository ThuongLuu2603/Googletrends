"""
Module mô phỏng dữ liệu Google Trends cho phân tích du lịch Việt Nam
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


def generate_trend_data(keyword, start_date, end_date, regions=None):
    """
    Tạo dữ liệu mô phỏng xu hướng Google Trends theo thời gian và khu vực
    
    Args:
        keyword (str): Từ khóa tìm kiếm
        start_date (datetime): Ngày bắt đầu
        end_date (datetime): Ngày kết thúc
        regions (list): Danh sách khu vực, mặc định là ['Bắc', 'Trung', 'Nam']
    
    Returns:
        pd.DataFrame: DataFrame chứa dữ liệu xu hướng
    """
    if regions is None:
        regions = ['Bắc', 'Trung', 'Nam']
    
    # Tạo dãy ngày
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    
    data = []
    for region in regions:
        # Tạo xu hướng cơ bản với seasonal pattern
        base_trend = 50
        for date in date_range:
            # Thêm seasonal effect (du lịch cao vào hè và lễ tết)
            seasonal = 20 * np.sin(2 * np.pi * date.dayofyear / 365)
            
            # Thêm weekend effect
            weekend_boost = 10 if date.dayofweek >= 5 else 0
            
            # Thêm regional multiplier
            if region == 'Nam':
                regional_mult = 1.2  # Nam có xu hướng tìm kiếm cao hơn
            elif region == 'Trung':
                regional_mult = 0.9
            else:  # Bắc
                regional_mult = 1.0
            
            # Tạo giá trị cuối cùng với noise
            noise = np.random.normal(0, 5)
            value = max(0, min(100, (base_trend + seasonal + weekend_boost) * regional_mult + noise))
            
            data.append({
                'date': date,
                'keyword': keyword,
                'region': region,
                'value': round(value, 2)
            })
    
    df = pd.DataFrame(data)
    return df


def generate_regional_comparison(keyword, date):
    """
    Tạo dữ liệu so sánh giữa các khu vực cho một ngày cụ thể
    
    Args:
        keyword (str): Từ khóa tìm kiếm
        date (datetime): Ngày cần so sánh
    
    Returns:
        pd.DataFrame: DataFrame chứa dữ liệu so sánh khu vực
    """
    regions = ['Bắc', 'Trung', 'Nam']
    
    # Tạo giá trị mô phỏng cho từng khu vực
    base_values = {
        'Bắc': np.random.uniform(60, 80),
        'Trung': np.random.uniform(50, 70),
        'Nam': np.random.uniform(70, 90)
    }
    
    data = []
    for region in regions:
        data.append({
            'region': region,
            'keyword': keyword,
            'value': round(base_values[region], 2)
        })
    
    df = pd.DataFrame(data)
    return df


def generate_related_keywords(main_keyword):
    """
    Tạo danh sách từ khóa liên quan dựa trên từ khóa chính
    
    Args:
        main_keyword (str): Từ khóa chính
    
    Returns:
        pd.DataFrame: DataFrame chứa từ khóa liên quan và điểm số
    """
    # Danh sách từ khóa du lịch phổ biến tại Việt Nam
    related_keywords_map = {
        'du lịch': [
            ('du lịch hè', 95),
            ('tour du lịch', 88),
            ('du lịch biển', 85),
            ('du lịch miền Trung', 78),
            ('vé máy bay', 75),
            ('khách sạn', 72),
            ('resort', 68),
            ('du lịch Đà Nẵng', 65),
            ('du lịch Phú Quốc', 62),
            ('du lịch Nha Trang', 60)
        ],
        'Đà Nẵng': [
            ('Bà Nà Hills', 92),
            ('Hội An', 88),
            ('Mỹ Khê', 85),
            ('Sơn Trà', 78),
            ('Ngũ Hành Sơn', 75),
            ('cầu Rồng', 72),
            ('bãi biển Đà Nẵng', 70),
            ('khách sạn Đà Nẵng', 68),
            ('tour Đà Nẵng', 65),
            ('vé máy bay Đà Nẵng', 60)
        ],
        'Phú Quốc': [
            ('Vinpearl Phú Quốc', 90),
            ('bãi Sao', 85),
            ('Sunset Sanato', 80),
            ('chợ đêm Phú Quốc', 75),
            ('Grand World', 72),
            ('cáp treo Hòn Thơm', 70),
            ('Safari Phú Quốc', 68),
            ('resort Phú Quốc', 65),
            ('tour Phú Quốc', 62),
            ('vé máy bay Phú Quốc', 58)
        ],
        'Nha Trang': [
            ('Vinpearl Nha Trang', 88),
            ('biển Nha Trang', 85),
            ('bùn khoáng Nha Trang', 80),
            ('Hòn Mun', 75),
            ('VinWonders Nha Trang', 72),
            ('khách sạn Nha Trang', 70),
            ('tour Nha Trang', 68),
            ('Tháp Bà', 65),
            ('Hòn Tằm', 60),
            ('vé máy bay Nha Trang', 55)
        ],
        'Hà Nội': [
            ('phố cổ Hà Nội', 90),
            ('Hồ Gươm', 85),
            ('chùa Một Cột', 78),
            ('Văn Miếu', 75),
            ('Lăng Bác', 72),
            ('bảo tàng Hà Nội', 68),
            ('ẩm thực Hà Nội', 80),
            ('khách sạn Hà Nội', 65),
            ('tour Hà Nội', 62),
            ('vé máy bay Hà Nội', 58)
        ],
        'Sài Gòn': [
            ('Nhà thờ Đức Bà', 88),
            ('Bưu điện Sài Gòn', 85),
            ('Bến Thành', 82),
            ('Bitexco', 78),
            ('Phố đi bộ Nguyễn Huệ', 75),
            ('Địa đạo Củ Chi', 72),
            ('khách sạn Sài Gòn', 70),
            ('ẩm thực Sài Gòn', 85),
            ('tour Sài Gòn', 65),
            ('vé máy bay Sài Gòn', 60)
        ]
    }
    
    # Tìm từ khóa liên quan
    related = None
    for key in related_keywords_map:
        if key.lower() in main_keyword.lower():
            related = related_keywords_map[key]
            break
    
    # Nếu không tìm thấy, sử dụng danh sách mặc định
    if related is None:
        related = related_keywords_map['du lịch']
    
    data = []
    for keyword, score in related:
        data.append({
            'keyword': keyword,
            'score': score
        })
    
    df = pd.DataFrame(data)
    return df


def get_popular_keywords():
    """
    Lấy danh sách các từ khóa phổ biến cho du lịch Việt Nam
    
    Returns:
        list: Danh sách từ khóa phổ biến
    """
    return [
        'du lịch',
        'Đà Nẵng',
        'Phú Quốc',
        'Nha Trang',
        'Hà Nội',
        'Sài Gòn',
        'Hạ Long',
        'Đà Lạt',
        'Hội An',
        'Vũng Tàu'
    ]
