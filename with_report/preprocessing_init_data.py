import streamlit as st
from with_report.load_data import load
from with_report.export_info import get_week_info, get_month_info
from with_report.formatting_init_data import format_media, format_ga, format_history
from with_report.period_filter import filter_by_period
from with_report.arrange_metric import arrange_metric


def filtering_data(media_file, ga_file, history_file, condition_set):
    commerce_or_not = condition_set['commerce_or_not']
    analysis_period = condition_set['analysis_period']
    selected_date = condition_set['selected_date']
    week_start_day = condition_set['week_start_day']

    notice_analysis_period(condition_set)
    
    with st.spinner("데이터 가져오는 중..."):
        original_media_df = load(media_file)
        formatted_media_df = format_media(original_media_df)

        original_ga_df = load(ga_file)
        formatted_ga_df = format_ga(original_ga_df)

        original_history_df = load(history_file)
        formatted_history_df = format_history(original_history_df)

        internal_ch_df, now_media, pre_media = filter_by_period(formatted_media_df, analysis_period, selected_date, week_start_day)
        internal_ga_df, now_ga, pre_ga = filter_by_period(formatted_ga_df, analysis_period, selected_date, week_start_day)
        internal_history_df, now_history, pre_history = filter_by_period(formatted_history_df, analysis_period, selected_date, week_start_day)

        df_set = {'original_media': original_media_df,
                'formatted_media': formatted_media_df,
                'used_media' : internal_ch_df,
                'original_ga': original_ga_df,
                'formatted_ga': formatted_ga_df,
                'used_ga' : internal_ga_df,
                'original_history': original_history_df,
                'formatted_history': formatted_history_df,
                'used_history' : internal_history_df,}

        if (now_media == now_ga) and (now_media == now_history):
            now_period = now_media
        else:
            print('now 기간 추출 문제 있음')
        
        if (pre_media == pre_ga) and (pre_media == pre_history):
            pre_period = pre_media
        else:
            print('pre 기간 추출 문제 있음')
        
        period_set = {
            "now" : now_period,
            "pre" : pre_period
        }
        
        list_inflow, list_trans_media, list_trans_ga = arrange_metric(internal_ch_df, internal_ga_df, commerce_or_not, analysis_period)

        metric_set = {
            'inflow_metric' : list_inflow,
            'trans_metric' : list_trans_media,
            'trans_ga_metric' : list_trans_ga,
        }

        return df_set, period_set, metric_set

def notice_analysis_period(condition_set):
    analysis_period = condition_set['analysis_period']
    selected_date = condition_set['selected_date']
    week_start_day = condition_set['week_start_day']

    if analysis_period == "일간":
        st.write(selected_date, " 을(를) 기준으로 전 일과 비교 분석 합니다.")
    elif analysis_period == "주간":
        st.write(get_week_info(selected_date,week_start_day), " 을(를) 기준으로 전 주와 비교 분석 합니다.")
    else:
        st.write(get_month_info(selected_date), " 을(를) 기준으로 전 월과 비교 분석 합니다.")