#!/usr/bin/env python
# coding: utf-8

# In[18]:


import pandas as pd
# import numpy as np
# from scipy import stats
# import plotly.graph_objects as go
from mindmap.openai_text_summarization import generate_response as grs
import warnings

warnings.filterwarnings('ignore')

pd.set_option('display.max_columns', 100)

from mindmap.chunk_automation_wc import get_first_period

import mindmap.chunk_automation_wc as ca


# # Trend Analysis

# ### Monthly Trend Analysis

# In[2]:


def trend_analysis_monthly(df, period, head):
    """
        This function returns line chart data for monthly trend analysis, (from start of the year to the selected period).

        Aurguments:
            df: DataFrame
            period: Year Period

    """

    x_ax, y_ax = ca.trnd_var(df, period)

    trend_analysis_monthly_nan = [{
        "paragraphData1": {
            "paragraphID": 1,
            "HeaderText": "Monthly Trend Variance Analysis",
            "paragraphText1": grs(ca.trend_analysis_para(df, period, head)),
            "Chart1": {
                "chartType": "line",
                "chartTitle": f"Monthly {head} Trend for 2023",
                "chartData": {
                    "X_axis": x_ax,
                    "Y_axis": y_ax,
                    "chartXAxisLabel": "Month-Year",
                    "chartYAxisLabel": f"{head} (Millions)"

                }
            }
        }
    }]

    return trend_analysis_monthly_nan,None


# In[3]:


def trend_analysis_26_rolling(df, period, head):
    """
        This function returns line chart data for 26 rolling trend analysis.

        Aurguments:
            df: DataFrame
            period: Year Period

    """

    x_ax, y_ax = ca.trend_26(df, period)
    roll_avg = ca.roll_avg(df, period)
    summ_para = grs(ca.trend_analysis_para(df, period, head))

    trend_variance_analysis_26 = [{
        "paragraphData1": {
            "paragraphID": 1,
            "HeaderText": "Trend Analysis Monthly",
            "paragraphText1": summ_para,
            "Chart1": {
                "chartType": "line",
                "chartTitle": f"YTD {head} Trend Analysis",
                "chartData": {
                    "X_axis": x_ax,
                    "Y_axis": y_ax,
                    "chartXAxisLabel": "Month-Year",
                    "chartYAxisLabel": f"{head} (Millions)",
                    "BaseLine": roll_avg,
                    "BaseLineText": "Rolling Average",
                }
            }

        }
    }]

    return trend_variance_analysis_26,None


# In[ ]:


# # Variance Analysis

# In[16]:


def monthly_variance_analysis(df, period, head):
    """
        This Function will return overall monthly Variance analysis
        Including Profit Center & Gl Account Name

    """

    # For Profit Center
    data_pr, x_ax_pr, y_ax_pr, _, _ = ca.monthly_var_decom_prof(df, period)
    prof_summ = grs(ca.var_decom_para_creation('month', 'Profit Center', data_pr, 'var', head))

    prof_monthly_variance_analysis_df = [{"paragraphData1": {
        "paragraphID": 1,
        "HeaderText": "Monthly variance analysis by Profit center",
        "paragraphText1": prof_summ,
        "Chart1": {
            "chartType": "bridge chart",
            "chartTitle": "Bridge Chart - Profit center variance analysis",
            "chartData": {
                "X_axis": x_ax_pr,
                "Y_axis": y_ax_pr
            }

        }
    }
    }]

    # For GL Account Names
    data_gl, x_ax_gl, y_ax_gl, _, _ = ca.monthly_var_decom_gl(df, period)
    gl_summ = grs(ca.var_decom_para_creation('month', 'GL Account', data_gl, 'var', head))

    gl_monthly_variance_analysis_df = [{"paragraphData2": {
        "paragraphID": 2,
        "HeaderText": "Monthly variance analysis by GL Account",
        "paragraphText2": gl_summ,
        "Chart2": {
            "chartType": "bridge chart",
            "chartTitle": "Bridge Chart - GL Account variance analysis",
            "chartData": {
                "X_axis": x_ax_gl,
                "Y_axis": y_ax_gl
            }

        }
    }
    }]

    return prof_monthly_variance_analysis_df, gl_monthly_variance_analysis_df


# #### Only Profit

# In[5]:


