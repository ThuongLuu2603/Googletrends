"""
Module lấy dữ liệu Google Trends thực cho phân tích du lịch Việt Nam.

LƯU Ý: theo yêu cầu, module này KHÔNG cung cấp dữ liệu mô phỏng. Nếu `pytrends`
không được cài hoặc Google Trends không trả dữ liệu, các hàm sẽ raise lỗi rõ ràng.
"""
import logging
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import time
import os
import json

try:
    from pytrends.request import TrendReq
    _PYTRENDS_AVAILABLE = True
except Exception:
    TrendReq = None
    _PYTRENDS_AVAILABLE = False

if _PYTRENDS_AVAILABLE:
    try:
        from pytrends.exceptions import TooManyRequestsError
    except Exception:
        TooManyRequestsError = Exception
else:
    TooManyRequestsError = Exception

logger = logging.getLogger(__name__)

# retry config for pytrends requests
_MAX_RETRIES = 5
_RETRY_BACKOFF = 2  # seconds (exponential backoff base)

def _retry_call(fn, *args, max_retries=_MAX_RETRIES, backoff=_RETRY_BACKOFF, **kwargs):
    """Call fn(*args, **kwargs) with retries on TooManyRequestsError or transient errors.
    Raises last exception if all retries fail.
    """
    last_exc = None
    for attempt in range(1, max_retries + 1):
        try:
            return fn(*args, **kwargs)
        except Exception as e:
            last_exc = e
            # If it's clearly a 4xx/5xx transient error, retry; otherwise raise immediately.
            if isinstance(e, TooManyRequestsError) or '429' in str(e) or attempt < max_retries:
                sleep_time = backoff ** (attempt - 1)
                logger.warning('Transient error on attempt %s/%s: %s — retrying after %ss', attempt, max_retries, e, sleep_time)
                time.sleep(sleep_time)
                continue
            raise
    # exhausted
    raise last_exc


def _get_pytrends():
    """Create a TrendReq instance. If environment variable GOOGLE_TRENDS_PROXY is set,
    it will be used as proxies for requests (either a single URL string or a JSON map).
    """
    if not _PYTRENDS_AVAILABLE:
        raise RuntimeError("pytrends package is required. Please install pytrends and ensure network/proxy setup.")

    requests_args = {}
    proxy_env = os.environ.get('GOOGLE_TRENDS_PROXY')
    if proxy_env:
        try:
            proxies = json.loads(proxy_env)
        except Exception:
            proxies = {'http': proxy_env, 'https': proxy_env}
        requests_args['proxies'] = proxies

    # allow passing requests_args into TrendReq to enable proxies/timeouts
    return TrendReq(hl='vi-VN', tz=7, requests_args=requests_args)

# Mapping đơn giản từ tên tỉnh/thành phổ biến sang 3 vùng lớn: Bắc/Trung/Nam
# Đây là một ánh xạ heuristic để gom các kết quả theo khu vực macro. Nếu tên tỉnh
# không khớp, mặc định sẽ gán vào 'Bắc'.
_PROVINCE_TO_REGION = {
    # Bắc
    'hà nội': 'Bắc', 'hanoi': 'Bắc', 'bắc ninh': 'Bắc', 'bắc giang': 'Bắc', 'hải phòng': 'Bắc',
    'thái bình': 'Bắc', 'nam định': 'Bắc', 'ninh bình': 'Bắc', 'vĩnh phúc': 'Bắc', 'hưng yên': 'Bắc',
    # Trung
    'đà nẵng': 'Trung', 'da nang': 'Trung', 'thanh hóa': 'Trung', 'nghệ an': 'Trung', 'hà tĩnh': 'Trung',
    'quảng bình': 'Trung', 'quảng trị': 'Trung', 'thừa thiên': 'Trung', 'huế': 'Trung', 'quảng nam': 'Trung',
    'quảng ngãi': 'Trung', 'khánh hòa': 'Trung', 'nha trang': 'Trung',
    # Nam
    'hồ chí minh': 'Nam', 'ho chi minh': 'Nam', 'sài gòn': 'Nam', 'saigon': 'Nam', 'bình dương': 'Nam',
    'đồng nai': 'Nam', 'bà rịa': 'Nam', 'vũng tàu': 'Nam', 'kiên giang': 'Nam', 'phú quốc': 'Nam',
    'ninh thuận': 'Nam', 'bình thuận': 'Nam', 'lâm đồng': 'Nam', 'đắk lắk': 'Nam', 'gia lai': 'Nam'
}

