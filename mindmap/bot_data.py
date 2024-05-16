import plotly.graph_objects as go

def reply(head,extract_data,extract_data2):

    if extract_data2 is None:
        if extract_data[0]['paragraphData1']['HeaderText'] == 'Monthly Trend Variance Analysis':
            title = "Monthly Trend Analysis"
            description = extract_data[0]['paragraphData1']['paragraphText1']
            chart_title = extract_data[0]['paragraphData1']['Chart1']['chartTitle']
            x = [str(i // 1000) + '_' + str(i % 1000).zfill(3) for i in
                 extract_data[0]['paragraphData1']['Chart1']['chartData']['X_axis']]
            y = extract_data[0]['paragraphData1']['Chart1']['chartData']['Y_axis']
            fig = go.Figure(data=go.Scatter(x=x, y=y))

            return title, description, chart_title, fig

        if extract_data[0]['paragraphData1']['HeaderText'] == 'Trend Analysis Monthly':
            title = 'Trend Analysis Monthly'
            chart_title = extract_data[0]['paragraphData1']['Chart1']['chartTitle']
            description = extract_data[0]['paragraphData1']['paragraphText1']

            x = [str(i // 1000) + '_' + str(i % 1000).zfill(3) for i in
                 extract_data[0]['paragraphData1']['Chart1']['chartData']['X_axis']]
            y = extract_data[0]['paragraphData1']['Chart1']['chartData']['Y_axis']
            bs = [extract_data[0]['paragraphData1']['Chart1']['chartData']['BaseLine']] * len(x)

            fig = go.Figure()

            fig.add_traces(
                go.Scatter(x=x, y=y, name='rolling value'),

            )
            fig.add_traces(
                go.Scatter(x=x, y=bs, name='Average Line')
            )

            return title, description, chart_title, fig

        ## Variance Analysis for profit center
        if extract_data[0]['paragraphData1']['HeaderText'] == 'Monthly variance analysis by Profit center':
            title = "Monthly Variance Analysis for Profit center"

            # Description
            description = extract_data[0]['paragraphData1']['paragraphText1']

            # Chart Data
            chart_title = extract_data[0]['paragraphData1']['Chart1']['chartTitle']
            acc_name = extract_data[0]['paragraphData1']['Chart1']['chartData']['X_axis']
            value = extract_data[0]['paragraphData1']['Chart1']['chartData']['Y_axis']

            fig = go.Figure(go.Waterfall(
                # name=f"{head}",
                name=f'{head}',
                measure=["absolute"] + ["relative"] * (len(acc_name) - 2) + ['total'],
                x=acc_name,
                y=value,
                textposition="outside",
                connector={"line": {"color": "rgb(63, 63, 63)"}},
            ))

            return title, description, chart_title, fig

        if extract_data[0]['paragraphData1']['HeaderText'] == 'Monthly variance analysis by GL Account Name':

            title = "Monthly Variance Analysis for GL Account Name"

            description = extract_data[0]['paragraphData1']['paragraphText1']

            chart_title = extract_data[0]['paragraphData1']['Chart1']['chartTitle']

            acc_name = extract_data[0]['paragraphData1']['Chart1']['chartData']['X_axis']
            value = extract_data[0]['paragraphData1']['Chart1']['chartData']['Y_axis']

            fig = go.Figure(go.Waterfall(
                name=f"{head}",
                measure=["absolute"] + ["relative"] * (len(acc_name) - 2) + ['total'],
                x=acc_name,
                y=value,
                textposition="outside",
                connector={"line": {"color": "rgb(63, 63, 63)"}},
            ))
            return title, description, chart_title, fig

        ## Decomposition
        if extract_data[0]['paragraphData1']['HeaderText'] == "Monthly Profit Center Breakdown":
            title = "Monthly Decomposition Analysis of Profit Center"
            description = extract_data[0]['paragraphData1']['paragraphText1']
            chart_title = extract_data[0]['paragraphData1']['Chart1']['chartTitle']
            labels = extract_data[0]['paragraphData1']['Chart1']['chartdata']['X_axis']
            values = extract_data[0]['paragraphData1']['Chart1']['chartdata']['Y_axis']
            fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])

            return title, description, chart_title, fig

        if extract_data[0]['paragraphData1']['HeaderText'] == "Monthly GL Account Name Breakdown":
            title = "Monthly Decomposition Analysis of GL Account Name"
            description = extract_data[0]['paragraphData1']['paragraphText1']
            chart_title = extract_data[0]['paragraphData1']['Chart1']['chartTitle']
            labels = extract_data[0]['paragraphData1']['Chart1']['chartdata']['X_axis']
            values = extract_data[0]['paragraphData1']['Chart1']['chartdata']['Y_axis']
            fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])

            return title, description, chart_title, fig

        #YTD

        # Trend
        if extract_data[0]['paragraphData1']['HeaderText'] == "Trend Analysis YTD":
            title = extract_data[0]['paragraphData1']['HeaderText']
            description = extract_data[0]['paragraphData1']['paragraphText1']
            chart_title = extract_data[0]['paragraphData1']['Chart1']['chartTitle']

            x = [str(i // 1000) + '_' + str(i % 1000).zfill(3) for i in
                 extract_data[0]['paragraphData1']['Chart1']['chartData']['X_axis']]
            y = extract_data[0]['paragraphData1']['Chart1']['chartData']['Y_axis']
            bs = [extract_data[0]['paragraphData1']['Chart1']['chartData']['BaseLine']] * len(x)

            fig = go.Figure()

            fig.add_traces(
                go.Scatter(x=x, y=y, name='rolling value'),

            )
            fig.add_traces(
                go.Scatter(x=x, y=bs, name='Average Line')
            )

            return title, description, chart_title, fig

        # Variance
        if extract_data[0]['paragraphData1']['HeaderText'] == "YTD variance analysis by Profit Center":

            title = 'YTD Variance analysis by Profit Center'

            description = extract_data[0]['paragraphData1']['paragraphText1']

            chart_title = extract_data[0]['paragraphData1']['Chart1']['chartTitle']

            acc_name = extract_data[0]['paragraphData1']['Chart1']['chartData']['X_axis']
            value = extract_data[0]['paragraphData1']['Chart1']['chartData']['Y_axis']

            fig = go.Figure(go.Waterfall(
                name=f"{head}",
                measure=["absolute"] + ["relative"] * (len(acc_name) - 2) + ['total'],
                x=acc_name,
                y=value,
                textposition="outside",
                connector={"line": {"color": "rgb(63, 63, 63)"}},
            ))
            return title, description, chart_title, fig

        if extract_data[0]['paragraphData1']['HeaderText'] == "YTD variance analysis by GL Account Name":

            title = 'YTD Variance analysis by GL Account'

            description = extract_data[0]['paragraphData1']['paragraphText1']

            chart_title = extract_data[0]['paragraphData1']['Chart1']['chartTitle']

            acc_name = extract_data[0]['paragraphData1']['Chart1']['chartData']['X_axis']
            value = extract_data[0]['paragraphData1']['Chart1']['chartData']['Y_axis']

            fig = go.Figure(go.Waterfall(
                name=f"{head}",
                measure=["absolute"] + ["relative"] * (len(acc_name) - 2) + ['total'],
                x=acc_name,
                y=value,
                textposition="outside",
                connector={"line": {"color": "rgb(63, 63, 63)"}},
            ))
            return title, description, chart_title, fig

        ## Decomposition

        if extract_data[0]['paragraphData1']['HeaderText'] == "YTD Profit Center Breakdown":
            title = "YTD Decomposition Analysis by Profit Center"
            description = extract_data[0]['paragraphData1']['paragraphText1']
            chart_title = extract_data[0]['paragraphData1']['Chart1']['chartTitle']
            labels = extract_data[0]['paragraphData1']['Chart1']['chartdata']['X_axis']
            values = extract_data[0]['paragraphData1']['Chart1']['chartdata']['Y_axis']
            fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])

            return title, description, chart_title, fig

        if extract_data[0]['paragraphData1']['HeaderText'] == "YTD GL Account Name Breakdown":
            title = "YTD Decomposition Analysis by GL Account Name"
            description = extract_data[0]['paragraphData1']['paragraphText1']
            chart_title = extract_data[0]['paragraphData1']['Chart1']['chartTitle']
            labels = extract_data[0]['paragraphData1']['Chart1']['chartdata']['X_axis']
            values = extract_data[0]['paragraphData1']['Chart1']['chartdata']['Y_axis']
            fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])

            return title, description, chart_title, fig




    else:
        # Monthly Variance
        if extract_data[0]['paragraphData1']['HeaderText'] == "Monthly variance analysis by Profit center":
            title = "Monthly Variance Analysis by Profit Center and GL Account Name"

            header1 = "Variance Analysis by Profit Center"
            header2 = "Variance Analysis by GL Account"

            desc1 = extract_data[0]['paragraphData1']['paragraphText1']
            desc2 = extract_data2[0]['paragraphData2']['paragraphText2']

            chart_title1 = extract_data[0]['paragraphData1']['Chart1']['chartTitle']
            chart_title2 = extract_data2[0]['paragraphData2']['Chart2']['chartTitle']

            acc_name_prof = extract_data[0]['paragraphData1']['Chart1']['chartData']['X_axis']
            value_prof = extract_data[0]['paragraphData1']['Chart1']['chartData']['Y_axis']

            fig1 = go.Figure(go.Waterfall(
                name=f"{head}",
                measure=["absolute"] + ["relative"] * (len(acc_name_prof) - 2) + ['total'],
                x=acc_name_prof,
                y=value_prof,
                textposition="outside",
                connector={"line": {"color": "rgb(63, 63, 63)"}},
            ))

            acc_name_gl = extract_data2[0]['paragraphData2']['Chart2']['chartData']['X_axis']
            value_gl = extract_data2[0]['paragraphData2']['Chart2']['chartData']['Y_axis']

            fig2 = go.Figure(go.Waterfall(
                name=f"{head}",
                measure=["absolute"] + ["relative"] * (len(acc_name_gl) - 2) + ['total'],
                x=acc_name_gl,
                y=value_gl,
                textposition="outside",
                connector={"line": {"color": "rgb(63, 63, 63)"}},
            ))

            return title, header1, header2, desc1, desc2, chart_title1, chart_title2, fig1, fig2

        #Monthly Decomposition
        if extract_data[0]['paragraphData1']['HeaderText'] == "Monthly Profit Center Breakdown":
            title = "Monthly Decomposition Analysis by Profit Center and GL Account Name"

            header1 = "Decomposition analysis by Profit Center"
            header2 = "Decomposition analysis by GL Account"

            desc1 = extract_data[0]['paragraphData1']['paragraphText1']
            desc2 = extract_data2[0]['paragraphData2']['paragraphText2']

            chart_title1 = extract_data[0]['paragraphData1']['Chart1']['chartTitle']
            chart_title2 = extract_data2[0]['paragraphData2']['Chart2']['chartTitle']

            labels_prof = extract_data[0]['paragraphData1']['Chart1']['chartdata']['X_axis']
            values_prof = extract_data[0]['paragraphData1']['Chart1']['chartdata']['Y_axis']

            fig1 = go.Figure(data=[go.Pie(labels=labels_prof, values=values_prof, hole=.3)])

            labels_gl = extract_data2[0]['paragraphData2']['Chart2']['chartdata']['X_axis']
            values_gl = extract_data2[0]['paragraphData2']['Chart2']['chartdata']['Y_axis']

            fig2 = go.Figure(data=[go.Bar(name="GL Accounts", x=labels_gl, y=values_gl)])

            return title, header1, header2, desc1, desc2, chart_title1, chart_title2, fig1, fig2

        #YTD Variance
        if extract_data[0]['paragraphData1']['HeaderText'] == "YTD variance analysis by Profit Center":
            title = "Monthly Variance Analysis by Profit Center and GL Account Name"

            header1 = "Variance analysis by Profit Center"
            header2 = "Variance analysis by GL Account"

            desc1 = extract_data[0]['paragraphData1']['paragraphText1']
            desc2 = extract_data2[0]['paragraphData2']['paragraphText2']

            chart_title1 = extract_data[0]['paragraphData1']['Chart1']['chartTitle']
            chart_title2 = extract_data2[0]['paragraphData2']['Chart2']['chartTitle']

            acc_name_prof = extract_data[0]['paragraphData1']['Chart1']['chartData']['X_axis']
            value_prof = extract_data[0]['paragraphData1']['Chart1']['chartData']['Y_axis']

            fig1 = go.Figure(go.Waterfall(
                name=f"{head}",
                measure=["absolute"] + ["relative"] * (len(acc_name_prof) - 2) + ['total'],
                x=acc_name_prof,
                y=value_prof,
                textposition="outside",
                connector={"line": {"color": "rgb(63, 63, 63)"}},
            ))

            acc_name_gl = extract_data2[0]['paragraphData2']['Chart2']['chartData']['X_axis']
            value_gl = extract_data2[0]['paragraphData2']['Chart2']['chartData']['Y_axis']

            fig2 = go.Figure(go.Waterfall(
                name=f"{head}",
                measure=["absolute"] + ["relative"] * (len(acc_name_gl) - 2) + ['total'],
                x=acc_name_gl,
                y=value_gl,
                textposition="outside",
                connector={"line": {"color": "rgb(63, 63, 63)"}},
            ))

            return title, header1, header2, desc1, desc2, chart_title1, chart_title2, fig1, fig2

        #YTD Decomposition
        if extract_data[0]['paragraphData1']['HeaderText'] == "YTD Profit Center Breakdown":
            title = "YTD Decomposition Analysis by Profit Center and GL Account Name"

            header1 = "Decomposition analysis by Profit Center"
            header2 = "Decomposition analysis by GL Account"

            desc1 = extract_data[0]['paragraphData1']['paragraphText1']
            desc2 = extract_data2[0]['paragraphData2']['paragraphText2']

            chart_title1 = extract_data[0]['paragraphData1']['Chart1']['chartTitle']
            chart_title2 = extract_data2[0]['paragraphData2']['Chart2']['chartTitle']

            labels_prof = extract_data[0]['paragraphData1']['Chart1']['chartdata']['X_axis']
            values_prof = extract_data[0]['paragraphData1']['Chart1']['chartdata']['Y_axis']

            fig1 = go.Figure(data=[go.Pie(labels=labels_prof, values=values_prof, hole=.3)])

            labels_gl = extract_data2[0]['paragraphData2']['Chart2']['chartdata']['X_axis']
            values_gl = extract_data2[0]['paragraphData2']['Chart2']['chartdata']['Y_axis']

            fig2 = go.Figure(data=[go.Bar(name="GL Accounts", x=labels_gl, y=values_gl)])

            return title, header1, header2, desc1, desc2, chart_title1, chart_title2, fig1, fig2