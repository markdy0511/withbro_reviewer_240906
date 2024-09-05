import pandas as pd

# 2. NaN 값을 제외하고, 문자열 또는 숫자형 데이터만 처리
def process_value(x):
    if pd.isna(x):
        return x  # NaN은 그대로 유지
    elif isinstance(x, (str, int, float)):  # 문자열, 정수, 실수형 데이터 처리
        return str(x).strip()
    else:
        return x  # 그 외 자료형(예: 리스트, 딕셔너리 등)은 그대로 유지


def format_media(df):
    # 날짜 형식 통일
    df['일자'] = pd.to_datetime(df['일자'], format='%Y-%m-%d')

    # 객체형 데이터 통일
    object_columns = ['캠페인', '광고그룹', '소재명/키워드', '디바이스', '매체', '소재구분', '소재종류', '광고유형']
    for col in object_columns:
        try: #비커머스와 커머스 열 항목 다른 점
            df[col] = df[col].apply(process_value)
        except:
            pass
    
    # 정수형 데이터 통일
    int_columns = ['노출수', '클릭수', '총비용']
    for col in int_columns:
        # 1. NaN 값을 0으로 채우기
        df[col] = df[col].fillna(0)
        
        # 2. 문자열 등을 숫자로 변환, 변환 불가능한 값은 NaN으로 처리
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
        # 3. 소수점이 있는 값은 반올림하여 정수로 변환
        df[col] = df[col].round().astype('int64')
        #df[col] = df[col].astype('int')
    
    # 전환지표 int64로 변환할 열 자동 추출
    excluded_columns = ['일자'] + object_columns + int_columns
    trans_columns = [col for col in df.columns if col not in excluded_columns]

    # 전환지표 int64로 변환
    for col in trans_columns:
        # 1. NaN 값을 0으로 채우기
        df[col] = df[col].fillna(0)
        
        # 2. 문자열 등을 숫자로 변환, 변환 불가능한 값은 NaN으로 처리
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
        # 3. 소수점이 있는 값은 반올림하여 정수로 변환
        df[col] = df[col].round().astype('int64')
    
    return df

def format_ga(df):
    # 날짜 형식 통일
    df['일자'] = pd.to_datetime(df['일자'], format='%Y-%m-%d')

    # 객체형 데이터 통일
    object_columns = ['캠페인', '광고그룹', '소재명/키워드', '디바이스', '매체', '소재구분', '소재종류', '광고유형']
    for col in object_columns:
        try: #비커머스와 커머스 열 항목 다른 점
            df[col] = df[col].apply(process_value)
        except:
            pass
    
    # 전환지표 int64로 변환할 열 자동 추출
    excluded_columns = ['일자'] + object_columns
    trans_columns = [col for col in df.columns if col not in excluded_columns]

    # 전환지표 int64로 변환
    for col in trans_columns:
        # 1. NaN 값을 0으로 채우기
        df[col] = df[col].fillna(0)
        
        # 2. 문자열 등을 숫자로 변환, 변환 불가능한 값은 NaN으로 처리
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
        # 3. 소수점이 있는 값은 반올림하여 정수로 변환
        df[col] = df[col].round().astype('int64')
    
    return df

def format_history(df):
    # 날짜 형식 통일
    df['일자'] = pd.to_datetime(df['일자'], format='%Y-%m-%d')

    # 객체형 데이터 통일
    object_columns = ['운영 히스토리', '매체']
    for col in object_columns:
        try:
            df[col] = df[col].apply(process_value)
        except:
            pass
    
    return df