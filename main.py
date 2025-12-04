from fastapi import FastAPI, Form, Request ,Body, UploadFile, File
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from app.functions import markdown_to_html, corrector , uploadFile


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
async def correct(html: str = Body(..., media_type="text/plain")):
    corrected_html = corrector(html)
    return JSONResponse(content={"corrected_html": corrected_html})

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    content = await uploadFile(file)
    return content


