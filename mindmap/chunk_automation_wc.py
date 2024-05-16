#!/usr/bin/env python
# coding: utf-8

# In[36]:


# from tkinter import Y
import pandas as pd
import numpy as np
from scipy import stats
import warnings

warnings.filterwarnings('ignore')


# In[37]:


# To get the first period of the year
def get_first_period(selected_period):
    """return:
            frist_period: This Function will return first period of the year
                          eg: 2023009 -> 2023001
        Aurgument:
            selected_period: year period

    """

    selected_period = str(selected_period)
    year = selected_period[:4]
    first_period = year + "001"

    if selected_period != first_period:
        return int(first_period)
    else:
        return None


# To get previous period
def get_previous_period(df, selected_period):
    """
       return:
           previous_period: This function will return previous period
                            eg: 2023009 -> 2023008

        Aurguments:
            df: DataFrame
            selected_period: Year Period
    """

    yp_list = sorted(df['Period/Year'].unique().tolist())
    number_to_previous = {yp_list[i]: yp_list[i - 1] for i in range(1, len(yp_list))}

    #     print(number_to_previous)
    if selected_period in number_to_previous:
        return number_to_previous[selected_period]
    else:
        return None


def trnd_var(df, period):
    """return:
            x_ax, y_ax: This function will return x-axis and y-axis data for line chart.
                        Data will plot a line chart from first period of the selected year till the selected year period
                        eg: if selected_year is 2023009, data will be from 2023001 till 2023009
        Aurguments:
            df: DataFrame
            period: Year Period, eg: 2023009
    """

    pr_data = df[(df['Period/Year'] >= get_first_period(period)) & (df['Period/Year'] <= period)].reset_index(drop=True)
    pr_agg = abs(pr_data.groupby(['Period/Year'])['Amount'].sum()).reset_index()

    x_ax, y_ax = list(pr_agg['Period/Year']), list(pr_agg['Amount'])

    return x_ax, y_ax


def roll_avg(df, period):
    """
        return:
            mean: This function will return rolling average for the selected period, window = 26

        Aurguments:
            df: DataFrame
            period: Year Period, eg: 2023009
    """

    gg = abs(df.groupby(['Period/Year'])['Amount'].sum().reset_index())
    window = 26
    #     gg['roll'] = gg['Amount'].rolling(window=26).mean()
    #     mean = gg[gg['Period/Year'] == period]['roll'].iloc[0]
    dd = gg[gg['Period/Year'] <= period]
    prev_period = dd.iloc[-(window)]['Period/Year']
    dd = gg[(gg['Period/Year'] >= prev_period) & (gg['Period/Year'] <= period)]

    dd["roll"] = dd['Amount'].rolling(window=window).mean()
    mean = dd[dd['Period/Year'] == period]['roll'].iloc[0]

    return mean


