import streamlit as st
import random
import time


import mindmap.chart_data as cd
import plotly.graph_objects as go

# st.title("Simple chat")
#
# # Initialize chat history
# if "messages" not in st.session_state:
#     st.session_state.messages = []

# # Display chat messages from history on app rerun
# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])

# # Accept user input
# if prompt := st.chat_input("What is up?"):
#     # Display user message in chat message container
#     with st.chat_message("user"):
#         st.markdown(prompt)
#     # Add user message to chat history
#     st.session_state.messages.append({"role": "user", "content": prompt})
#
# # Display assistant response in chat message container
# with st.chat_message("assistant"):
#     message_placeholder = st.empty()
#     full_response = ""
#     assistant_response = random.choice(
#         [
#             "Hello there! How can I assist you today?",
#             "Hi, human! Is there anything I can help you with?",
#             "Do you need help?",
#         ]
#     )
#     # Simulate stream of response with milliseconds delay
#     for chunk in assistant_response.split():
#         full_response += chunk + " "
#         time.sleep(0.05)
#         # Add a blinking cursor to simulate typing
#         message_placeholder.markdown(full_response + "▌")
#     message_placeholder.markdown(full_response)
# # Add assistant response to chat history
# st.session_state.messages.append({"role": "assistant", "content": full_response})

