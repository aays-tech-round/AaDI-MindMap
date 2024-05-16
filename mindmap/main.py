import mindmap.chart_data as cd
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

with st.sidebar:
    st.title("📝 Upload Your DataFrame")
    uploaded_file = st.file_uploader("Select DataFrame", type=("csv", "xlsx"))

    if uploaded_file is not None:
        # Read the uploaded DataFrame
        df = pd.read_csv(uploaded_file)
        df = df[['Period/Year','Profit_Center_Desc','GL_Account_Name','Amount']]

        values = sorted(df['Period/Year'].unique())
        def_ind = values.index(values[-1])

        year_period = st.selectbox(
            'Select Year/Period',
            values,
            index= def_ind
        )

        head = st.selectbox(
            "Select Head",
            ['NSV', 'GSV'],
            # index=None
        )

        analysis_dur = st.selectbox(
            "Analysis Duration",
            ['Monthly','YTD'],
            index=None,
        )

        analysis_type = st.selectbox(
            "Analysis Type",
            ['Trend','Variance','Decomposition'],
            index=None
        )
        if (analysis_type == 'Variance') | (analysis_type == 'Decomposition'):
            breakdown = st.selectbox(
                "Select Breakdown",
                ['Profit_Center_Desc', 'GL_Account_Name', 'both'],
                index=None
            )


tab1 , tab2 = st.tabs(['API Plots',"Support"])

# if uploaded_file is not None:
#     st.write("Uploaded DataFrame:")
#     st.dataframe(df.head())