def trend_analysis_para(df, period, head):
    """
        return:
            final_para: This function will return a basic structured paragraph related to the trend analysis for the selected year period.
            Which includes rolling average, Confidence interval, Variantion with previous month & Variation with last year same month with selcted month.

        Aurguments:
            df: DataFrame
            period: Year Period
            head: NSV/GSV ....

    """

    # Data Creation
    agg = abs(df.groupby(['Period/Year'])[['Amount']].sum().reset_index())

    # Calculating Confidence Interval
    agg['CI_lower'] = np.nan
    agg['CI_upper'] = np.nan

    rolling_window_size = 26
    confidence_level = 0.95

    for i in range(len(agg)):
        if i >= rolling_window_size - 1:
            window_data = agg.loc[i - rolling_window_size + 1: i, 'Amount']
            mean = window_data.mean()
            std_dev = window_data.std()
            length = len(window_data)

            # Calculate confidence intervals
            degrees_of_freedom = length - 1
            critical_value = stats.t.ppf((1 + confidence_level) / 2, degrees_of_freedom)
            standard_error = std_dev / np.sqrt(length)
            margin_of_error = critical_value * standard_error

            lower_bound = mean - margin_of_error
            upper_bound = mean + margin_of_error

            # Update the CI_lower and CI_upper columns
            agg.at[i, 'CI_lower'] = lower_bound
            agg.at[i, 'CI_upper'] = upper_bound

    # Whether Under Confidance Interval or not
    agg['Under Confidance Interval or not'] = agg.apply(
        lambda row: 'Yes' if row['Amount'] >= row['CI_lower'] and row['Amount'] <= row['CI_upper'] else 'No', axis=1)

    # Calculating Last month Variance
    agg['percentage of variance with last month'] = np.nan
    for i in range(1, len(agg)):
        agg['percentage of variance with last month'][i] = ((agg['Amount'][i] - agg['Amount'][i - 1]) / agg['Amount'][
            i]) * 100
    agg['percentage of variance with same month last year'] = ((agg['Amount'] - agg['Amount'].shift(periods=13)) / agg[
        'Amount']) * 100

    # Calculating Rolling Average
    agg['Rolling Avg'] = agg['Amount'].rolling(window=26).mean()
    agg['Rolling Avg'] = agg['Rolling Avg'].fillna(0).apply(lambda x: round(x, 1))

    # Monthly Difference
    agg['amount diff monthly'] = np.nan
    for i in range(1, len(agg)):
        agg['amount diff monthly'][i] = agg['Amount'][i] - agg['Amount'][i - 1]
    agg['amount diff monthly'] = agg['amount diff monthly'].apply(lambda x: round(x, 1))

    # Yearly Difference
    agg['Amount Diff Yearly'] = ((agg['Amount'] - agg['Amount'].shift(periods=13)))

    # creating dict
    filerted_df = agg[agg['Period/Year'] == period].reset_index(drop=True)

    conf = filerted_df['Under Confidance Interval or not'][0]
    roll = 'under window' if filerted_df['Rolling Avg'][0] == 0 else f"{filerted_df['Rolling Avg'][0] / 1000000:.2f}M"
    per_var_month = "Previous month is not available" if np.isnan(filerted_df['percentage of variance with last month'][
                                                                      0]) else f"{round(filerted_df['percentage of variance with last month'][0], 2)}%"
    var_mon_val = "Previous month is not available" if np.isnan(
        filerted_df['amount diff monthly'][0]) else f"{filerted_df['amount diff monthly'][0] / 1000000:.2f}M"
    per_var_yr = "Previous year data is not available" if np.isnan(
        filerted_df['percentage of variance with same month last year'][
            0]) else f"{round(filerted_df['percentage of variance with same month last year'][0], 2)}%"
    var_yr_val = "Previous year data is not available" if np.isnan(
        filerted_df['Amount Diff Yearly'][0]) else f"{filerted_df['Amount Diff Yearly'][0] / 1000000:.2f}M"

    final_pgraph = f"{head} trend for the current month is {'not' if conf == 'No' else ''} in the confidence interval.\
    Rolling Average: The rolling average of {head} for all months until now is {roll}.\
    Month-to-Month Variation: The {head} is {var_mon_val} from the previous month with {per_var_month}.\
    Year-to-Year Variation: Compared to the same month last year, the {head} is {var_yr_val},with {per_var_yr}. "

    return final_pgraph


## Value for 26 moving period
def trend_26(df, selected_period):
    """
        return: This function will return 26 rolling period x-axis and y-axis data for line chart to analyse the trend.
            x_ax
            y_ax

        Aurguments:
            df: DataFrame
            selected_period: Year Period, eg: 2023009

    """

    agge = df[df['Period/Year'] <= selected_period].reset_index()
    agge = abs(agge.groupby(['Period/Year'])['Amount'].sum()).reset_index()
    agge = agge.iloc[-26:].reset_index(drop=True)

    x_ax, y_ax = list(agge['Period/Year']), list(agge['Amount'])

    return x_ax, y_ax


# In[ ]:


def var_decom_para_creation(mode, brk, data, analysis_type, head):
    """
        return:
            paragraph: This function will return basic structured data for variance and decomposition analysis.

        Aurguments:
            mode: month/ytd,
            brk: Profit Center / GL Account Name
            data: data will be returned from var_decom function
            head: 'NSV'/'GSV etc...
            analysis_type: var/ decom

    """
    paragraph = ""
    if analysis_type == 'var':
        header = []
        if mode == 'month':
            text = f"Variance decomposition for {brk} at current month:"
            header.append(text)
        if mode == 'ytd':
            text = f"Variance Decomposition for {brk} at YTD level:"
            header.append(text)
        for k, v in data.items():
            new = f"* {k} at {v[0]}% which amounts to {v[1] / 1000000:.2f}M to {head}"
            header.append(new)

        paragraph = " ".join(header)

    elif analysis_type == 'decom':
        header = []
        if mode == 'month':
            text = f"One of the decomposition mechanism is {brk}. {brk} Breakdown for current month:"
            header.append(text)
        if mode == 'ytd':
            text = f"One of the decomposition mechanism is {brk}. {brk} Breakdown at YTD level:"
            header.append(text)
        for k, v in data.items():
            new = f"* {k} contributes {v[0]}% to {head}."
            header.append(new)

        paragraph = " ".join(header)

    return paragraph


