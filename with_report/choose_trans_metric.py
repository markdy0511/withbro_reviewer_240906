import streamlit as st

def create_form(metric_set):
    filtered_trans_list = [item for item in metric_set["trans_metric"] if "구매액" not in item]
    filtered_ga_trans_list = [item for item in metric_set["trans_ga_metric"] if "구매액" not in item]

    with st.form(key='metric_select_form'):
        selected_trans_media = st.multiselect("매체 데이터에서 전환의 총합으로 사용될 지표들을 선택해주세요.", filtered_trans_list)
        selected_trans_ga = st.multiselect("GA 데이터에서 전환의 총합으로 사용될 지표들을 선택해주세요.", filtered_ga_trans_list)
        # 조건 버튼 입력
        submit_trans = st.form_submit_button(label='설정 완료')
        if submit_trans:
            return {'selected_trans_media': selected_trans_media, 'selected_trans_ga': selected_trans_ga}
        
def display_form(metric_set, trans_metric_set):
    filtered_trans_list = [item for item in metric_set["trans_metric"] if "구매액" not in item]
    filtered_ga_trans_list = [item for item in metric_set["trans_ga_metric"] if "구매액" not in item]
    with st.form(key='metric_select_form'):
        default_values_1 = trans_metric_set["selected_trans_media"]
        selected_trans_media = st.multiselect("매체 데이터에서 전환의 총합으로 사용될 지표들을 선택해주세요.", filtered_trans_list, default=default_values_1)
        default_values_2 = trans_metric_set["selected_trans_ga"]
        selected_trans_ga = st.multiselect("GA 데이터에서 전환의 총합으로 사용될 지표들을 선택해주세요.", filtered_ga_trans_list, default=default_values_2)
        # 조건 버튼 입력
        submit_trans = st.form_submit_button(label='설정 완료')
        
        return {'selected_trans_media': selected_trans_media, 'selected_trans_ga': selected_trans_ga}

        if submit_trans:
            return {'selected_trans_media': selected_trans_media, 'selected_trans_ga': selected_trans_ga}