import mindmap.chart_data as cd

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

def data_extract(df,dd):
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

    elif dd['year'] != 'nan' and dd['period'] == 'nan':
        yp = int(dd['year'] + '009')

    elif dd['year'] == 'nan' and dd['period'] != 'nan':
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
            result1, result2 = cd.trend_analysis_monthly(df, yp, 'GSV')
            return result1, result2

        ## Varince Analysis
        if dd['analysis'] == 'Variance':
            if dd['breakdown'] == 'nan':
                result1, result2 = cd.monthly_variance_analysis(df, yp, 'GSV')
                return result1, result2

        if dd['analysis'] == 'Variance':
            if dd['breakdown'] == 'Profit Center':
                result1, result2 = cd.monthly_var_analysis_profit(df, yp, 'GSV')
                return result1, result2

        if dd['analysis'] == 'Variance':
            if dd['breakdown'] == 'GL Account Name':
                result1, result2 = cd.monthly_var_analysis_gl(df, yp, 'GSV')
                return result1, result2

        ## Decomposition Analysis
        if dd['analysis'] == 'Decomposition':
            if dd['breakdown'] == 'nan':
                result1, result2  = cd.monthly_decom(df, yp, 'GSV')
                return result1, result2

        if dd['analysis'] == 'Decomposition':
            if dd['breakdown'] == 'Profit Center':
                result1, result2 = cd.monthly_decom_profit(df, yp, 'GSV')
                return result1, result2

        if dd['analysis'] == 'Decomposition':
            if dd['breakdown'] == 'GL Account Name':
                result1, result2 = cd.monthly_decom_gl(df, yp, 'GSV')
                return result1, result2

    # YTD Analysis
    if dd['analysis_period'] == 'YTD':

        ## Trend Analysis
        if dd['analysis'] == 'Trend Analysis':
            result1, result2 = cd.trend_analysis_26_rolling(df, yp, 'GSV')
            return result1, result2

        ## Varince Analysis
        if dd['analysis'] == 'Variance':
            if dd['breakdown'] == 'nan':
                result1, result2  = cd.ytd_variance_analysis(df, yp, 'GSV')
                return result1, result2

        if dd['analysis'] == 'Variance':
            if dd['breakdown'] == 'Profit Center':
                result1, result2 = cd.ytd_variance_analysis_profit(df, yp, 'GSV')
                return result1, result2

        if dd['analysis'] == 'Variance':
            if dd['breakdown'] == 'GL Account Name':
                result1, result2 = cd.ytd_variance_analysis_gl(df, yp, 'GSV')
                return result1, result2

        ## Decomposition Analysis
        if dd['analysis'] == 'Decomposition':
            if dd['breakdown'] == 'nan':
                result1, result2  = cd.ytd_decom(df, yp, 'GSV')
                return result1, result2

        if dd['analysis'] == 'Decomposition':
            if dd['breakdown'] == 'Profit Center':
                result1, result2 = cd.ytd_decom_prof(df, yp, 'GSV')
                return result1, result2

        if dd['analysis'] == 'Decomposition':
            if dd['breakdown'] == 'GL Account Name':
                result1, result2 = cd.ytd_decom_gl(df, yp, 'GSV')
                return result1, result2