with tab1:
    if uploaded_file is not None:

        if analysis_dur == 'Monthly':
            if analysis_type == 'Trend':
                dd = cd.trend_analysis_monthly(df, year_period, head)

                # Title
                st.title("Monthly Trend Analysis")

                st.subheader("Description")
                st.write(dd[0]['paragraphData1']['paragraphText1'])

                # Chart Data
                title = dd[0]['paragraphData1']['Chart1']['chartTitle']
                st.subheader(title)
                # x = [str(i) for i in dd[0]['paragraphData1']['Chart1']['chartData']['X_axis']]
                x =  [str(i // 1000) + '_' + str(i % 1000).zfill(3) for i in dd[0]['paragraphData1']['Chart1']['chartData']['X_axis']]
                y = dd[0]['paragraphData1']['Chart1']['chartData']['Y_axis']


                fig = go.Figure(data=go.Scatter(x=x, y=y))
                st.plotly_chart(fig)

            if analysis_type == 'Variance':
                if breakdown == 'Profit_Center_Desc':
                    dd = cd.monthly_var_analysis_profit(df,year_period,head)

                    # Title

                    st.title("Monthly Variance Analysis for Profit center")

                    #Description
                    st.subheader("Description")
                    st.write(dd[0]['paragraphData1']['paragraphText1'])

                    # Chart Data
                    title = dd[0]['paragraphData1']['Chart1']['chartTitle']
                    st.subheader(title)
                    acc_name = dd[0]['paragraphData1']['Chart1']['chartData']['X_axis']
                    value = dd[0]['paragraphData1']['Chart1']['chartData']['Y_axis']

                    fig = go.Figure(go.Waterfall(
                        name=f"{head}",
                        measure=["absolute"] + ["relative"] * (len(acc_name) - 2) + ['total'],
                        x=acc_name,
                        y=value,
                        textposition="outside",
                        connector={"line": {"color": "rgb(63, 63, 63)"}},
                    ))
                    st.plotly_chart(fig)


                elif breakdown == 'GL_Account_Name':
                    dd = cd.monthly_var_analysis_gl(df,year_period,head)

                    # Title

                    st.title("Monthly Variance Analysis for GL Account Name")

                    st.subheader("Description")
                    st.write(dd[0]['paragraphData1']['paragraphText1'])

                    # Chart Data
                    subhead = dd[0]['paragraphData1']['Chart1']['chartTitle']
                    st.subheader(subhead)
                    acc_name = dd[0]['paragraphData1']['Chart1']['chartData']['X_axis']
                    value = dd[0]['paragraphData1']['Chart1']['chartData']['Y_axis']

                    fig = go.Figure(go.Waterfall(
                        name=f"{head}",
                        measure=["absolute"] + ["relative"] * (len(acc_name) - 2) + ['total'],
                        x=acc_name,
                        y=value,
                        textposition="outside",
                        connector={"line": {"color": "rgb(63, 63, 63)"}},
                    ))
                    st.plotly_chart(fig)

                else:
                    prof, gl = cd.monthly_variance_analysis(df,year_period,head)

                    st.title("Monthly Variance Analysis for Profit Center and GL Account Name")

                    st.header("Profit Center")
                    st.write(prof[0]['paragraphData1']['paragraphText1'])

                    # Chart Data Prof
                    subhead = prof[0]['paragraphData1']['Chart1']['chartTitle']
                    st.subheader(subhead)
                    acc_name_prof = prof[0]['paragraphData1']['Chart1']['chartData']['X_axis']
                    value_prof = prof[0]['paragraphData1']['Chart1']['chartData']['Y_axis']

                    fig1 = go.Figure(go.Waterfall(
                        name=f"{head}",
                        measure=["absolute"] + ["relative"] * (len(acc_name_prof) - 2) + ['total'],
                        x=acc_name_prof,
                        y=value_prof,
                        textposition="outside",
                        connector={"line": {"color": "rgb(63, 63, 63)"}},
                    ))
                    st.plotly_chart(fig1)

                    # For GL Account
                    st.header(" GL Account Name")
                    st.write(gl[0]['paragraphData2']['paragraphText2'])

                    # Chart Data Prof
                    subhead_gl = gl[0]['paragraphData2']['Chart2']['chartTitle']
                    st.subheader(subhead_gl)
                    acc_name_gl = gl[0]['paragraphData2']['Chart2']['chartData']['X_axis']
                    value_gl = gl[0]['paragraphData2']['Chart2']['chartData']['Y_axis']

                    fig2 = go.Figure(go.Waterfall(
                        name=f"{head}",
                        measure=["absolute"] + ["relative"] * (len(acc_name_gl) - 2) + ['total'],
                        x=acc_name_gl,
                        y=value_gl,
                        textposition="outside",
                        connector={"line": {"color": "rgb(63, 63, 63)"}},
                    ))
                    st.plotly_chart(fig2)

           # DECOMPOSITION
            if analysis_type == 'Decomposition':
                if breakdown == 'Profit_Center_Desc':
                    dd = cd.monthly_decom_profit(df,year_period,head)
                    st.title("Monthly Decomposition Analysis of Profit Center")

                    # Description
                    st.header("Description")
                    des = dd[0]['paragraphData1']['paragraphText1']
                    st.write(des)

                    # Chart Data
                    ch_title = dd[0]['paragraphData1']['Chart1']['chartTitle']
                    st.title(ch_title)

                    labels = dd[0]['paragraphData1']['Chart1']['chartdata']['X_axis']
                    values = dd[0]['paragraphData1']['Chart1']['chartdata']['Y_axis']

                    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
                    st.plotly_chart(fig)

                elif breakdown == 'GL_Account_Name':
                    dd = cd.monthly_decom_gl(df,year_period,head)
                    st.title("Monthly Decomposition Analysis of GL Account Name")

                    # Description
                    st.header("Description")
                    des = dd[0]['paragraphData1']['paragraphText1']
                    st.write(des)

                    # Chart Data
                    ch_title = dd[0]['paragraphData1']['Chart1']['chartTitle']
                    st.title(ch_title)

                    labels = dd[0]['paragraphData1']['Chart1']['chartdata']['X_axis']
                    values = dd[0]['paragraphData1']['Chart1']['chartdata']['Y_axis']

                    fig = go.Figure(data=[go.Bar(name="GL Account Name",x=labels, y=values)])
                    st.plotly_chart(fig)

                else:
                    prof, gl = cd.monthly_decom(df,year_period,head)

                    st.title("Monthly Decomposition Analysis of Profit Center & GL Account Name")

                    # Description
                    st.header("Profit Center")
                    des_prof = prof[0]['paragraphData1']['paragraphText1']
                    st.write(des_prof)

                    # Chart Data
                    ch_title_prof = prof[0]['paragraphData1']['Chart1']['chartTitle']
                    st.title(ch_title_prof)

                    # Chart Data Profit
                    labels_prof = prof[0]['paragraphData1']['Chart1']['chartdata']['X_axis']
                    values_prof = prof[0]['paragraphData1']['Chart1']['chartdata']['Y_axis']

                    fig_prof = go.Figure(data=[go.Pie(labels=labels_prof, values=values_prof, hole=.3)])
                    st.plotly_chart(fig_prof)

                    # GL Account Name

                    st.header("GL Account Name")
                    des_gl = gl[0]['paragraphData2']['paragraphText2']
                    st.write(des_gl)

                    # Chart Data
                    ch_title_gl = gl[0]['paragraphData2']['Chart2']['chartTitle']
                    st.title(ch_title_gl)

                    labels_gl = gl[0]['paragraphData2']['Chart2']['chartdata']['X_axis']
                    values_gl = gl[0]['paragraphData2']['Chart2']['chartdata']['Y_axis']

                    fig_gl = go.Figure(data=[go.Bar(name= "GL Accounts",x=labels_gl, y=values_gl)])
                    st.plotly_chart(fig_gl)

        if analysis_dur == 'YTD':
            if analysis_type == 'Trend':
                dd = cd.trend_analysis_26_rolling(df, year_period, head)

                # Title
                title = dd[0]['paragraphData1']['Chart1']['chartTitle']
                st.title(title)


                st.subheader("Description")
                st.write(dd[0]['paragraphData1']['paragraphText1'])

                # Chart Data
                st.subheader("Analysis Plot")
                # x = [str(i) for i in dd[0]['paragraphData1']['Chart1']['chartData']['X_axis']]
                x = [str(i // 1000) + '_' + str(i % 1000).zfill(3) for i in
                     dd[0]['paragraphData1']['Chart1']['chartData']['X_axis']]
                y = dd[0]['paragraphData1']['Chart1']['chartData']['Y_axis']
                bs = [dd[0]['paragraphData1']['Chart1']['chartData']['BaseLine']] * len(x)

                fig = go.Figure()

                fig.add_traces(
                    go.Scatter(x=x, y=y, name='rolling value'),

                )
                fig.add_traces(
                    go.Scatter(x=x, y=bs, name='Average Line')
                )

                st.plotly_chart(fig)

            # Variance
            if analysis_type == 'Variance':
                if breakdown == 'Profit_Center_Desc':
                    dd, _ = cd.ytd_variance_analysis(df,year_period,head)

                    st.title("YTD Variance Analysis for Profit center")

                    # Description
                    st.subheader("Description")
                    st.write(dd[0]['paragraphData1']['paragraphText1'])

                    # Chart Data
                    title = dd[0]['paragraphData1']['Chart1']['chartTitle']
                    st.subheader(title)
                    acc_name = dd[0]['paragraphData1']['Chart1']['chartData']['X_axis']
                    value = dd[0]['paragraphData1']['Chart1']['chartData']['Y_axis']

                    fig = go.Figure(go.Waterfall(
                        name=f"{head}",
                        measure=["absolute"] + ["relative"] * (len(acc_name) - 2) + ['total'],
                        x=acc_name,
                        y=value,
                        textposition="outside",
                        connector={"line": {"color": "rgb(63, 63, 63)"}},
                    ))
                    st.plotly_chart(fig)

                elif breakdown == 'GL_Account_Name':
                    _, dd = cd.ytd_variance_analysis(df, year_period, head)

                    st.title("Monthly Variance Analysis for GL Account Name")

                    st.subheader("Description")
                    st.write(dd[0]['paragraphData2']['paragraphText2'])

                    # Chart Data
                    subhead = dd[0]['paragraphData2']['Chart2']['chartTitle']
                    st.subheader(subhead)
                    acc_name = dd[0]['paragraphData2']['Chart2']['chartData']['X_axis']
                    value = dd[0]['paragraphData2']['Chart2']['chartData']['Y_axis']

                    fig = go.Figure(go.Waterfall(
                        name=f"{head}",
                        measure=["absolute"] + ["relative"] * (len(acc_name) - 2) + ['total'],
                        x=acc_name,
                        y=value,
                        textposition="outside",
                        connector={"line": {"color": "rgb(63, 63, 63)"}},
                    ))
                    st.plotly_chart(fig)

                else:
                    prof, gl = cd.ytd_variance_analysis(df, year_period, head)

                    st.title("YTD Overall Variance Analysis")

                    # Description
                    st.subheader("Profit Center")
                    st.write(prof[0]['paragraphData1']['paragraphText1'])

                    # Chart Data
                    title_prof = prof[0]['paragraphData1']['Chart1']['chartTitle']
                    st.subheader(title_prof)
                    acc_name_prof = prof[0]['paragraphData1']['Chart1']['chartData']['X_axis']
                    value_prof = prof[0]['paragraphData1']['Chart1']['chartData']['Y_axis']

                    fig1 = go.Figure(go.Waterfall(
                        name=f"{head}",
                        measure=["absolute"] + ["relative"] * (len(acc_name_prof) - 2) + ['total'],
                        x=acc_name_prof,
                        y=value_prof,
                        textposition="outside",
                        connector={"line": {"color": "rgb(63, 63, 63)"}},
                    ))
                    st.plotly_chart(fig1)

                    ## For GL Account
                    st.subheader("GL Account Name")
                    st.write(gl[0]['paragraphData2']['paragraphText2'])

                    # Chart Data
                    subhead = gl[0]['paragraphData2']['Chart2']['chartTitle']
                    st.subheader(subhead)
                    acc_name_gl = gl[0]['paragraphData2']['Chart2']['chartData']['X_axis']
                    value_gl = gl[0]['paragraphData2']['Chart2']['chartData']['Y_axis']

                    fig2 = go.Figure(go.Waterfall(
                        name=f"{head}",
                        measure=["absolute"] + ["relative"] * (len(acc_name_gl) - 2) + ['total'],
                        x=acc_name_gl,
                        y=value_gl,
                        textposition="outside",
                        connector={"line": {"color": "rgb(63, 63, 63)"}},
                    ))
                    st.plotly_chart(fig2)

            if analysis_type == 'Decomposition':
                if breakdown == 'Profit_Center_Desc':
                    dd, _ = cd.ytd_decom(df, year_period, head)

                    st.title("YTD Decomposition Analysis of Profit Center")

                    # Description
                    st.header("Description")
                    des = dd[0]['paragraphData1']['paragraphText1']
                    st.write(des)

                    # Chart Data
                    ch_title = dd[0]['paragraphData1']['Chart1']['chartTitle']
                    st.title(ch_title)

                    labels = dd[0]['paragraphData1']['Chart1']['chartdata']['X_axis']
                    values = dd[0]['paragraphData1']['Chart1']['chartdata']['Y_axis']

                    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
                    st.plotly_chart(fig)

                elif breakdown == 'GL_Account_Name':
                    _,dd = cd.ytd_decom(df,year_period, head)
                    st.title("YTD Decomposition Analysis of GL Account Name")

                    # Description
                    st.header("Description")
                    des = dd[0]['paragraphData2']['paragraphText2']
                    st.write(des)

                    # Chart Data
                    ch_title = dd[0]['paragraphData2']['Chart2']['chartTitle']
                    st.title(ch_title)

                    labels = dd[0]['paragraphData2']['Chart2']['chartdata']['X_axis']
                    values = dd[0]['paragraphData2']['Chart2']['chartdata']['Y_axis']

                    # fig = go.Figure(data=[go.Bar(name="GL Account Name", x=labels, y=values)])
                    # st.plotly_chart(fig)

                    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
                    st.plotly_chart(fig)

                else:
                    prof, gl = cd.ytd_decom(df, year_period, head)

                    st.title("YTD Overall Decomposition Analysis")

                    # Description
                    st.subheader("Profit Center")
                    des = prof[0]['paragraphData1']['paragraphText1']
                    st.write(des)

                    # Chart Data
                    ch_title_prof = prof[0]['paragraphData1']['Chart1']['chartTitle']
                    st.title(ch_title_prof)

                    labels_prof = prof[0]['paragraphData1']['Chart1']['chartdata']['X_axis']
                    values_prof = prof[0]['paragraphData1']['Chart1']['chartdata']['Y_axis']

                    fig1 = go.Figure(data=[go.Pie(labels=labels_prof, values=values_prof, hole=.3)])
                    st.plotly_chart(fig1)

                    # GL Account Name
                    st.header("GL Account Name")
                    des = gl[0]['paragraphData2']['paragraphText2']
                    st.write(des)

                    # Chart Data
                    ch_title_gl = gl[0]['paragraphData2']['Chart2']['chartTitle']
                    st.title(ch_title_gl)

                    labels_gl = gl[0]['paragraphData2']['Chart2']['chartdata']['X_axis']
                    values_gl = gl[0]['paragraphData2']['Chart2']['chartdata']['Y_axis']

                    # fig = go.Figure(data=[go.Bar(name="GL Account Name", x=labels, y=values)])
                    # st.plotly_chart(fig)

                    fig2 = go.Figure(data=[go.Pie(labels=labels_gl, values=values_gl, hole=.3)])
                    st.plotly_chart(fig2)

# with tab2:
#     if uploaded_file is not None:
#         keyword_to_analysis = {
#
#             'GSV': ['Gross sales value', 'revenue', 'sales', 'GSV'],
#
#             'Trend Analysis': ['Statistical analysis', 'growth', 'month on month movements', 'CAGR', 'trend'],
#
#             'Decomposition': ['breakdown', 'break down', 'analyse', 'composition', 'composed of', 'mix', 'decomposition'],
#
#             'Variance': ['Flux report', 'month-on-month change', 'year-on-year change', 'year on year', 'month on month',
#                          'variance'],
#
#             'Summary': ['Overall', 'overview', 'summary'],
#
#             'Monthly': ['monthly analysis', 'monthly'],
#
#             'YTD': ['YTD analysis', 'year to date', 'year-to-date', 'ytd'],
#
#             'Accounting Profile': ['accounting profile', 'accounting', 'account'],
#
#             'GL Account Name': ['gl account', 'gl account name', 'gl'],
#
#             'Profit Center': ['profit center', 'profit center profile', 'profit centre']
#
#         }
#
#
#         def year_extract(input_string):
#             input_string = input_string.lower()
#             yp = {
#                 'year': ['2020', '2021', '2022', '2023'],
#                 'period': ['period 1', 'period 2', 'period 3', 'period 4', 'period 5', 'period 6', 'period 7', 'period 8',
#                            'period 9', 'period 10', 'period 11', 'period 12', 'period 13',
#                            'p01', 'p02', 'p03', 'p04', 'p05', 'p06', 'p07', 'p08', 'p09', 'p10', 'p11', 'p12', 'p13']
#             }
#
#             data = {}
#             for k, pr in yp.items():
#                 for p in pr:
#                     if p in input_string:
#                         data[k] = p
#             return data
#
#
#         def identify_components(input_string):
#             # Convert input string to lowercase for case-insensitive matching
#             input_string = input_string.lower()
#
#             data = {'analysis': 'nan',
#                     'analysis_period': 'nan',
#                     'breakdown': 'nan',
#                     'year': 'nan',
#                     'period': 'nan',
#                     'year': 'nan',
#                     'period': 'nan'
#                     }
#
#             for key, phrases in keyword_to_analysis.items():
#                 for phrase in phrases:
#                     if phrase.lower() in input_string:
#                         if key in ['Monthly', 'YTD']:
#                             data['analysis_period'] = key
#                         elif key in ['Accounting Profile', 'Profit Center', 'GL Account Name']:
#                             data['breakdown'] = key
#                         else:
#                             data['analysis'] = key
#                         break
#
#             dict_yp = year_extract(input_string)
#             if 'year' in dict_yp.keys():
#                 data['year'] = dict_yp['year']
#
#             if 'period' in dict_yp.keys():
#                 data['period'] = dict_yp['period']
#
#             return data
#
#
#         def data_extract(dd):
#             # Creating year period
#             # """this condition will return year and period 9 as desired format,
#             # if period is not given it will add period 13 with the year by default,
#             # if year is not given it will add 2023 as year by default
#             # and if both of them are not available then by default it will be 2023009
#             # """
#             if dd['period'] != 'nan' and dd['year'] != 'nan':
#                 p = "".join(filter(str.isdigit, dd['period']))
#                 p = p.zfill(3)
#                 yp = int(dd['year'] + p)
#
#             elif dd['period'] == 'nan':
#                 yp = int(dd['year'] + '009')
#
#             elif dd['year'] == 'nan':
#                 p = "".join(filter(str.isdigit, dd['period']))
#                 p = p.zfill(3)
#                 yp = int("2023" + p)
#
#             else:
#                 yp = 2023009
#
#             ## Analysis Data
#             # """
#             # This condition will return chart data and paragraph as per the user query
#             # """
#
#             ## Monthly Analysis
#             if dd['analysis_period'] == 'Monthly':
#
#                 ## Trend Analysis
#                 if dd['analysis'] == 'Trend Analysis':
#                     result = cd.trend_analysis_monthly(df, yp, 'GSV')
#
#                 ## Varince Analysis
#                 if dd['analysis'] == 'Variance':
#                     if dd['breakdown'] == 'nan':
#                         result = cd.monthly_variance_analysis(df, yp, 'GSV')
#
#                 if dd['analysis'] == 'Variance':
#                     if dd['breakdown'] == 'Profit Center':
#                         result = cd.monthly_var_analysis_profit(df, yp, 'GSV')
#
#                 if dd['analysis'] == 'Variance':
#                     if dd['breakdown'] == 'GL Account Name':
#                         result = cd.monthly_var_analysis_gl(df, yp, 'GSV')
#
#                 ## Decomposition Analysis
#                 if dd['analysis'] == 'Decomposition':
#                     if dd['breakdown'] == 'nan':
#                         result = cd.monthly_decom(df, yp, 'GSV')
#
#                 if dd['analysis'] == 'Decomposition':
#                     if dd['breakdown'] == 'Profit Center':
#                         result = cd.monthly_decom_profit(df, yp, 'GSV')
#
#                 if dd['analysis'] == 'Decomposition':
#                     if dd['breakdown'] == 'GL Account Name':
#                         result = cd.monthly_decom_gl(df, yp, 'GSV')
#
#             # YTD Analysis
#             if dd['analysis_period'] == 'YTD':
#
#                 ## Trend Analysis
#                 if dd['analysis'] == 'Trend Analysis':
#                     result = cd.trend_analysis_26_rolling(df, yp, 'GSV')
#
#                 ## Varince Analysis
#                 if dd['analysis'] == 'Variance':
#                     if dd['breakdown'] == 'nan':
#                         result = cd.ytd_variance_analysis(df, yp, 'GSV')
#
#                 if dd['analysis'] == 'Variance':
#                     if dd['breakdown'] == 'Profit Center':
#                         result = cd.ytd_variance_analysis_profit(df, yp, 'GSV')
#
#                 if dd['analysis'] == 'Variance':
#                     if dd['breakdown'] == 'GL Account Name':
#                         result = cd.ytd_variance_analysis_gl(df, yp, 'GSV')
#
#                 ## Decomposition Analysis
#                 if dd['analysis'] == 'Decomposition':
#                     if dd['breakdown'] == 'nan':
#                         result = cd.ytd_decom(df, yp, 'GSV')
#
#                 if dd['analysis'] == 'Decomposition':
#                     if dd['breakdown'] == 'Profit Center':
#                         result = cd.ytd_decom_prof(df, yp, 'GSV')
#
#                 if dd['analysis'] == 'Decomposition':
#                     if dd['breakdown'] == 'GL Account Name':
#                         result = cd.ytd_decom_gl(df, yp, 'GSV')
#
#             return result
#
#
#         prompt = st.chat_input("What is up?")
#
#         if prompt:
#             with st.chat_message('user'):
#                 st.write(prompt)
#
#             ext_data = data_extract(identify_components(prompt))
#             with st.chat_message("assistant"):
#                 st.write(ext_data)
