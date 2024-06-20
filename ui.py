import gradio as gr
import requests
import os


def file_display(filename):
    if filename:
        iframe_code = f"""<!DOCTYPE html>
            <html>
            <body>
                <h1>{filename}</h1>
                <iframe src="http://127.0.0.1:8000/file/{filename}" width="100%" height="600px"></iframe>
            </body>
            </html>  """
        return iframe_code, gr.Button(visible=True), gr.Button(visible=False)
    return "Error processing file"


def file_upload(file):
    if file is None:
        return {"status": "error", "message": "No file uploaded"}

    with open(file.name, "rb") as f:
        response = requests.post("http://127.0.0.1:8000/upload/", files={"file": f})
    if response.status_code != 200:
        return "Error uploading file"

    return file_display(os.path.basename(file.name))


def respond(message, history, file):
    filename = os.path.basename(file.name)
    response = requests.get(
        "http://127.0.0.1:8000/chat/",
        params={"question": message, "filename": filename},
    )
    if response.status_code != 200:
        return "Error processing question"
    return response.text


greet_message = [
    ("Hello! I am a bot that can answer questions about the uploaded document.", "")
]


def start_chat(file):
    return gr.Column(visible=True)


chatbot = gr.Chatbot(value=greet_message)

with gr.Blocks() as iface:
    with gr.Row():
        file = gr.File(label="Upload a document", scale=0.3)
        file_preview = gr.HTML(label="Preview")

    upload_button = gr.Button(value="Upload", visible=True)
    chat_button = gr.Button(value="Start Chat Session", visible=False)
    upload_button.click(
        file_upload, inputs=[file], outputs=[file_preview, chat_button, upload_button]
    )

    with gr.Column(visible=False) as chat_col:
        chat_iface = gr.ChatInterface(
            chatbot=chatbot, fn=respond, additional_inputs=[file], undo_btn=None
        )
    chat_button.click(start_chat, inputs=[file], outputs=[chat_col])


iface.launch()
