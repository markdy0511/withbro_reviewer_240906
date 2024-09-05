from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import streamlit as st
import pandas as pd
from langchain.schema import StrOutputParser
from with_report.grouping import grouped_media, grouped_ga
from with_report.reporting import report_media, report_ga, report_ga_add
from with_report.diff import comparing_df
from with_report.rounding import round_two_axis, round_multi_axis

overview_llm = ChatOpenAI(
    temperature=0.7,
    model = "gpt-4o-mini"
)

def overview_df(media_df, ga_df, metric_set, trans_metric_set, group_period, condition_set, period_set):
    grouped_media_df = grouped_media(media_df, metric_set, group_period)
    reported_media_df = report_media(grouped_media_df, metric_set, trans_metric_set, condition_set)

    grouped_ga_df = grouped_ga(ga_df, metric_set, group_period)
    calculated_ga_df = report_ga(grouped_ga_df, metric_set, trans_metric_set, condition_set)
    reported_ga_df = report_ga_add(reported_media_df, calculated_ga_df, condition_set)
 
    df_combined = pd.concat([reported_media_df, reported_ga_df], axis=1)
    overview_df = comparing_df(df_combined, period_set)

    if condition_set["commerce_or_not"] == '비커머스':
        rounded_overview_df = round_two_axis(overview_df, '증감율', 'CTR', period_set)
    else:
        rounded_overview_df = round_multi_axis(overview_df,  '증감율', ['CTR','ROAS','전환율','GA_ROAS','GA_전환율'], period_set)

    return rounded_overview_df

def writer(rounded_overview_df):
    description = "Periodical change data results:\n\n"
    description += rounded_overview_df.to_string()
    print(description)
    sentences = []
    if len(rounded_overview_df) == 1:
        sentences = ["비교할 수 있는 기간이 없습니다."]
    else:
        previous_period = rounded_overview_df.iloc[0]
        current_period = rounded_overview_df.iloc[1]
        change_period = rounded_overview_df.iloc[2]
        columns = rounded_overview_df.columns[1:]

        # Generating the sentences
        for col in columns:
            change = "증가" if change_period[col] > 0 else "감소"
            sentence = f"{col}은 지난 기간 대비 {abs(change_period[col]):,.2f} {change}하였습니다. ({previous_period[col]:,.2f} -> {current_period[col]:,.2f})"
            sentences.append(sentence)

    month_compare_prompt = ChatPromptTemplate.from_messages([
        'system',
        """
        너는 퍼포먼스 마케팅 성과 분석가야.
        다음 주차에 따른 성과 자료를 기반으로 유입 성과와 전환 성과를 분석해야해.

        노출수, 클릭수, CTR, CPC, 총비용은 유입에 대한 성과야.
        회원가입, DB전환, 가망, 전환수, CPA는 매체 전환에 대한 성과야.
        GA_회원가입, GA_db전환, GA_카톡btn, GA_전화btn, GA_총합계, GA_CPA는 GA 전환에 대한 성과야.

        절대값의 크기, 변화의 크기가 의미있는 것 위주로 정리해줘.
        변화가 크지 않았다면 유지되었다고 이야기하면 돼.

        숫자를 사용할 때는 지난 기간의 절대값과 이번 기간의 절대값을 모두 표시해줘. 예시. 절대값(지난 기간 -> 이번 기간, 00%)
        1% 이상의 변화가 있을 때는 유지된 것이 아닌, 어떤 이유로 증가되었는지 또는 감소되었는지를 분석해야해.
        비용의 증가는 노출수, 클릭수, 전환수의 증가를 기대해.
        비용의 증가는 노출수, 클릭수, 전환수의 증가를 기대하는 것 잊지마.
        증감율이 양수면 증가, 음수면 감소야.

        다음과 같은 양식으로 정리해줘. 존댓말 써.

        '''list:
        [[
        전체 요약 : 지난 기간 대비 변화 언급 /s/s
        유입 성과 : 지난 기간 대비 변화 언급 /s/s
        매체 전환 성과 : 지난 기간 대비 변화 언급 /s/s
        GA 전환 성과 :  지난 기간 대비 변화 언급 /s/s
        총평 : 긍정적인 요소와 앞으로 바꾸면 좋을 방향성 제시 /s/s
        ]]
        '''


        유입 성과는 CTR과 CPC가 얼마나 변하였고, 그에 대한 근거로 노출수와 클릭수, 비용이 어떻게 변화했기에 CTR과 CPC가 그러한 변화를 가지게 되었는지 분석해야해.
        전환 성과는 전환수가 얼마나 변하였고, CPA가 얼마나 변하였는지를 파악하고, 그에 대한 근거로 노출수, 클릭수, 비용, 회원가입, DB전환, 가망에서의 변화를 분석해야해.
        매체 전환과 GA 전환을 구분해서 설명해야해.

        분석 결과를 양식과 같이 5줄로 출력해줘.
        완벽한 인과관계를 설명하면 너에게 보상을 줄게.

        데이터에서 잘못읽으면 패널티가 있어.
    
        let's go!

        Context :
        \n\n{description}
        \n\n{sentences}
    """,]
    )

    comparison_month_chain = month_compare_prompt | overview_llm | StrOutputParser()
    descript = comparison_month_chain.invoke(
            {"description": description,"sentences":sentences},
        )
    
    descript_result = descript.replace("'''","").replace("[[","").replace("]]","").replace("list:","").replace("\n\n","").split("/s/s")

    return descript_result