"""
Working with rag sysytem as it is very important 
"""
from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain_community.document_loaders import OnlinePDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
doc_path = r"C:\Users\adity\Desktop\luck\project\mainapp\001-information-security-and-assurance-policy.pdf"
model = "llama3"

if doc_path:
    loader = UnstructuredPDFLoader(doc_path)
    text = loader.load()
    print("done loading.....")
else:
    print("Uplaod a pdf file")

content = text[0].page_content
#print(content[:100])
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200)
chunks = text_splitter.split_documents(text)
print("done splitting.....")    
print(chunks[0])

import ollama
from langchain_ollama import OllamaEmbeddings
ollama.pull("nomic-embed-text")

vector_db = Chroma.from_documents(documents=chunks,embedding=OllamaEmbeddings(model = "nomic-embed-text"),collection_name="simple-rag")
print("done vectorizing.....")


from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser

from langchain_ollama import ChatOllama

from langchain_core.runnables import RunnablePassthrough
from langchain.retrievers.multi_query import MultiQueryRetriever

llm  = ChatOllama(model = model)

query_prompt = PromptTemplate(
    input_variables= ["question"],
    template="""Your are an AI language model assistant. tour task is to answer the question of the user based on the vector databse given: {question}

"""
)

retriver = MultiQueryRetriever.from_llm(
    vector_db.as_retriever(),llm,prompt = query_prompt
)

template = """Answer the question based Only on the following content{context}
Question: {question}"""

prompt = ChatPromptTemplate.from_template(template)

chain = (
    {"context":retriver,"question":RunnablePassthrough()}
    | prompt
    | llm 
    | StrOutputParser()
)

res = chain.invoke(input=("what is this document about?",))
print(res)


# import requests
# import json

# url = "http://localhost:11434/api/generate"
# model_name = "llama3"

# # Preload model to avoid first-time delay
# requests.post(url, json={"model": model_name, "prompt": "Hello"}, stream=True)

# # Use a persistent session
# session = requests.Session()
# data = {
#     "model": model_name,
#     "prompt": "Give me tips for linkdin profile",
# }

# response = session.post(url, json=data, stream=True)

# if response.status_code == 200:
#     print("Generated Text:", end=" ", flush=True)
#     for line in response.iter_lines(decode_unicode=True):
#         if line:
#             print(json.loads(line).get("response", ""), end=" ", flush=True)
# else:
#     print("Error Occurred")
# import ollama

# #response = ollama.list()
# #print(response)

# res  = ollama.chat(
#     model="llama3",
#     messages=[{"role": "user", "content": "Why is the ocean so salty?"}],
#     stream=True,
# )
# for chunk in res:
#     print(chunk["message"]['content'],end=" ",flush=True)
# import ollama 
# res = ollama.generate(
#     model="llama3",
#     prompt="yo how are you",
# )

# print(res["response"])