def _map_province_to_region(name: str) -> str:
    if not isinstance(name, str):
        return 'Bắc'
    lname = name.lower()
    for key, region in _PROVINCE_TO_REGION.items():
        if key in lname:
            return region
    # fallback heuristic: look for keywords
    if any(k in lname for k in ('hồ', 'ho chi', 'sài', 'saigon', 'hcm')):
        return 'Nam'
    if any(k in lname for k in ('đà', 'da nang', 'đà nẵng', 'huế', 'quảng')):
        return 'Trung'
    return 'Bắc'


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

    if not _PYTRENDS_AVAILABLE:
        raise RuntimeError("pytrends package is required for real data. Please install with `pip install pytrends` and ensure network access to Google Trends.")

    # Normalize inputs
    if not isinstance(start_date, datetime):
        start_date = pd.to_datetime(start_date)
    if not isinstance(end_date, datetime):
        end_date = pd.to_datetime(end_date)

    pytrends = _get_pytrends()
    timeframe = f"{start_date.strftime('%Y-%m-%d')} {end_date.strftime('%Y-%m-%d')}"

    try:
        pytrends.build_payload([keyword], cat=0, timeframe=timeframe, geo='VN', gprop='')
    except Exception as e:
        logger.error('Failed to build pytrends payload: %s', e)
        raise RuntimeError(f'pytrends build_payload failed: {e}')

    try:
        national = _retry_call(pytrends.interest_over_time)
    except Exception as e:
        logger.error('Failed to fetch interest_over_time: %s', e)
        raise RuntimeError(f'Failed to fetch time series from Google Trends: {e}')

    if national is None or national.empty:
        raise RuntimeError('Google Trends returned empty time series for the requested timeframe')

    try:
        by_region = _retry_call(pytrends.interest_by_region, resolution='REGION', inc_low_vol=True, inc_geo_code=False)
    except Exception as e:
        logger.error('Failed to fetch interest_by_region: %s', e)
        raise RuntimeError(f'Failed to fetch regional breakdown from Google Trends: {e}')

    if by_region is None or by_region.empty:
        raise RuntimeError('Google Trends returned empty regional data for the requested timeframe')

    if keyword in by_region.columns:
        region_vals = by_region[keyword].copy()
    else:
        region_vals = by_region.iloc[:, 0].copy()

    mapped = {}
    for prov, val in region_vals.items():
        macro = _map_province_to_region(str(prov))
        mapped.setdefault(macro, []).append(float(val))

    macro_means = {k: (sum(v) / len(v) if v else 0.0) for k, v in mapped.items()}
    for r in regions:
        macro_means.setdefault(r, 0.0)

    total = sum(macro_means.values())
    if total <= 0:
        raise RuntimeError('Regional totals are zero - cannot compute shares')

    macro_share = {k: (v / total) for k, v in macro_means.items()}

    if keyword in national.columns:
        series = national[keyword]
    else:
        series = national.iloc[:, 0]

    rows = []
    for dt, nat_val in series.items():
        date = pd.to_datetime(dt)
        for r in regions:
            val = float(nat_val) * float(macro_share.get(r, 0.0))
            val = max(0.0, min(100.0, val))
            rows.append({'date': date, 'keyword': keyword, 'region': r, 'value': round(val, 2)})

    return pd.DataFrame(rows)


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

    if not _PYTRENDS_AVAILABLE:
        raise RuntimeError("pytrends package is required for real regional comparison. Please install pytrends and ensure network access to Google Trends.")

    if not isinstance(date, datetime):
        date = pd.to_datetime(date)

    pytrends = _get_pytrends()
    timeframe = f"{date.strftime('%Y-%m-%d')} {date.strftime('%Y-%m-%d')}"
    try:
        pytrends.build_payload([keyword], cat=0, timeframe=timeframe, geo='VN', gprop='')
        by_region = _retry_call(pytrends.interest_by_region, resolution='REGION', inc_low_vol=True, inc_geo_code=False)
    except Exception as e:
        logger.error('Failed to fetch regional comparison: %s', e)
        raise RuntimeError(f'Failed to fetch regional comparison from Google Trends: {e}')

    if by_region is None or by_region.empty:
        raise RuntimeError('Google Trends returned empty regional data for the requested date')

    if keyword in by_region.columns:
        col = by_region[keyword]
    else:
        col = by_region.iloc[:, 0]

    mapped = {}
    for prov, val in col.items():
        macro = _map_province_to_region(str(prov))
        mapped.setdefault(macro, []).append(float(val))

    base_values = {r: (sum(mapped.get(r, [])) / max(1, len(mapped.get(r, [])))) for r in regions}
    data = [{'region': r, 'keyword': keyword, 'value': round(base_values.get(r, 0.0), 2)} for r in regions]
    return pd.DataFrame(data)


def generate_related_keywords(main_keyword):
    """
    Tạo danh sách từ khóa liên quan dựa trên từ khóa chính
    
    Args:
        main_keyword (str): Từ khóa chính
    
    Returns:
        pd.DataFrame: DataFrame chứa từ khóa liên quan và điểm số
    """
    if not _PYTRENDS_AVAILABLE:
        raise RuntimeError('pytrends package is required to fetch related keywords. Please install pytrends and ensure network access to Google Trends.')

    pytrends = _get_pytrends()
    try:
        pytrends.build_payload([main_keyword], timeframe='today 12-m', geo='VN')
        related = _retry_call(pytrends.related_queries)
    except Exception as e:
        logger.error('Failed to fetch related queries: %s', e)
        raise RuntimeError(f'Failed to fetch related queries from Google Trends: {e}')

    if not related or main_keyword not in related or related[main_keyword]['top'] is None:
        raise RuntimeError('Google Trends did not return related queries for the given keyword')

    top_df = related[main_keyword]['top'].copy().head(10)
    rows = []
    for _, r in top_df.iterrows():
        q = r.get('query') or r.get('keyword')
        score = int(r.get('value', 0))
        rows.append({'keyword': q, 'score': score})
    return pd.DataFrame(rows)


def get_popular_keywords():
    """
    Lấy danh sách các từ khóa phổ biến cho du lịch Việt Nam
    
    Returns:
        list: Danh sách từ khóa phổ biến
    """
    if not _PYTRENDS_AVAILABLE:
        raise RuntimeError('pytrends package is required to fetch popular keywords. Please install pytrends and ensure network access to Google Trends.')

    pytrends = _get_pytrends()
    try:
        trends = _retry_call(pytrends.trending_searches, pn='vietnam')
    except Exception as e:
        logger.error('Failed to fetch trending searches: %s', e)
        raise RuntimeError(f'Failed to fetch trending searches from Google Trends: {e}')

    if trends is None or trends.empty:
        raise RuntimeError('Google Trends returned no trending searches for Vietnam')

    return trends[0].astype(str).head(20).tolist()
