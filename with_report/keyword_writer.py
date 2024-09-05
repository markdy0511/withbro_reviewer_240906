from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import streamlit as st
import pandas as pd
from langchain.schema import StrOutputParser
from with_report.grouping import grouped_media_kwrd, grouped_ga_kwrd
from with_report.reporting import report_media, report_ga, report_ga_add
from with_report.rounding import round_col_axis


overview_llm = ChatOpenAI(
    temperature=0.7,
    model = "gpt-4o-mini"
)

def kwrd_ranking_df(media_df, ga_df, metric_set, trans_metric_set, group_period, condition_set):
    grouped_media_df = grouped_media_kwrd(media_df, metric_set, group_period)
    reported_media_df = report_media(grouped_media_df, metric_set, trans_metric_set, condition_set)

    grouped_ga_df = grouped_ga_kwrd(ga_df, metric_set, group_period)
    calculated_ga_df = report_ga(grouped_ga_df, metric_set, trans_metric_set, condition_set)
    reported_ga_df = report_ga_add(reported_media_df, calculated_ga_df, condition_set)
 
    df_combined = pd.concat([reported_media_df, reported_ga_df], axis=1)

    df_combined.reset_index(inplace=True)
    df_combined[['매체','캠페인','광고그룹','소재명/키워드', group_period]] = pd.DataFrame(df_combined['index'].tolist(), index=df_combined.index)
    df_combined.drop(columns=['index'], inplace=True)
    # 특정 열을 앞에 오도록 열 순서 재배치
    columns = ['매체','캠페인','광고그룹','소재명/키워드', group_period] + [col for col in df_combined.columns if  (col != '소재명/키워드') and (col != '매체') and (col != '캠페인') and (col != '광고그룹') and (col != group_period)]
    df_cleaned = df_combined.dropna(subset=['소재명/키워드'])
    df_combined_re = df_cleaned[columns]

    rounded_kwrd_ranking_df = round_col_axis(df_combined_re, 'CTR')

    return rounded_kwrd_ranking_df



def writer(detail_df, ranking_df, sort_columns, sort_orders):
    descript_kwrd_list = []
    for mtrc in sort_columns:
        st.subheader(f'성과 상위 소재명/키워드 by {mtrc}')
        sorted_da_df = detail_df.sort_values(by=mtrc, ascending=sort_orders[mtrc]).head(5)
        st.write(sorted_da_df[['소재명/키워드', mtrc]])
        filter_list = list(sorted_da_df['소재명/키워드'])
        # 선택된 키워드에 대한 데이터 필터링
        filtered_data =  ranking_df[ranking_df['소재명/키워드'].isin(filter_list)]
        st.write(filtered_data)

        kwrd_description = "keywords performance results by " + str(mtrc) + " :\n\n"
        kwrd_description += filtered_data.to_string()


        kwrd_prompt = ChatPromptTemplate.from_template(
                """
                너는 퍼포먼스 마케팅 성과 분석가야.
                다음은 {metric}에 따른 성과가 좋은 키워드에 대한 데이터야.
                \n\n{kwrd_perf}

                {kwrd_list}를 대상으로 {kwrd_perf}를 분석해서
                가장 {metric}이 좋은 매체, 캠페인, 광고그룹, 그것의 {metric} 성과를 출력해.

                한 개의 키워드마다 아래 형태로 출력해줘.
                -----------
                키워드
                ● 매체 : 이름
                ● 캠페인 : 이름
                ● 광고그룹 : 이름
                ● {metric} : 수치

                각 매체별로 한글로 100자 정도로 표현해줘.
                제목은 만들지마.
                출력할 때, 마크다운 만들지마.
                수치 표현할 때는 천 단위에서 쉼표 넣어줘.

            """
            )

        kwrd_chain = kwrd_prompt | overview_llm | StrOutputParser()

        descript_kwrd = kwrd_chain.invoke(
                {"kwrd_list":filter_list,"metric":mtrc,"kwrd_perf":kwrd_description},
            )
        st.markdown(descript_kwrd)
        descript_kwrd_list.append(descript_kwrd)

    return descript_kwrd_list