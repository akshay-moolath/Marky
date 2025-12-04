import markdown, bleach, requests, os
from bs4 import BeautifulSoup, NavigableString
from dotenv import load_dotenv
from fastapi import UploadFile, File
import asyncio
from fastapi.responses import JSONResponse
from PyPDF2 import PdfReader
from io import BytesIO



load_dotenv()
spellcheck_URL = os.getenv("spellcheck_URL")
API_KEY = os.getenv("API_KEY")


def markdown_to_html(md_text: str) -> str:
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

def corrector(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    
    for element in soup.descendants:
        if isinstance(element, NavigableString):
            if element.strip():
                original_text = str(element)
                corrected = " "+ spellcheck(original_text)
                if original_text: 
                    if original_text[0].isupper():
                        corrected = corrected[1].upper() + corrected[2:]
                element.replace_with(corrected)
                
    return str(soup)

def spellcheck(plain: str) -> str:
    url = spellcheck_URL 
    params = {"text": plain}

    headers = {
        "X-Api-Key": API_KEY
    }
    resp = requests.get(url, headers=headers, params=params, timeout=20)
    data = resp.json()
    return data.get("corrected", plain)

async def uploadFile(file):
    
    contents = await file.read()
    text_content = contents.decode('utf-8')
    html = markdown_to_html(text_content)
    return JSONResponse({"html": html})

        

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