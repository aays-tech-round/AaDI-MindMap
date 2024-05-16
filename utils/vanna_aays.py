from openai import AzureOpenAI
import streamlit as st
from vanna.openai import OpenAI_Chat
from vanna.chromadb import ChromaDB_VectorStore


OPENAI_API_KEY = '997acf70c60c4e858adbbbe7e3662817'
OPENAI_DEPLOYMENT_NAME = 'gpt35turbo-16k'
MODEL_NAME = 'gpt35turbo-16k'
api_version = '2023-09-15-preview'
azure_endpoint = 'https://openaiivadev.openai.azure.com/'
OPENAI_DEPLOYMENT_NAME_GPT4 = 'gpt4dev'

client = AzureOpenAI(
  azure_endpoint = azure_endpoint,
  api_key=OPENAI_API_KEY,
  api_version=api_version
)


class MyVanna(ChromaDB_VectorStore, OpenAI_Chat):
    def __init__(self, config=None):
        ChromaDB_VectorStore.__init__(self, config=config)
        OpenAI_Chat.__init__(self, client=AzureOpenAI(
                              azure_endpoint = azure_endpoint,
                              api_key=OPENAI_API_KEY,
                              api_version=api_version), config=config) # Make sure to put your AzureOpenAI client here

vn = MyVanna(config={'model': OPENAI_DEPLOYMENT_NAME_GPT4})

vn.connect_to_sqlite('iva_sample.db')

# vn.train(ddl=
#     """
# CREATE TABLE IF NOT EXISTS costs (
#     Level1 TEXT,
#     FY INTEGER,
#     Periods TEXT,
#     Current_Value REAL,
#     GSV REAL,
#     Anomaly BOOLEAN,
#     Confidence_Low REAL,
#     Confidence_High REAL
# )
#     """
# )
#
# queries = [
#     "SELECT SUM(Current_Value) FROM costs WHERE Level1 = 'Advertising & Consumer Promo' AND FY = '2021' AND Periods = 'P05';",
#     "SELECT SUM(Current_Value) FROM costs WHERE Level1 = 'Advertising & Consumer Promo' AND FY = '2022' AND Periods = 'P13';",
#     "SELECT SUM(Current_Value) FROM costs WHERE Level1 = 'Franchise & Sales Costs' AND FY = '2021' AND Periods = 'P04';",
#     "SELECT SUM(Current_Value) FROM costs WHERE Level1 = 'Franchise & Sales Costs' AND FY = '2022' AND Periods = 'P01';",
#     "SELECT SUM(Current_Value) FROM costs WHERE Level1 = 'General & Admin Overheads' AND FY = '2021' AND Periods = 'P07';",
#     "SELECT SUM(Current_Value) FROM costs WHERE Level1 = 'General & Admin Overheads' AND FY = '2022' AND Periods = 'P11';",
#     "SELECT SUM(Current_Value) FROM costs WHERE Level1 = 'Prime Costs' AND FY = '2021' AND Periods = 'P01';",
#     "SELECT SUM(Current_Value) FROM costs WHERE Level1 = 'Prime Costs' AND FY = '2022' AND Periods = 'P06';",
#     "SELECT SUM(Current_Value) FROM costs WHERE Level1 = 'R Depreciation' AND FY = '2021' AND Periods = 'P03';",
#     "SELECT SUM(Current_Value) FROM costs WHERE Level1 = 'R Depreciation' AND FY = '2022' AND Periods = 'P10';",
#     "SELECT SUM(Current_Value) FROM costs WHERE Level1 = 'Advertising & Consumer Promo' AND FY = '2023' AND Periods = 'P02';",
#     "SELECT SUM(Current_Value) FROM costs WHERE Level1 = 'Franchise & Sales Costs' AND FY = '2023' AND Periods = 'P09';",
#     "SELECT SUM(Current_Value) FROM costs WHERE Level1 = 'General & Admin Overheads' AND FY = '2021' AND Periods = 'P12';",
#     "SELECT SUM(Current_Value) FROM costs WHERE Level1 = 'Prime Costs' AND FY = '2023' AND Periods = 'P08';",
#     "SELECT SUM(Current_Value) FROM costs WHERE Level1 = 'R Depreciation' AND FY = '2021' AND Periods = 'P05';",
#     "SELECT SUM(Current_Value) FROM costs WHERE Level1 = 'Advertising & Consumer Promo' AND FY = '2022' AND Periods = 'P08';",
#     "SELECT SUM(Current_Value) FROM costs WHERE Level1 = 'Franchise & Sales Costs' AND FY = '2021' AND Periods = 'P03';",
#     "SELECT SUM(Current_Value) FROM costs WHERE Level1 = 'General & Admin Overheads' AND FY = '2022' AND Periods = 'P02';",
#     "SELECT SUM(Current_Value) FROM costs WHERE Level1 = 'Prime Costs' AND FY = '2021' AND Periods = 'P11';",
#     "SELECT SUM(Current_Value) FROM costs WHERE Level1 = 'R Depreciation' AND FY = '2022' AND Periods = 'P04';"
# ]
# for query in queries:
#   vn.train(sql=query)

