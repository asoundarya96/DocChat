# Document Chat Application

This project is a document chat application that allows users to interact with PDF documents through a chat interface.

## Features

- **Interacting with Documents**: Upload your documents via the Gradio interface and start a chat session to interact with the uploaded documents.

## Implementation

- **Chat Interface**: Built using Gradio for a user-friendly UI.
- **Language Model Interaction**: Utilizes LangChain framework for interacting with a local LLM (Large Language Model) powered by Ollama.
- **API**: Exposed using FastAPI for document uploads and chat.
- **Embeddings**: Uses GPT4AllEmbeddings for embedding models.
- **Local RAG**: Implemented using pgvector database.

## Database Setup

Embedding and collection tables are auto-generated by LangChain functions.

### Documents Table

```sql
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    document BYTEA,
    embedding VECTOR(384) -- Set dimensions based on embed model
);

https://github.com/asoundarya96/DocChat/assets/24543401/8d2d5b58-a3ea-4a84-a181-195cd713a83d

