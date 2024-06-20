from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_postgres.vectorstores import PGVector
from langchain_community.embeddings import GPT4AllEmbeddings
from app.db import connection_string
from fastapi import HTTPException
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

llm = ChatOllama(model="llama2")
model_name = "all-MiniLM-L6-v2.gguf2.f16.gguf"
gpt4all_kwargs = {"allow_download": "True"}
embeddings = GPT4AllEmbeddings(model_name=model_name, gpt4all_kwargs=gpt4all_kwargs)

prompt_template = PromptTemplate(
    template="""
    You are an assitant that can answer questions from given document.
    if user greets, greet back.
    Please provide the answer strictly based on the provided document context.
    Do not generate any information that is not found in the documents. If user asks for information that is not in the document,
    please respond with "I am sorry, I could not find that information in given document".

    Context: {context}
    Question: {question}
    """,
    input_variables=["context", "question"],
)


def run_chat(question, filename):
    try:
        vectordb = PGVector(
            connection=connection_string,
            collection_name=filename,
            embeddings=embeddings,
            use_jsonb=True,
        )

        qa_chain = RetrievalQA.from_chain_type(
            llm,
            retriever=vectordb.as_retriever(),
            chain_type_kwargs={"prompt": prompt_template},
        )
        question = {"query": question}
        result = qa_chain.invoke(question)
        return result["result"]
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=500, detail=str(e))