# vn.add_question_sql("Which Periods of Prime Costs are out of confidence interval for year 2022","SELECT Periods FROM costs WHERE Level1 = 'Prime Costs' AND FY = '2022' AND Anomaly = 1;")
# vn.add_question_sql("Which Periods of Prime Costs are out of confidence interval for year 2021","SELECT Periods FROM costs WHERE Level1 = 'Prime Costs' AND FY = '2021' AND Anomaly = 1;")
# vn.add_question_sql("Which Periods of Advertising & Consumer Promo are out of confidence interval for year 2022","SELECT Periods FROM costs WHERE Level1 = 'Advertising & Consumer Promo' AND FY = '2022' AND Anomaly = 1;")
# vn.add_question_sql("Which Periods of Advertising & Consumer Promo are out of confidence interval for year 2021","SELECT Periods FROM costs WHERE Level1 = 'Advertising & Consumer Promo' AND FY = '2021' AND Anomaly = 1;")
# vn.add_question_sql("Which Periods of Franchise & Sales Costs are out of confidence interval for year 2022","SELECT Periods FROM costs WHERE Level1 = 'Franchise & Sales Costs' AND FY = '2022' AND Anomaly = 1;")
# vn.add_question_sql("Which Periods of Franchise & Sales Costs are out of confidence interval for year 2021","SELECT Periods FROM costs WHERE Level1 = 'Franchise & Sales Costs' AND FY = '2021' AND Anomaly = 1;")
# vn.add_question_sql("Which Periods of Prime Costs are out of confidence interval for year 2023","SELECT Periods FROM costs WHERE Level1 = 'Prime Costs' AND FY = '2023' AND Anomaly = 1;")
# #
# doc="""
# Dataset: Company Cost Heads Data
# ---------------------------------
#
# Description:
#     This dataset provides detailed information about various cost heads within a company across different fiscal years and periods. It includes data on spending categories such as advertising, franchise costs, administrative overheads, prime costs, and asset depreciation. Each record in the dataset represents aggregated financial figures for a specific category, period, and fiscal year.
#
# Schema:
#     Level1 (TEXT): Describes the category of the costs, e.g., 'Advertising & Consumer Promo', 'Franchise & Sales Costs', etc.
#     FY (INTEGER): Fiscal year of the recorded data.
#     Periods (TEXT): Fiscal period within the year, ranges from P01 to P13.
#     Current_Value (REAL): The actual monetary value spent or incurred in the specified category during the period.
#     GSV (REAL): Gross Sales Value associated with the cost head for the period.
#     Anomaly (BOOLEAN): A boolean flag indicating whether the entry is considered an anomaly.
#     Confidence_Low (REAL): The lower bound of the confidence interval in absolute terms.
#     Confidence_High (REAL): The upper bound of the confidence interval in absolute terms.
#
# Usage:
#     This dataset is primarily used for financial analysis, budget planning, and auditing. Analysts can query the dataset to track financial trends, assess budget adherence, and identify anomalies in spending across different categories and periods.
# """
#
# vn.train(documentation=doc)

def vn_aays():
    return vn

