from pydantic import BaseModel, Field
from .Email_extractor_model import Email_extractor_model

class Email_response(BaseModel):
    emails: list[Email_extractor_model] = Field(
        description="Extracted information for each email"
    )