
import os

from langchain.llms import OpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
from langchain.chains.summarize import load_summarize_chain
from langchain_openai import AzureChatOpenAI
from dotenv import load_dotenv

load_dotenv()

# In[2]:
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_DEPLOYMENT_NAME = os.getenv('OPENAI_DEPLOYMENT_NAME')
OPENAI_DEPLOYMENT_NAME_GPT4 = os.getenv('OPENAI_DEPLOYMENT_NAME_GPT4')
MODEL_NAME = os.getenv('MODEL_NAME')
api_version = os.getenv('api_version')
azure_endpoint = os.getenv('azure_endpoint')

def generate_response(txt):
    # Instantiate the LLM model
    llm = AzureChatOpenAI(openai_api_key=OPENAI_API_KEY,
                          deployment_name=OPENAI_DEPLOYMENT_NAME_GPT4,
                          api_version="2023-05-15",
                          azure_endpoint='https://openaiivadev.openai.azure.com/',
                          temperature=0)
    
    # Split text
    text_splitter = CharacterTextSplitter()
    texts = text_splitter.split_text(txt)
    
    # Create multiple documents
    docs = [Document(page_content=t) for t in texts]
    
    # Text summarization
    chain = load_summarize_chain(llm, chain_type='map_reduce')
    
    return chain.run(docs)
