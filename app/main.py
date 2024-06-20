from fastapi import FastAPI, File, Query, UploadFile, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
import io
import uvicorn
from app.chat import run_chat
from app.document import Document

app = FastAPI()


@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        doc = Document(file.filename, contents)
        doc.store_embeddings()
        doc.store_file()
        return JSONResponse(
            content={"message": "File uploaded and processed successfully."},
            status_code=200,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/file/{filename}")
async def download_file(filename: str):
    try:
        file_data = Document(filename).get_file()
        return StreamingResponse(
            io.BytesIO(file_data),
            media_type="application/pdf",
            headers={"Content-Disposition": "inline", "filename": filename},
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/chat/")
async def chat(question: str = Query(), filename: str = Query()):
    try:
        response = run_chat(question, filename)
        return StreamingResponse(io.StringIO(response), media_type="text/plain")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
