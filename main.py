from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from schemas import HTMLCorrectionRequest
from app.functions import markdown_to_html, extract_text_from_html, spellcheck



app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def home():
    return FileResponse("static/index.html")

@app.post("/render")
async def render(md: str = Form(...)):
    html = markdown_to_html(md)
    return HTMLResponse(content=html, status_code=200)

@app.post("/correct")
async def correct(data_in: HTMLCorrectionRequest):
    return {
  "status": "success",
  "original_length": 500,
  "corrected_html": "<h2>This is the *new*, clean HTML snippet.</h2>" 
}