# In[ ]:


def monthly_var_decom_prof(df, period, analysis_type='var'):
    """
        This function is for monthly variance and decomposition analysis for profit center,
        It will return:
            data: this data will help to create paragraph
            x_ax: analysis data for bridge chart(X-AXIS)
            y_ax: analysis data for bridge chart(Y-AXIS)
            pie_x: analysis data for pie chart
            pie_y: analysis data for pie chart

        Aurguments:
            df: DataFrame
            period: Year Period to be analyzed eg: 2023009
            analysis_type: var/decom, var is for variance, decom is decomposition

    """
    curr_yp = period
    prev_yp = get_previous_period(df, curr_yp)

    if prev_yp is not None:

        agg = df.groupby(['Period/Year', 'Profit_Center_Desc'])['Amount'].sum().reset_index()
        # total value for current month and previous month
        curr_val = agg[(agg['Period/Year'] == curr_yp)]['Amount'].sum()
        prev_val = agg[(agg['Period/Year'] == prev_yp)]['Amount'].sum()

        curr_val = abs(round(curr_val, 2))
        prev_val = abs(round(prev_val, 2))

        variance = curr_val - prev_val

        currmonth = agg[(agg['Period/Year'] == curr_yp)]
        prev_mon = agg[(agg['Period/Year'] == prev_yp)]

        curr_df = currmonth.groupby(['Profit_Center_Desc'])['Amount'].sum().reset_index()
        prev_df = prev_mon.groupby(['Profit_Center_Desc'])['Amount'].sum().reset_index()

        merged_df = pd.merge(curr_df, prev_df, on='Profit_Center_Desc', suffixes=('_curr', '_prev'), how='outer')
        merged_df = merged_df.fillna(0)
        merged_df['Amount_Difference'] = merged_df['Amount_curr'] - merged_df['Amount_prev']

        x_ax = ['Previous Period']
        y_ax = [prev_val]

        data = {}

        # Creating data for pie chart
        pie_df = {}
        for i in range(len(merged_df)):
            val_change = merged_df['Amount_Difference'][i]
            per_change = (merged_df['Amount_Difference'][i] / variance) * 100

            if np.isnan(val_change) | np.isnan(per_change) | (per_change < 1):
                #Exxt----
                data[merged_df['Profit_Center_Desc'][i]] = [round(per_change, 2), round(val_change, 2)]
                x_ax.append(merged_df['Profit_Center_Desc'][i])
                y_ax.append(round(val_change, 2))
                #----
                if 'others' not in (pie_df.keys()):
                    pie_df['others'] = round(per_change, 2)
                else:
                    pie_df['others'] += round(per_change, 2)
            else:
                x_ax.append(merged_df['Profit_Center_Desc'][i])
                y_ax.append(round(val_change, 2))

                # Check for type of analysis
                if analysis_type == 'var':
                    data[merged_df['Profit_Center_Desc'][i]] = [round(per_change, 2), round(val_change, 2)]
                elif analysis_type == 'decom':
                    data[merged_df['Profit_Center_Desc'][i]] = round(per_change, 2)

                pie_df[merged_df['Profit_Center_Desc'][i]] = round(per_change, 2)

        x_ax.append('Current Period')
        y_ax.append(curr_val)

        ## Ext----
        y_ax = [y_ax[0]] + [-1 * x for x in y_ax[1:-1]] + [y_ax[-1]]
        ##-----

        pie_x = list(pie_df.keys())
        pie_y = [round(i, 2) for i in pie_df.values()]

        return data, x_ax, y_ax, pie_x, pie_y
    else:
        print("Previous period is not available.")


# In[ ]:


