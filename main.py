from fastapi import FastAPI, Form, Request ,Body
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from schemas import HTMLCorrectionRequest
from app.functions import markdown_to_html, corrector


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
async def correct_endpoint(body: str = Body(..., media_type="text/plain")):
    corrected_html = corrector(body)
    return JSONResponse(content={"corrected_html": corrected_html})

