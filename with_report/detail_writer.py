from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import streamlit as st
from langchain.schema import StrOutputParser

overview_llm = ChatOpenAI(
    temperature=0.7,
    model = "gpt-4o-mini"
)


def choose_metric(metric, i):
    with st.form(key='sort_form_br_'+str(i)):
        sort_columns = st.multiselect('가장 먼저 정렬하고 싶은 순서대로 정렬할 기준을 선택하세요 (여러 개 선택 가능):', metric)
        
        # 폼 제출 버튼
        submit_button = st.form_submit_button(label='정렬 적용')

    return submit_button, sort_columns

def generate_statements(df, now_ch_cmp_week, metrics, top_num):
    statements = []
        # Statements for sum metrics

    metrics = [element for element in metrics if (element != '총비용') and (element != '전환수')]
    for metric in metrics:
        if metric in ['CPA', 'CPC', 'CTR', 'GA_CPA']:
            if metric == 'CPA' or metric == 'GA_CPA':
                top_10_cost = df['총비용'].sum()
                top_10_acquisitions = df['전환수'].sum()
                total_cost = now_ch_cmp_week['총비용']
                total_acquisitions = now_ch_cmp_week['전환수']
                top_10_metric = top_10_cost / top_10_acquisitions if top_10_acquisitions != 0 else 0
                total_metric = total_cost / total_acquisitions if total_acquisitions != 0 else 0
            elif metric == 'CPC':
                top_10_cost = df['총비용'].sum()
                top_10_clicks = df['클릭수'].sum()
                total_cost = now_ch_cmp_week['총비용']
                total_clicks = now_ch_cmp_week['클릭수']
                top_10_metric = top_10_cost / top_10_clicks if top_10_clicks != 0 else 0
                total_metric = total_cost / total_clicks if total_clicks != 0 else 0
            elif metric == 'CTR':
                top_10_clicks = df['클릭수'].sum()
                top_10_impressions = df['노출수'].sum()
                total_clicks = now_ch_cmp_week['클릭수']
                total_impressions = now_ch_cmp_week['노출수']
                top_10_metric = (top_10_clicks / top_10_impressions) * 100 if top_10_impressions != 0 else 0
                total_metric = (total_clicks / total_impressions) * 100 if total_impressions != 0 else 0

            ratio = round((top_10_metric - total_metric),2)
            statement = f"정렬된 상위 {top_num}개의 {metric} ({top_10_metric:.2f})는 당 기간 전체 {metric} ({total_metric:.2f})보다 {ratio}만큼 차이가 있습니다."
            statements.append(statement)
        else:
            top_10_sum = df[metric].sum()
            total_sum = now_ch_cmp_week[metric]
            ratio = round((top_10_sum / total_sum) * 100, 2)
            statement = f"정렬된 상위 {top_num}개의 {metric} ({top_10_sum:,})는 당 기간 전체 {metric} ({total_sum:,})의 {ratio}% 입니다."
            statements.append(statement)

    return statements

def display_top(sort_columns, sort_orders, detail_df, overview_df):
    ascending_orders = [sort_orders[col] for col in sort_columns]
    filtered_overview_df = overview_df.iloc[1]
    # 데이터 프레임 정렬
    num_data = len(detail_df)
    if num_data >= 10:
        sorted_df = detail_df.sort_values(by=sort_columns, ascending=ascending_orders).head(10)
    else:
        sorted_df = detail_df.sort_values(by=sort_columns, ascending=ascending_orders).head(num_data)

    top_num = len(sorted_df)
    br_statements = generate_statements(sorted_df, filtered_overview_df, sort_columns, top_num)

    # 값 컬럼을 기준으로 내림차순 정렬 후 상위 10개의 합 계산
    top_10_cost_sum = sorted_df['총비용'].sum()
    total_cost_sum = filtered_overview_df['총비용']
    ratio_cost = round((top_10_cost_sum / total_cost_sum) * 100, 2)

    top_10_cv_sum = sorted_df['전환수'].sum()
    total_cv_sum = filtered_overview_df['전환수']
    ratio_cv = round((top_10_cv_sum / total_cv_sum) * 100, 2)

    cost_statement = "정렬된 상위 " +str(top_num) + " 개의 총비용("+"{:,}".format(top_10_cost_sum)+")"+ "은 당 기간 전체 집행 비용("+"{:,}".format(total_cost_sum)+")의 "+str(ratio_cost)+"% 입니다."
    cv_statement = "정렬된 상위 " +str(top_num) + " 개의 전환수("+"{:,}".format(top_10_cv_sum)+")는 당 기간 전체 전환수("+"{:,}".format(total_cv_sum)+")의 "+str(ratio_cv)+"% 입니다."

    br_statements.insert(0,cv_statement)
    br_statements.insert(0,cost_statement)    

    return sorted_df, top_num, br_statements

def writer(top_num, detail_df, sort_columns):
    metric_str = 'and'.join(str(x) for x in sort_columns)
    br_description = "Top " +str(top_num) + " branches sorted by " + metric_str + ":\n\n"
    br_description += detail_df.to_string()

    br_prompt = ChatPromptTemplate.from_messages([
        'system',
        """
        너는 퍼포먼스 마케팅 성과 분석가야.
        각 소재종류의 성과를 요약해야해.

        유입 성과는 CTR과 CPC가 얼마나 변하였고, 그에 대한 근거로 노출수와 클릭수, 비용이 어떻게 변화했기에 CTR과 CPC가 그러한 변화를 가지게 되었는지 분석해야해.
        전환 성과는 전환수가 얼마나 변하였고, CPA가 얼마나 변하였는지를 파악하고, 그에 대한 근거로 노출수, 클릭수, 비용, 회원가입, DB전환, 가망에서의 변화를 분석해야해.
        매체 전환과 GA 전환을 구분해서 설명해야해.

        완벽한 인과관계를 설명하면 너에게 보상을 줄게.
        종합 분석을 항상 먼저 알려줘.

        데이터에서 잘못읽으면 패널티가 있어.
    
        let's go!

        Context :
        상위 {n}개의 분과구분에 대한 성과 데이터야.
        \n\n{br_per}
    """,]
    )

    br_chain = br_prompt | overview_llm | StrOutputParser()
    with st.status("분과구분별 분석...") as status:
        descript_br_d = br_chain.invoke(
            {"n":top_num,
            "br_per":br_description},
        )

    return descript_br_d