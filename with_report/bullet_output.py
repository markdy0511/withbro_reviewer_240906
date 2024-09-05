import streamlit as st

def print_bullet(statement):
    #sentences = statement.split('.\n')
    #bullet_list = "<ul>" + "".join(f"<li>{sentence}</li>" for sentence in statement if sentence) + "</ul>"
    bullet_list = "<ul>" + "".join(f"<li>{sentence}</li>" if not sentence.endswith('.') else f"<li>{sentence}</li>" for sentence in statement if sentence) + "</ul>"
    st.markdown(bullet_list, unsafe_allow_html=True)

    return None