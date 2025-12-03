import markdown, bleach, requests, os
from bs4 import BeautifulSoup
from dotenv import load_dotenv

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

def extract_text_from_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(separator="\n")
    return text.strip()

def spellcheck(plain: str) -> str:
    url = "https://api.api-ninjas.com/v1/spellcheck"
    params = {"text": plain}

    headers = {
        "X-Api-Key": API_KEY
    }
    resp = requests.get(url, headers=headers, params=params, timeout=20)
    data = resp.json()
    return data.get("corrected", plain)

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