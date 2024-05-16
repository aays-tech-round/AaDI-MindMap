import streamlit as st
from utils import vanna_aays as va
from streamlit_feedback import streamlit_feedback
import pandas as pd
import mindmap.chart_data as cd
import plotly.graph_objects as go
from mindmap import (
    chart_data as cd,
    quesmap as qm,
    bot_data as bd
)

sidebar_style = """
<style>
[data-testid="stSidebarContent"]{
    background: linear-gradient(45deg, #c4f5f4, rgb(255 241 253));
}
[data-testid="stImage"]{
max-width: 75%;
}
[data-testid="baseButton-secondary"]{
    background: linear-gradient(45deg, #fce6ff, transparent);
}
</style>
"""
st.markdown(sidebar_style, unsafe_allow_html=True)


# Bot reply allignment
st.markdown(
    """
<style>
    [class="stChatMessage st-emotion-cache-1c7y2kd eeusbqq4"]{
        flex-direction: row-reverse;
        text-align: right;
    }
</style>
""",
    unsafe_allow_html=True,
)

gradient_text_html = """
<style>
.gradient-text {
    font-weight: bold;
    background: -webkit-linear-gradient(left, blue, black);
    background: linear-gradient(to right, blue, black);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    display: inline;
    font-size: 3em;
}
</style>
<div class="gradient-text">AaDI</div>
"""

st.markdown(gradient_text_html, unsafe_allow_html=True)
st.caption("Talk your way through data")

st.sidebar.image('logo.png')

with open("ui/sidebar.md", "r") as sidebar_file:
    sidebar_content = sidebar_file.read()

with open("ui/style.md", "r") as styles_file:
    styles_content = styles_file.read()

st.sidebar.markdown(sidebar_content)


st.write(styles_content, unsafe_allow_html=True)

if 'model' not in st.session_state:
    st.session_state['model'] = 'gpt35turbo-16k'
# Initialize the chat messages history
if "messages" not in st.session_state.keys():
    st.session_state["messages"] = []

assistant_avatar = 'logo1.webp'
user_avatar = 'user.webp'
for message in st.session_state.messages:
    if message["role"] == 'assistant':
        with st.chat_message(message["role"],avatar=assistant_avatar):
            # st.markdown(message["content"])
            if len(message["content"]) == 4:
                try:
                    st.dataframe(message["content"][1], use_container_width=True)
                    st.markdown("SUMMARY:")
                    st.markdown(message["content"][3])
                    st.plotly_chart(message["content"][2], use_container_width=True)
                except:
                    st.subheader(message["content"][0])

                    st.subheader("Description")
                    st.write(message["content"][1])

                    st.subheader(message["content"][2])
                    st.plotly_chart(message["content"][3], use_container_width=True)


            elif len(message["content"]) == 9:
                st.subheader(message["content"][0])
                st.subheader(message["content"][1])
                st.markdown(message["content"][2])

                st.subheader(message["content"][3])
                st.plotly_chart(message["content"][4], use_container_width=True)

                st.subheader(message["content"][5])
                st.markdown(message["content"][6])

                st.subheader(message["content"][7])
                st.plotly_chart(message["content"][8], use_container_width=True)


            else:
                st.markdown(message["content"])
    else:
        with st.chat_message(message["role"],avatar= user_avatar):
            st.markdown(message["content"])

if "history" not in st.session_state:
    st.session_state["history"] = []

def reset_conversation():
  st.session_state["messages"] = []
  st.session_state["history"] = []

#feedback
def fbcb():
    message_id = len(st.session_state.history) - 1
    if message_id >= 0:
        st.session_state.history[message_id]["feedback"] = st.session_state.fb_k


st.sidebar.button('Reset Chat', on_click=reset_conversation)

# SQL pattern matching
import re

def is_sql_query(input_text):
    # Define SQL query patterns using regular expressions
    sql_patterns = [
        'SELECT','FROM',
    ]
    # Check if any SQL pattern matches the input text
    for pattern in sql_patterns:
        if re.search(pattern, input_text, re.IGNORECASE):
            return True

    return False


# Loading data for IVA tool
df_iva_tool = pd.read_csv('tnsv3rdparty.csv')

