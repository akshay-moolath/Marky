from pydantic import BaseModel

class HTMLCorrectionRequest(BaseModel):
    html: str