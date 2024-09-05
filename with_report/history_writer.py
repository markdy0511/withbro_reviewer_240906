from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import streamlit as st
from langchain.schema import StrOutputParser
import pandas as pd


strict_llm = ChatOpenAI(
    temperature=0.1,
    model = "gpt-4o-mini"
)


def writer(history_df, group_period, period):
    period_data = history_df[history_df[group_period] == period]
   
    history_set = {}
    for index, row in period_data.iterrows():
        if row['매체'] not in history_set.keys():
            history_set[row['매체']] = [[row[group_period], row['운영 히스토리']]]
        else:
            history_set[row['매체']].append([row[group_period], row['운영 히스토리']])

    history_prompt = ChatPromptTemplate.from_template(
                """
                너는 퍼포먼스 마케팅 성과 분석가야.
                주어진 운영 히스토리로 인해 성과에 확인해야 하는 것이 무엇인지 안내해줘.

                다음은 운영 히스토리 데이터야.
                \n\n{history}
                
                그리고 매체에 대한 정보가 없으면 확인할 특별 사항이 없다고 해줘.
                매체 정보가 있는 경우 확인해야 할 가능성이 높아져.
                하지만, 운영 히스토리에 정산, 세금, 트리거 수정, 중복 호출, 전달, 검수, 테스트 관련 이야기는 마케팅 성과랑 관련 없어.
                마케팅 성광에 유의미한 운영 히스토리가 있는 경우에 매체를 언급하면서, 유입 성과와 전환 성과 관점에서 안내해줘.

                한글로 50자 정도로 표현해줘.
                존댓말을 써야 해.
            """
        )
    history_chain = history_prompt | strict_llm | StrOutputParser()

    for key, his_list in history_set.items():
        st.subheader(key)
        for ep in his_list:
            st.write("● " + ep[1])
    history_description = "history :\n\n"
    history_description += period_data.to_string()
    descript_his = history_chain.invoke(
                {"history":history_description,},
    )

    return descript_his