try:
    df = pd.read_csv('tnsv3rdparty.csv')

    keyword_to_analysis = {

        'GSV': ['Gross sales value', 'revenue', 'sales', 'GSV'],

        'Trend Analysis': ['Statistical analysis', 'growth', 'month on month movements', 'CAGR', 'trend'],

        'Decomposition': ['breakdown', 'break down', 'analyse', 'composition', 'composed of', 'mix', 'decomposition'],

        'Variance': ['Flux report', 'month-on-month change', 'year-on-year change', 'year on year', 'month on month',
                     'variance'],

        'Summary': ['Overall', 'overview', 'summary'],

        'Monthly': ['monthly analysis', 'monthly'],

        'YTD': ['YTD analysis', 'year to date', 'year-to-date', 'ytd'],

        'Accounting Profile': ['accounting profile', 'accounting', 'account'],

        'GL Account Name': ['gl account', 'gl account name', 'gl'],

        'Profit Center': ['profit center', 'profit center profile', 'profit centre']

    }


    def year_extract(input_string):
        input_string = input_string.lower()
        yp = {
            'year': ['2020', '2021', '2022', '2023'],
            'period': ['period 1', 'period 2', 'period 3', 'period 4', 'period 5', 'period 6', 'period 7', 'period 8',
                       'period 9', 'period 10', 'period 11', 'period 12', 'period 13',
                       'p01', 'p02', 'p03', 'p04', 'p05', 'p06', 'p07', 'p08', 'p09', 'p10', 'p11', 'p12', 'p13']
        }

        data = {}
        for k, pr in yp.items():
            for p in pr:
                if p in input_string:
                    data[k] = p
        return data


    def identify_components(input_string):
        # Convert input string to lowercase for case-insensitive matching
        input_string = input_string.lower()

        data = {'analysis': 'nan',
                'analysis_period': 'nan',
                'breakdown': 'nan',
                'year': 'nan',
                'period': 'nan',}
        # 'year': 'nan',
        # 'period': 'nan'

        for key, phrases in keyword_to_analysis.items():
            for phrase in phrases:
                if phrase.lower() in input_string:
                    if key in ['Monthly', 'YTD']:
                        data['analysis_period'] = key
                    elif key in ['Accounting Profile', 'Profit Center', 'GL Account Name']:
                        data['breakdown'] = key
                    else:
                        data['analysis'] = key
                    break

        dict_yp = year_extract(input_string)
        if 'year' in dict_yp.keys():
            data['year'] = dict_yp['year']

        if 'period' in dict_yp.keys():
            data['period'] = dict_yp['period']

        return data


    def data_extract(dd):
        # Creating year period
        # """this condition will return year and period 9 as desired format,
        # if period is not given it will add period 13 with the year by default,
        # if year is not given it will add 2023 as year by default
        # and if both of them are not available then by default it will be 2023009
        # """

        if dd['period'] != 'nan' and dd['year'] != 'nan':
            p = "".join(filter(str.isdigit, dd['period']))
            p = p.zfill(3)
            yp = int(dd['year'] + p)

        elif dd['period'] == 'nan':
            yp = int(dd['year'] + '009')

        elif dd['year'] == 'nan':
            p = "".join(filter(str.isdigit, dd['period']))
            p = p.zfill(3)
            yp = int("2023" + p)

        else:
            yp = 2023009

        ## Analysis Data
        # """
        # This condition will return chart data and paragraph as per the user query
        # """

        ## Monthly Analysis
        if dd['analysis_period'] == 'Monthly':

            ## Trend Analysis
            if dd['analysis'] == 'Trend Analysis':
                result = cd.trend_analysis_monthly(df, yp, 'GSV')

            ## Varince Analysis
            if dd['analysis'] == 'Variance':
                if dd['breakdown'] == 'nan':
                    result = cd.monthly_variance_analysis(df, yp, 'GSV')

            if dd['analysis'] == 'Variance':
                if dd['breakdown'] == 'Profit Center':
                    result = cd.monthly_var_analysis_profit(df, yp, 'GSV')

            if dd['analysis'] == 'Variance':
                if dd['breakdown'] == 'GL Account Name':
                    result = cd.monthly_var_analysis_gl(df, yp, 'GSV')

            ## Decomposition Analysis
            if dd['analysis'] == 'Decomposition':
                if dd['breakdown'] == 'nan':
                    result = cd.monthly_decom(df, yp, 'GSV')

            if dd['analysis'] == 'Decomposition':
                if dd['breakdown'] == 'Profit Center':
                    result = cd.monthly_decom_profit(df, yp, 'GSV')

            if dd['analysis'] == 'Decomposition':
                if dd['breakdown'] == 'GL Account Name':
                    result = cd.monthly_decom_gl(df, yp, 'GSV')

        # YTD Analysis
        if dd['analysis_period'] == 'YTD':

            ## Trend Analysis
            if dd['analysis'] == 'Trend Analysis':
                result = cd.trend_analysis_26_rolling(df, yp, 'GSV')

            ## Varince Analysis
            if dd['analysis'] == 'Variance':
                if dd['breakdown'] == 'nan':
                    result = cd.ytd_variance_analysis(df, yp, 'GSV')

            if dd['analysis'] == 'Variance':
                if dd['breakdown'] == 'Profit Center':
                    result = cd.ytd_variance_analysis_profit(df, yp, 'GSV')

            if dd['analysis'] == 'Variance':
                if dd['breakdown'] == 'GL Account Name':
                    result = cd.ytd_variance_analysis_gl(df, yp, 'GSV')

            ## Decomposition Analysis
            if dd['analysis'] == 'Decomposition':
                if dd['breakdown'] == 'nan':
                    result = cd.ytd_decom(df, yp, 'GSV')

            if dd['analysis'] == 'Decomposition':
                if dd['breakdown'] == 'Profit Center':
                    result = cd.ytd_decom_prof(df, yp, 'GSV')

            if dd['analysis'] == 'Decomposition':
                if dd['breakdown'] == 'GL Account Name':
                    result = cd.ytd_decom_gl(df, yp, 'GSV')

        return result

    prompt = st.chat_input("What is up?")

    if prompt:
        with st.chat_message('user'):
            st.write(prompt)

        ext_data = data_extract(identify_components(prompt))
        with st.chat_message("assistant"):
            # st.write(ext_data)
            ## Trend Analysis
            if ext_data[0]['paragraphData1']['HeaderText'] == 'Monthly Trend Variance Analysis':
                st.title("Monthly Trend Analysis")

                st.subheader("Description")
                st.write(ext_data[0]['paragraphData1']['paragraphText1'])

                # Chart Data
                title = ext_data[0]['paragraphData1']['Chart1']['chartTitle']
                st.subheader(title)
                # x = [str(i) for i in dd[0]['paragraphData1']['Chart1']['chartData']['X_axis']]
                x = [str(i // 1000) + '_' + str(i % 1000).zfill(3) for i in
                     ext_data[0]['paragraphData1']['Chart1']['chartData']['X_axis']]
                y = ext_data[0]['paragraphData1']['Chart1']['chartData']['Y_axis']

                fig = go.Figure(data=go.Scatter(x=x, y=y))
                st.plotly_chart(fig)

            if ext_data[0]['paragraphData1']['HeaderText'] == 'Trend Analysis Monthly':
                title = ext_data[0]['paragraphData1']['Chart1']['chartTitle']
                st.title(title)

                st.subheader("Description")
                st.write(ext_data[0]['paragraphData1']['paragraphText1'])

                # Chart Data
                st.subheader("Analysis Plot")
                # x = [str(i) for i in dd[0]['paragraphData1']['Chart1']['chartData']['X_axis']]
                x = [str(i // 1000) + '_' + str(i % 1000).zfill(3) for i in
                     ext_data[0]['paragraphData1']['Chart1']['chartData']['X_axis']]
                y = ext_data[0]['paragraphData1']['Chart1']['chartData']['Y_axis']
                bs = [ext_data[0]['paragraphData1']['Chart1']['chartData']['BaseLine']] * len(x)

                fig = go.Figure()

                fig.add_traces(
                    go.Scatter(x=x, y=y, name='rolling value'),

                )
                fig.add_traces(
                    go.Scatter(x=x, y=bs, name='Average Line')
                )

                st.plotly_chart(fig)

            ## Variance Analysis
            if ext_data[0]['paragraphData1']['HeaderText'] == 'Monthly variance analysis of Profit center':
                st.title("Monthly Variance Analysis for Profit center")

                # Description
                st.subheader("Description")
                st.write(ext_data[0]['paragraphData1']['paragraphText1'])

                # Chart Data
                title = ext_data[0]['paragraphData1']['Chart1']['chartTitle']
                st.subheader(title)
                acc_name = ext_data[0]['paragraphData1']['Chart1']['chartData']['X_axis']
                value = ext_data[0]['paragraphData1']['Chart1']['chartData']['Y_axis']

                fig = go.Figure(go.Waterfall(
                    # name=f"{head}",
                    name = 'NSV',
                    measure=["absolute"] + ["relative"] * (len(acc_name) - 2) + ['total'],
                    x=acc_name,
                    y=value,
                    textposition="outside",
                    connector={"line": {"color": "rgb(63, 63, 63)"}},
                ))
                st.plotly_chart(fig)
except:
    with st.chat_message("assistant"):
        response = random.choice(
                [
                    "Hello there! Please Ask About your data?",
                    "Hi! You can ask about your data",
                    "Hope you are doing good, Do you need help about your data?",
                ])
        st.write(response)
