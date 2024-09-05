import pandas as pd
import streamlit as st

def report_media(df, metric_set, trans_metric_set, condition_set):
    if condition_set["commerce_or_not"] == "비커머스":
        columns_inflow = metric_set["inflow_metric"] + ['CTR','CPC']
        columns_trans = metric_set["trans_metric"] + ['전환수','CPA']
        columns_report = columns_inflow + columns_trans
    else: #커머스
        columns_inflow = metric_set["inflow_metric"] + ['CTR','CPC']
        columns_trans = metric_set["trans_metric"] + ['전환수','객단가','CPA','ROAS','전환율']
        columns_report = columns_inflow + columns_trans

    print(columns_report)
    
    report_df = pd.DataFrame(columns=columns_report)
    report_df = pd.concat([report_df, df])
    
    # ZeroDivisionError 예외 처리
    report_df['CTR'] = report_df.apply(lambda row: (row['클릭수'] / row['노출수'] * 100) if row['노출수'] != 0 else 'NaN', axis=1)
    report_df['CPC'] = report_df.apply(lambda row: (row['총비용'] / row['클릭수']) if row['클릭수'] != 0 else 'NaN', axis=1)
    
    report_df['전환수'] = report_df[trans_metric_set["selected_trans_media"]].sum(axis=1) #report_df['회원가입'] + report_df['DB전환'] + report_df['가망']
    report_df['CPA'] = report_df.apply(lambda row: (row['총비용'] / row['전환수']) if row['전환수'] != 0 else 'NaN', axis=1)
    
    # 데이터 타입 확인 및 변환
    report_df['CTR'] = pd.to_numeric(report_df['CTR'], errors='coerce')
    report_df['CPC'] = pd.to_numeric(report_df['CPC'], errors='coerce')
    report_df['CPA'] = pd.to_numeric(report_df['CPA'], errors='coerce')
    
    #report_df['CTR'] = report_df['CTR'].round(2)
    #report_df['CPC'] = report_df['CPC'].round(0)
    #report_df['CPA'] = report_df['CPA'].round(0)

    if condition_set["commerce_or_not"] == "커머스":
        report_df['객단가'] = report_df.apply(lambda row: (row['구매액'] / row['구매']) if row['구매'] != 0 else 'NaN', axis=1)
        report_df['ROAS'] = report_df.apply(lambda row: (row['구매액'] / row['총비용'] * 100) if row['총비용'] != 0 else 'NaN', axis=1)
        report_df['전환율'] = report_df.apply(lambda row: (row['전환수'] / row['클릭수'] * 100) if row['클릭수'] != 0 else 'NaN', axis=1)

        # 데이터 타입 확인 및 변환
        report_df['객단가'] = pd.to_numeric(report_df['객단가'], errors='coerce')
        report_df['ROAS'] = pd.to_numeric(report_df['ROAS'], errors='coerce')
        report_df['전환율'] = pd.to_numeric(report_df['전환율'], errors='coerce')
    
    return report_df

def report_ga(df, metric_set, trans_metric_set, condition_set):
    if condition_set["commerce_or_not"] == "비커머스":
        columns_trans = metric_set["trans_ga_metric"] + ['전환수','CPA']
    else: #커머스
        columns_trans = metric_set["trans_ga_metric"] + ['전환수','객단가','CPA','ROAS','전환율']
    
    report_df = pd.DataFrame(columns=columns_trans)
    report_df = pd.concat([report_df, df])

    report_df['전환수'] = report_df[trans_metric_set["selected_trans_ga"]].sum(axis=1) #report_df['회원가입'] + report_df['db전환'] + report_df['카톡btn'] + report_df['전화btn']

    if condition_set["commerce_or_not"] == "커머스":
        report_df['객단가'] = report_df.apply(lambda row: (row['구매액'] / row['구매']) if row['구매'] != 0 else 0, axis=1)

        # 데이터 타입 확인 및 변환
        report_df['객단가'] = pd.to_numeric(report_df['객단가'], errors='coerce')

    return report_df

def report_ga_add(media_df, ga_df, condition_set):
    try:
        ga_df['CPA'] = (media_df['총비용'] / ga_df['전환수'])
        ga_df['CPA'] = pd.to_numeric(ga_df['CPA'], errors='coerce')
        #ga_df['CPA'] = ga_df['CPA'].round(0)
    except Exception as e:
        ga_df['CPA'] = 0

    if condition_set["commerce_or_not"] == "커머스":
        try:
            ga_df['ROAS'] = (ga_df['구매액'] / media_df['총비용']) * 100
            ga_df['ROAS'] = pd.to_numeric(ga_df['ROAS'], errors='coerce')
        except Exception as e:
            try:
                ga_df['ROAS'] = 0
            except:
                pass
        
        try:
            ga_df['전환율'] = (ga_df['전환수'] / media_df['클릭수']) * 100
            ga_df['전환율'] = pd.to_numeric(ga_df['전환율'], errors='coerce')
        except Exception as e:
            try:
                ga_df['전환율'] = 0
            except:
                pass

    ga_df.columns = [f'GA_{col}' for col in ga_df.columns]

    return ga_df