# Aadi UI
if prompt := st.chat_input():
    with st.chat_message("User",avatar=user_avatar):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    ## MINDMAP
    map_dict = qm.identify_components(prompt)

    if map_dict['analysis'] != 'nan' and map_dict['analysis_period'] != 'nan':
        with st.chat_message("assistant", avatar=assistant_avatar):
            with st.spinner("Thinking..."):
                ext_data1, ext_data2 = qm.data_extract(df_iva_tool,qm.identify_components(prompt))
                # st.write(ext_data1)
                # st.write(ext_data2)
                # st.write(ext_data1[0]['paragraphData1']['HeaderText'])
                if ext_data2 is None:
                    main_title, description, chart_title, fig = bd.reply('GSV',ext_data1, ext_data2)

                    st.subheader(main_title)

                    st.subheader("Description")
                    st.write(description)

                    st.subheader(chart_title)
                    st.plotly_chart(fig)
                else:
                    title, header1, header2, desc1, desc2, chart_title1, chart_title2, fig1, fig2 = bd.reply('GSV', ext_data1, ext_data2)

                    st.subheader(title)
                    st.subheader(header1)
                    st.markdown(desc1)

                    st.subheader(chart_title1)
                    st.plotly_chart(fig1)

                    st.subheader(header2)
                    st.markdown(desc2)

                    st.subheader(chart_title2)
                    st.plotly_chart(fig2)
            try:
                st.session_state.messages.append({"role": "assistant", "content": [main_title, description, chart_title, fig]})
                message_id = len(st.session_state.history)
                st.session_state.history.append({
                    "question": prompt,
                    "answer": [main_title, description, chart_title, fig],
                    "message_id": message_id})
            except:
                st.session_state.messages.append(
                    {"role": "assistant", "content": [title, header1, desc1, chart_title1, fig1, header2, desc2, chart_title2, fig2]})
                message_id = len(st.session_state.history)
                st.session_state.history.append({
                    "question": prompt,
                    "answer": [title, header1, desc1, chart_title1, fig1, header2, desc2, chart_title2, fig2],
                    "message_id": message_id})

    else:
        ## AaDI
        with st.chat_message("assistant", avatar=assistant_avatar):
            with st.spinner("Thinking..."):
                if 'your name' in prompt.lower():
                    response = "Hi, I'm AaDI. I can help simplify your data. Thank you."
                    st.write(response)
                else:
                    vn = va.vn_aays()
                    sql = vn.generate_sql(prompt)

                    if is_sql_query(sql):
                        df = vn.run_sql(sql)

                        st.dataframe(df, use_container_width=True)

                        st.markdown("SUMMARY:")
                        summary = vn.generate_summary(prompt, df)
                        st.markdown(summary)

                        code = vn.generate_plotly_code(question=prompt, sql=sql, df=df)

                        fig = vn.get_plotly_figure(plotly_code=code, df=df)

                        st.plotly_chart(fig, use_container_width=True)

                        with st.form('form'):
                            streamlit_feedback(feedback_type="thumbs", align="flex-start", key='fb_k',optional_text_label="[Optional] Please provide an explanation" )
                            st.form_submit_button('Save feedback', on_click=fbcb)

                    else:
                        st.markdown(sql)
            try:
                st.session_state.messages.append({"role": "assistant", "content": [sql, df, fig, summary]})
                message_id = len(st.session_state.history)
                st.session_state.history.append({
                    "question": prompt,
                    "answer": [sql, df, fig, summary],
                    "message_id": message_id,
                })
            except:
                st.session_state.messages.append({"role": "assistant", "content": sql})
                message_id = len(st.session_state.history)
                st.session_state.history.append({
                    "question": prompt,
                    "answer": sql,
                    "message_id": message_id,
                })

    # Adding question into trainning data
    if 'fb_k' in st.session_state:
        if st.session_state.fb_k is not None:
            if st.session_state.fb_k['score'] == '👍':
                vn = va.vn_aays()

                res = st.session_state.history[-1]
                question = res["question"]
                answer = res["answer"][0]
                question_list = vn.generate_questions()
                if question not in question_list:
                    vn.add_question_sql(question, answer)

# for message in st.session_state.messages:
#     if message["role"] == 'assistant':
#         st.write(message["content"])