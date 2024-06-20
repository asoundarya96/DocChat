import fitz  # PyMuPDF
from app.db import VectorDB, connection_string
from fastapi import HTTPException
from langchain_postgres.vectorstores import PGVector
from app.chat import embeddings
from langchain.docstore.document import Document as LangchainDocument


class Document:
    def __init__(self, name, content=None):
        self.name = name
        self.content = content

    def store_file(self):
        with VectorDB() as db:
            cursor = db.cursor()
            insert_query = (
                "INSERT INTO documents (document, collection_name) VALUES (%s, %s)"
            )
            cursor.execute(insert_query, (self.content, self.name))
            db.commit()

    def get_file(self):
        with VectorDB() as db:
            cursor = db.cursor()
            select_query = "SELECT document FROM documents WHERE collection_name = %s"
            cursor.execute(select_query, (self.name,))
            result = cursor.fetchone()

        if result is None:
            raise HTTPException(status_code=404, detail="File not found")
        return result[0]

    def extract_pages(self):
        pdf_document = fitz.open(stream=self.content, filetype="pdf")
        pages = []
        for page_num in range(pdf_document.page_count):
            page = pdf_document.load_page(page_num)
            pages.append(LangchainDocument(page_content=page.get_text()))
        return pages

    def store_embeddings(self):
        docs = self.extract_pages()
        vectorstore = PGVector.from_documents(
            embedding=embeddings,
            documents=docs,
            connection=connection_string,
            collection_name=self.name,
            use_jsonb=True,
        )
