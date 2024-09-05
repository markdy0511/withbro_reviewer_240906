import streamlit as st
from datetime import datetime

def create_form():
    with st.form(key='condition_form'):
        # Include ROAS analysis
        commerce_or_not = st.radio(
            "광고주가 커머스 분야인가요? 아니면 비커머스 분야인가요? (필수)",
            ("커머스", "비커머스")
        )

        # Select analysis period
        analysis_period = st.radio(
            "분석할 기간을 선택하세요 (필수)",
            ("일간", "주간", "월간")
        )
        selected_date = st.date_input(
            "분석 시작 날짜를 선택해주세요. 주간, 월간일 경우 포함 날짜 아무 일이나 선택해주세요. (필수)",
            datetime.today(), key="selected_date"
        )

        week_start_day = st.radio(
            "주의 시작 요일을 선택하세요. 주간 분석을 하지 않을 경우 아무것이나 선택해도 됩니다. (선택)",
                ("월요일", "일요일")
            )

        # 조건 버튼 입력
        submit_condition = st.form_submit_button(label='설정 완료')

        if submit_condition:
            return {'commerce_or_not': commerce_or_not, 'analysis_period': analysis_period, 'selected_date':selected_date, 'week_start_day':week_start_day}

        
def display_form(condition_set):
    with st.form(key='condition_form'):
        # Include ROAS analysis
        option_1 = ["커머스", "비커머스"]
        initial_selection_1 = condition_set["commerce_or_not"]
        initial_index_1 = option_1.index(initial_selection_1)

        commerce_or_not = st.radio(
            "광고주가 커머스 분야인가요? 아니면 비커머스 분야인가요? (필수)",
            ("커머스", "비커머스"), index=initial_index_1
        )

        option_2 = ["일간", "주간", "월간"]
        initial_selection_2 = condition_set["analysis_period"]
        initial_index_2 = option_2.index(initial_selection_2)
        # Select analysis period
        analysis_period = st.radio(
            "분석할 기간을 선택하세요 (필수)",
            ("일간", "주간", "월간"), index=initial_index_2
        )

        initial_date = condition_set["selected_date"]
        selected_date = st.date_input(
            "분석 시작 날짜를 선택해주세요. 주간, 월간일 경우 포함 날짜 아무 일이나 선택해주세요. (필수)",
            key="selected_date", value=initial_date
        )


        option_4 = ["월요일", "일요일"]
        initial_selection_4 = condition_set["week_start_day"]
        initial_index_4 = option_4.index(initial_selection_4)
        week_start_day = st.radio(
            "주의 시작 요일을 선택하세요. 주간 분석을 하지 않을 경우 아무것이나 선택해도 됩니다. (선택)",
                ("월요일", "일요일"), index=initial_index_4
            )

        # 조건 버튼 입력
        submit_condition = st.form_submit_button(label='설정 완료')

        return {'commerce_or_not': commerce_or_not, 'analysis_period': analysis_period, 'selected_date':selected_date, 'week_start_day':week_start_day}

        if submit_condition:
            return {'commerce_or_not': commerce_or_not, 'analysis_period': analysis_period, 'selected_date':selected_date, 'week_start_day':week_start_day}