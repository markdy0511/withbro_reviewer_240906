# 지표 추출
def arrange_metric(df1, df2, commerce_or_not, analysis_period):
    if "소재구분" in df1.columns.tolist() or "소재종류" in df1.columns.tolist(): #commerce_or_not == "비커머스":
        if analysis_period == "일간":
            exclude_column = ["일자", "캠페인", "광고그룹", "소재명/키워드", "디바이스", "매체", "소재구분", "소재종류", "광고유형"]
        elif analysis_period == "주간":
            exclude_column = ["일자", "캠페인", "광고그룹", "소재명/키워드", "디바이스", "매체", "소재구분", "소재종류", "광고유형","주"]
        else:
            exclude_column = ["일자", "캠페인", "광고그룹", "소재명/키워드", "디바이스", "매체", "소재구분", "소재종류", "광고유형","주","월"]
    else: #커머스
        if analysis_period == "일간":
            exclude_column = ["일자", "캠페인", "광고그룹", "소재명/키워드", "디바이스", "매체", "광고유형"]
        elif analysis_period == "주간":
            exclude_column = ["일자", "캠페인", "광고그룹", "소재명/키워드", "디바이스", "매체", "광고유형","주"]
        else:
            exclude_column = ["일자", "캠페인", "광고그룹", "소재명/키워드", "디바이스", "매체", "광고유형","주","월"]

    # 특정 열을 제외한 나머지 열을 리스트로 변환
    list_media = df1.drop(columns=exclude_column).columns.tolist()
    list_ga = df2.drop(columns=exclude_column).columns.tolist()
    
    # 매체 데이터의 유입, 전환 지표 분리
    list_inflow = [item for item in list_media if item in ["노출수","클릭수","총비용"]]
    list_trans_media = [item for item in list_media if item not in ["노출수","클릭수","총비용"]]
    
    return list_inflow, list_trans_media, list_ga