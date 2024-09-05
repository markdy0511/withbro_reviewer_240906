import pandas as pd
from datetime import timedelta
from with_report.export_info import get_month_info, get_week_info

def filter_by_period(df, period_type, reference_date, start_of_week):
    #reference_date = pd.to_datetime(reference_date)
    
    if period_type == '일간':
        reference = pd.to_datetime(reference_date, format='%Y-%m-%d')

        filtered_df = df[(df['일자'] >= reference - timedelta(days=1)) & (df['일자'] <= reference)]
        filtered_df['일자'] = filtered_df['일자'].dt.strftime('%Y-%m-%d')
        now = reference.strftime('%Y-%m-%d')
        pre = (reference - timedelta(days=1)).strftime('%Y-%m-%d')
        return filtered_df, now, pre
    
    elif period_type == '주간':
        this_week = get_week_info(reference_date, start_of_week)
        pre_week = get_week_info(reference_date - timedelta(days=7), start_of_week)
        df['주'] = df['일자'].apply(lambda x: get_week_info(x, start_of_week))
        
        filtered_weeks = [pre_week, this_week]
        filtered_df = df[df['주'].isin(filtered_weeks)]
        filtered_df['일자'] = filtered_df['일자'].dt.strftime('%Y-%m-%d')

        now = this_week
        pre = pre_week
        return filtered_df, now, pre

    elif period_type == '월간':
        this_month = get_month_info(reference_date)
        pre_month = this_month - 1
        df['주'] = df['일자'].apply(lambda x: get_week_info(x, start_of_week))
        df['월'] = df['일자'].apply(lambda x: get_month_info(x))

        filtered_months = [pre_month, this_month]
        filtered_df = df[df['월'].isin(filtered_months)]
        filtered_df['일자'] = filtered_df['일자'].dt.strftime('%Y-%m-%d')

        now = this_month
        pre = pre_month
        return filtered_df, now, pre

    else:
        raise ValueError("Invalid period_type. It should be one of ['일간', '주간', '월간']")