def monthly_var_analysis_profit(df, period, head):
    """
        This Function Will Return Monthly Variance Analysis for Profit Center
    """

    # For Profit Center
    data_pr, x_ax_pr, y_ax_pr, _, _ = ca.monthly_var_decom_prof(df, period)
    prof_summ = grs(ca.var_decom_para_creation('month', 'Profit Center', data_pr, 'var', head))

    prof_monthly_variance_analysis_df = [{"paragraphData1": {
        "paragraphID": 1,
        "HeaderText": "Monthly variance analysis by Profit center",
        "paragraphText1": prof_summ,
        "Chart1": {
            "chartType": "bridge chart",
            "chartTitle": "Bridge Chart - Profit center variance analysis",
            "chartData": {
                "X_axis": x_ax_pr,
                "Y_axis": y_ax_pr
            }

        }
    }
    }]

    return prof_monthly_variance_analysis_df,None


# #### Only GL

# In[17]:


def monthly_var_analysis_gl(df, period, head):
    """
        This Function Will Return Monthly Variance Analysis for GL Account Name
    """

    # For GL Account Names
    data_gl, x_ax_gl, y_ax_gl, _, _ = ca.monthly_var_decom_gl(df, period)
    gl_summ = grs(ca.var_decom_para_creation('month', 'GL Account', data_gl, 'var', head))

    gl_monthly_variance_analysis_df = [{"paragraphData1": {
        "paragraphID": 1,
        "HeaderText": "Monthly variance analysis by GL Account",
        "paragraphText1": gl_summ,
        "Chart1": {
            "chartType": "bridge chart",
            "chartTitle": "Bridge Chart - GL Account variance analysis",
            "chartData": {
                "X_axis": x_ax_gl,
                "Y_axis": y_ax_gl
            }

        }
    }
    }]

    return gl_monthly_variance_analysis_df,None


# ### YTD

# In[7]:


def ytd_variance_analysis(df, period, head):
    """
        This Function will return overall Variance analysis at YTD level
        Including Profit Center & Gl Account Name

    """

    # For Profit Center
    data_prof, x_ax_prof, y_ax_prof, _, _ = ca.ytd_var_decom_prof(df, period)
    prof_summ = grs(ca.var_decom_para_creation('ytd', 'Profit Center', data_prof, 'var', head))

    ytd_variance_analysis_df_prof = [{"paragraphData1": {
        "paragraphID": 1,
        "HeaderText": "YTD variance analysis by Profit Center",
        "paragraphText1": prof_summ,
        "Chart1": {
            "chartType": "bridge chart",
            "chartTitle": "Bridge Chart - YTD Profit Center variance analysis",
            "chartData": {
                "X_axis": x_ax_prof,
                "Y_axis": y_ax_prof}}}}]

    # For Gl Account Name
    data_gl, x_ax_gl, y_ax_gl, _, _ = ca.ytd_var_decom_gl(df, period)
    gl_summ = grs(ca.var_decom_para_creation('ytd', 'GL Account', data_gl, 'var', head))

    ytd_variance_analysis_df_gl = [{"paragraphData2": {
        "paragraphID": 2,
        "HeaderText": "YTD variance analysis by GL Account",
        "paragraphText2": gl_summ,
        "Chart2": {
            "chartType": "bridge chart",
            "chartTitle": "Bridge Chart - YTD GL Account variance analysis",
            "chartData": {
                "X_axis": x_ax_gl,
                "Y_axis": y_ax_gl}}}}]

    return ytd_variance_analysis_df_prof, ytd_variance_analysis_df_gl


# #### Only Profit

# In[8]:


def ytd_variance_analysis_profit(df, period, head):
    """
        This function will return Variance Analysis for Profit Center at YTD level
    """

    # For Profit Center
    data_prof, x_ax_prof, y_ax_prof, _, _ = ca.ytd_var_decom_prof(df, period)
    prof_summ = grs(ca.var_decom_para_creation('ytd', 'Profit Center', data_prof, 'var', head))

    ytd_variance_analysis_df_prof = [{"paragraphData1": {
        "paragraphID": 1,
        "HeaderText": "YTD variance analysis by Profit Center",
        "paragraphText1": prof_summ,
        "Chart1": {
            "chartType": "bridge chart",
            "chartTitle": "Bridge Chart - YTD Profit Center variance analysis",
            "chartData": {
                "X_axis": x_ax_prof,
                "Y_axis": y_ax_prof}}}}]

    return ytd_variance_analysis_df_prof,None