def monthly_var_decom_gl(df, period, analysis_type='var'):
    """
        This function is for monthly variance and decomposition analysis for GL Account Name,
        It will return:
            data: this data will help to create paragraph
            x_ax: analysis data for bridge chart(X-AXIS)
            y_ax: analysis data for bridge chart(Y-AXIS)
            pie_x: analysis data for pie chart
            pie_y: analysis data for pie chart

        Aurguments:
            df: DataFrame
            period: Year Period to be analyzed eg: 2023009
            analysis_type: default(var), var/decom, var is for variance, decom is decomposition

    """

    curr_yp = period
    prev_yp = get_previous_period(df, period)
    if prev_yp is not None:

        agg = df.groupby(['Period/Year', 'GL_Account_Name'])['Amount'].sum().reset_index()
        # agg = abs(agg)
        # total value for current month and previous month
        curr_val = agg[(agg['Period/Year'] == curr_yp)]['Amount'].sum()
        prev_val = agg[(agg['Period/Year'] == prev_yp)]['Amount'].sum()


        curr_val = abs(round(curr_val, 2))
        prev_val = abs(round(prev_val, 2))

        variance = curr_val - prev_val

        currmonth = agg[(agg['Period/Year'] == curr_yp)]
        prev_mon = agg[(agg['Period/Year'] == prev_yp)]

        curr_df = currmonth.groupby(['GL_Account_Name'])['Amount'].sum().reset_index()
        prev_df = prev_mon.groupby(['GL_Account_Name'])['Amount'].sum().reset_index()

        merged_df = pd.merge(curr_df, prev_df, on='GL_Account_Name', suffixes=('_curr', '_prev'), how='outer')
        merged_df['Amount_Difference'] = merged_df['Amount_curr'] - merged_df['Amount_prev']

        x_ax = ['Previous Period']
        y_ax = [prev_val]

        data = {}

        # Creating data for pie chart
        pie_df = {}
        for i in range(len(merged_df)):
            val_change = merged_df['Amount_Difference'][i]
            per_change = (merged_df['Amount_Difference'][i] / variance) * 100

            if np.isnan(val_change) | np.isnan(per_change) | (per_change < 5):
                # Extention------
                data[merged_df['GL_Account_Name'][i]] = [round(per_change, 2), round(val_change, 2)]
                x_ax.append(merged_df['GL_Account_Name'][i])
                y_ax.append(round(val_change, 2))
                # -------
                if 'others' not in (pie_df.keys()):

                    pie_df['others'] = round(per_change, 2)
                else:
                    pie_df['others'] += round(per_change, 2)
            else:
                x_ax.append(merged_df['GL_Account_Name'][i])
                y_ax.append(round(val_change, 2))

                if analysis_type == 'var':
                    data[merged_df['GL_Account_Name'][i]] = [round(per_change, 2), round(val_change, 2)]
                elif analysis_type == 'decom':
                    data[merged_df['GL_Account_Name'][i]] = round(per_change, 2)

                pie_df[merged_df['GL_Account_Name'][i]] = round(per_change, 2)

        x_ax.append('Current Period')
        y_ax.append(curr_val)

        # Ext----
        y_ax = [y_ax[0]]+[-1 * x for x in y_ax[1:-1]] + [y_ax[-1]]
        #-----
        pie_x = list(pie_df.keys())
        pie_y = [round(i, 2) for i in pie_df.values()]

        return data, x_ax, y_ax, pie_x, pie_y


# In[ ]:


def ytd_var_decom_prof(df, period, analysis_type='var'):
    """
        This function is for YTD variance and decomposition analysis for Profit center,
        It will return:
            data: this data will help to create paragraph
            x_ax: analysis data for bridge chart(X-AXIS)
            y_ax: analysis data for bridge chart(Y-AXIS)
            pie_x: analysis data for pie chart
            pie_y: analysis data for pie chart

        Aurguments:
            df: DataFrame
            period: Year Period to be analyzed eg: 2023009
            analysis_type: default(var), var/decom, var is for variance, decom is decomposition

    """

    curr_yp = period
    first_yp = get_first_period(period)

    if first_yp is not None:

        agg = abs(df.groupby(['Period/Year', 'Profit_Center_Desc'])['Amount'].sum()).reset_index()
        agg = agg[(agg['Period/Year'] >= first_yp) & (agg['Period/Year'] <= curr_yp)].reset_index()
        # total value for current month and previous month
        total_val = agg['Amount'].sum()
        first_val = agg[(agg['Period/Year'] == first_yp)]['Amount'].sum()

        total_val = round(total_val, 2)
        first_val = round(first_val, 2)

        var = total_val - first_val

        # Calculating total for every PCD
        prof = agg['Profit_Center_Desc'].unique().tolist()

        total = {}
        for i in prof:
            total[i] = agg[agg['Profit_Center_Desc'] == i]['Amount'].sum()

        first = {}
        for i in prof:
            first[i] = agg[(agg['Period/Year'] == first_yp) & (agg['Profit_Center_Desc'] == i)]['Amount'].sum()

        # Calculating Diff
        diff = {}
        for key in total:
            difference = total[key] - first[key]
            diff[key] = difference

        # Calculating Parcentage
        x_ax = ['First Period']
        y_ax = [first_val]

        data = {}

        pie_df = {}

        for key, val in diff.items():
            per = (val / var) * 100
            if (np.isnan(per)) or (per <= 1):
                if 'others' not in (pie_df.keys()):
                    pie_df['others'] = round(per, 2)
                else:
                    pie_df['others'] += round(per, 2)
            else:
                x_ax.append(key)
                y_ax.append(round(val, 2))

                if analysis_type == 'var':
                    data[key] = [round(per, 2), round(val, 2)]
                if analysis_type == 'decom':
                    data[key] = round(per, 2)

                pie_df[key] = round(per, 2)

        x_ax.append("Total")
        y_ax.append(total_val)

        pie_x = list(pie_df.keys())
        pie_y = [round(i, 2) for i in pie_df.values()]

        return data, x_ax, y_ax, pie_x, pie_y
    else:
        print("Period Not Available")


# In[ ]:


#### For GL Account Name

def ytd_var_decom_gl(df, period, analysis_type='var'):
    """
        This function is for YTD variance and decomposition analysis for GL Account Name,
        It will return:
            data: this data will help to create paragraph
            x_ax: analysis data for bridge chart(X-AXIS)
            y_ax: analysis data for bridge chart(Y-AXIS)
            pie_x: analysis data for pie chart
            pie_y: analysis data for pie chart

        Aurguments:
            df: DataFrame
            period: Year Period to be analyzed eg: 2023009
            analysis_type: default(var), var/decom, var is for variance, decom is decomposition

    """

    curr_yp = period
    first_yp = get_first_period(period)

    if first_yp is not None:

        agg = abs(df.groupby(['Period/Year', 'GL_Account_Name'])['Amount'].sum()).reset_index()
        agg = agg[(agg['Period/Year'] >= first_yp) & (agg['Period/Year'] <= curr_yp)].reset_index()
        # total value for current month and previous month
        total_val = agg['Amount'].sum()
        first_val = agg[(agg['Period/Year'] == first_yp)]['Amount'].sum()

        total_val = round(total_val, 2)
        first_val = round(first_val, 2)

        var = total_val - first_val

        # Calculating total for every PCD
        gl = agg['GL_Account_Name'].unique().tolist()

        total_gl = {}
        for i in gl:
            total_gl[i] = agg[agg['GL_Account_Name'] == i]['Amount'].sum()

        first_gl = {}
        for i in gl:
            first_gl[i] = agg[(agg['Period/Year'] == first_yp) & (agg['GL_Account_Name'] == i)]['Amount'].sum()

        # Calculating Diff
        diff = {}
        for key in total_gl:
            difference = total_gl[key] - first_gl[key]
            diff[key] = difference

        # Calculating Parcentage
        x_ax = ['First Period']
        y_ax = [first_val]

        data = {}

        pie_df = {}

        for key, val in diff.items():
            per = (val / var) * 100
            if (np.isnan(per)) or (per <= 1):
                if 'others' not in (pie_df.keys()):
                    pie_df['others'] = round(per, 2)
                else:
                    pie_df['others'] += round(per, 2)
            else:
                x_ax.append(key)
                y_ax.append(round(val, 2))

                if analysis_type == 'var':
                    data[key] = [round(per, 2), round(val, 2)]
                if analysis_type == 'decom':
                    data[key] = round(per, 2)

                pie_df[key] = round(per, 2)

        x_ax.append("Total")
        y_ax.append(total_val)

        pie_x = list(pie_df.keys())
        pie_y = [round(i, 2) for i in pie_df.values()]

        return data, x_ax, y_ax, pie_x, pie_y
    else:
        print("Period Not Available")


