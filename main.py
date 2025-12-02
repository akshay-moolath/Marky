from fastapi import FastAPI, Request, Form ,Body
from fastapi import HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from bs4 import BeautifulSoup
import bleach,os,requests,markdown
from dotenv import load_dotenv
import json

load_dotenv()
OPENAI_URL = "https://api.api-ninjas.com/v1/spellcheck"
API_KEY = os.getenv("API_KEY")

app = FastAPI()
templates = Jinja2Templates(directory="templates")

ALLOWED_TAGS = list(bleach.sanitizer.ALLOWED_TAGS) + [
    "p", "pre", "code", "hr", "br", "h1", "h2", "h3", "h4", "h5", "h6",
    "table", "thead", "tbody", "tr", "th", "td", "ul", "ol", "li"
]
ALLOWED_ATTRIBUTES = {
    **bleach.sanitizer.ALLOWED_ATTRIBUTES,
    "a": ["href", "title", "rel", "target"],
    "img": ["src", "alt", "title"],
    "th": ["colspan", "rowspan"],
    "td": ["colspan", "rowspan"],
}


def markdown_to_safe_html(md_text: str) -> str:
    raw_html = markdown.markdown(
    md_text,
    extensions=["fenced_code", "tables", "toc"]
    )
    clean = bleach.clean(
        raw_html,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        strip=True)
    clean = bleach.linkify(clean)
    clean = clean.replace("<a ", '<a target="_blank" rel="noopener noreferrer" ')

    return clean

def extract_text_from_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(separator="\n")
    return text.strip()

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("preview.html", {"request": request, "html": ""})

@app.post("/render", response_class=HTMLResponse)
async def render(request: Request, md: str = Form(...)):
    html= markdown_to_safe_html(md)
    plain = extract_text_from_html(html)
    corrected_text= spellcheck(plain)
    return templates.TemplateResponse("preview.html", {"request": request, "html": html, "md": md,"corrected_text": corrected_text})

def spellcheck(plain: str) -> str:
    if not API_KEY:
        raise RuntimeError("API Ninjas key not found in .env (NINJA_KEY).")

    url = "https://api.api-ninjas.com/v1/spellcheck"
    params = {"text": plain}

    headers = {
        "X-Api-Key": API_KEY
    }

    try:
        resp = requests.get(url, headers=headers, params=params, timeout=20)
    except requests.RequestException as exc:
        raise HTTPException(status_code=502, detail=f"API Key error: {exc}")

    if resp.status_code != 200:
        raise HTTPException(status_code=502, detail=resp.text)

    data = resp.json()

    # `corrected` always exists in Spell Check API response
    return data.get("corrected", plain)