# #### Only GL

# In[19]:


def ytd_variance_analysis_gl(df, period, head):
    """
        This function will return Variance Analysis for GL Account Name at YTD level
    """

    # For Gl Account Name
    data_gl, x_ax_gl, y_ax_gl, _, _ = ca.ytd_var_decom_gl(df, period)
    gl_summ = grs(ca.var_decom_para_creation('ytd', 'GL Account', data_gl, 'var', head))

    ytd_variance_analysis_df_gl = [{"paragraphData1": {
        "paragraphID": 1,
        "HeaderText": "YTD variance analysis by GL Account",
        "paragraphText1": gl_summ,
        "Chart1": {
            "chartType": "bridge chart",
            "chartTitle": "Bridge Chart - YTD GL Account variance analysis",
            "chartData": {
                "X_axis": x_ax_gl,
                "Y_axis": y_ax_gl}}}}]

    return ytd_variance_analysis_df_gl,None


# # Decomposition

# In[10]:


def monthly_decom(df, period, head):
    """
        This Function will return overall Decomposition Breakdown analysis at monthly level
        Including Profit Center & Gl Account Name

    """

    # Creating variable for profit center
    data_prof, _, _, pie_x_prof, pie_y_prof = ca.monthly_var_decom_prof(df, period)
    prof_summ = grs(ca.var_decom_para_creation('month', 'Profit Center', data_prof, 'decom', head))

    # Pie Chart for Profit Center
    decomposition_monthly_prof_pie = [
        {"paragraphData1": {
            "paragraphID": 1,

            "HeaderText": "Monthly Profit Center Breakdown",
            "paragraphText1": prof_summ,
            "Chart1": {

                "chartType": "pie",
                "chartTitle": "Monthly Profit Center Breakdown",
                "chartdata": {
                    "X_axis": pie_x_prof,
                    "Y_axis": pie_y_prof
                }
            }
        }}]
    # Creating variable for GL Account
    data_gl, _, _, pie_x_gl, pie_y_gl = ca.monthly_var_decom_gl(df, period)
    gl_summ = grs(ca.var_decom_para_creation('month', 'GL Account', data_gl, 'decom', head))

    # Pie Chart for GL Account Name
    decomposition_monthly_gl_pie = [
        {"paragraphData2": {
            "paragraphID": 2,

            "HeaderText": "Monthly GL Account Breakdown",
            "paragraphText2": gl_summ,
            "Chart2": {

                "chartType": "pie",
                "chartTitle": "Monthly GL Account Breakdown",
                "chartdata": {
                    "X_axis": pie_x_gl,
                    "Y_axis": pie_y_gl
                }
            }
        }}]

    return decomposition_monthly_prof_pie, decomposition_monthly_gl_pie


# #### Only Profit

# In[20]:


def monthly_decom_profit(df, period, head):
    """This Function will return Decomposition Breakdown analysis for Profit Center at monthly level"""

    # Creating variable for profit center
    data_prof, _, _, pie_x_prof, pie_y_prof = ca.monthly_var_decom_prof(df, period)
    prof_summ = grs(ca.var_decom_para_creation('month', 'Profit Center', data_prof, 'decom', head))

    # Pie Chart for Profit Center
    decomposition_monthly_prof_pie = [
        {"paragraphData1": {
            "paragraphID": 1,

            "HeaderText": "Monthly Profit Center Breakdown",
            "paragraphText1": prof_summ,
            "Chart1": {

                "chartType": "pie",
                "chartTitle": "Monthly Profit Center Breakdown",
                "chartdata": {
                    "X_axis": pie_x_prof,
                    "Y_axis": [round(i, 2) for i in pie_y_prof]
                }
            }
        }}]

    return decomposition_monthly_prof_pie,None


# #### Only GL

# In[21]:


def monthly_decom_gl(df, period, head):
    """This Function will return Decomposition Breakdown analysis for GL Account Name at monthly level"""

    data_gl, _, _, pie_x_gl, pie_y_gl = ca.monthly_var_decom_gl(df, period)
    gl_summ = grs(ca.var_decom_para_creation('month', 'GL Account', data_gl, 'decom', head))

    # Pie Chart for GL Account Name
    decomposition_monthly_gl_pie = [
        {"paragraphData1": {
            "paragraphID": 1,

            "HeaderText": "Monthly GL Account Breakdown",
            "paragraphText1": gl_summ,
            "Chart1": {

                "chartType": "pie",
                "chartTitle": "Monthly GL Account Breakdown",
                "chartdata": {
                    "X_axis": pie_x_gl,
                    "Y_axis": [round(i, 2) for i in pie_y_gl]
                }
            }
        }}]

    return decomposition_monthly_gl_pie,None


# ## YTD Decomposition

# In[22]:


def ytd_decom(df, period, head):
    """
        This Function will return overall Decomposition Breakdown analysis at YTD level
        Including Profit Center & Gl Account Name

    """

    # Creating variable for profit center
    data_prof, _, _, pie_x_prof, pie_y_prof = ca.ytd_var_decom_prof(df, period)
    prof_summ = grs(ca.var_decom_para_creation('ytd', 'Profit Center', data_prof, 'decom', head))

    # Pie Chart for Profit Center
    decomposition_ytd_prof_pie = [
        {"paragraphData1": {
            "paragraphID": 1,

            "HeaderText": "YTD Profit Center Breakdown",
            "paragraphText1": prof_summ,
            "Chart1": {

                "chartType": "pie",
                "chartTitle": "YTD Profit Center Breakdown",
                "chartdata": {
                    "X_axis": pie_x_prof,
                    "Y_axis": [round(i, 2) for i in pie_y_prof]
                }
            }
        }}]
    # Creating variable for GL Account
    data_gl, _, _, pie_x_gl, pie_y_gl = ca.ytd_var_decom_gl(df, period)
    gl_summ = grs(ca.var_decom_para_creation('ytd', 'GL Account', data_gl, 'decom', head))

    # Pie Chart for GL Account Name
    decomposition_ytd_gl_pie = [
        {"paragraphData2": {
            "paragraphID": 2,

            "HeaderText": "YTD GL Account Breakdown",
            "paragraphText2": gl_summ,
            "Chart2": {

                "chartType": "pie",
                "chartTitle": "YTD GL Account Breakdown",
                "chartdata": {
                    "X_axis": pie_x_gl,
                    "Y_axis": [round(i, 2) for i in pie_y_gl]
                }
            }
        }}]

    return decomposition_ytd_prof_pie, decomposition_ytd_gl_pie


# #### Only Profit

# In[23]:


def ytd_decom_prof(df, period, head):
    """This function will return Decomposition analysis for Profit Center at YTD level"""

    # Creating variable for profit center
    data_prof, _, _, pie_x_prof, pie_y_prof = ca.ytd_var_decom_prof(df, period)
    prof_summ = grs(ca.var_decom_para_creation('ytd', 'Profit Center', data_prof, 'decom', head))

    # Pie Chart for Profit Center
    decomposition_ytd_prof_pie = [
        {"paragraphData1": {
            "paragraphID": 1,

            "HeaderText": "YTD Profit Center Breakdown",
            "paragraphText1": prof_summ,
            "Chart1": {

                "chartType": "pie",
                "chartTitle": "YTD Profit Center Breakdown",
                "chartdata": {
                    "X_axis": pie_x_prof,
                    "Y_axis": [round(i, 2) for i in pie_y_prof]
                }
            }
        }}]

    return decomposition_ytd_prof_pie,None


# #### Only gl

# In[24]:


def ytd_decom_gl(df, period, head):
    """This function will return Decomposition analysis for GL Account Name at YTD level"""

    # Creating variable for GL Account
    data_gl, _, _, pie_x_gl, pie_y_gl = ca.ytd_var_decom_gl(df, period)
    gl_summ = grs(ca.var_decom_para_creation('ytd', 'GL Account', data_gl, 'decom', head))

    # Pie Chart for GL Account Name
    decomposition_ytd_gl_pie = [
        {"paragraphData1": {
            "paragraphID": 1,

            "HeaderText": "YTD GL Account Breakdown",
            "paragraphText1": gl_summ,
            "Chart1": {

                "chartType": "pie",
                "chartTitle": "YTD GL Account Breakdown",
                "chartdata": {
                    "X_axis": pie_x_gl,
                    "Y_axis": [round(i, 2) for i in pie_y_gl]
                }
            }
        }}]

    return decomposition_ytd_gl_pie,None




