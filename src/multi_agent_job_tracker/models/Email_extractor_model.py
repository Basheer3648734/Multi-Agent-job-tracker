from pydantic import BaseModel, Field, field_validator
from typing import Optional, Literal
from datetime import date, datetime

class Email_extractor_model(BaseModel):
    Company:str = Field(description="Company name where the job application is sent")
    position:str = Field(description="Job Position applied for")
    pay_rate: Optional[str] = Field(description="Pay rate offered for the job")
    job_portal: Optional[str] = Field(description="Job portal where the application is sent", default=None)
    location: Optional[str] = Field(description="Location of the job")
    applied_date: Optional[date] = Field(description="Date when the application was sent, Return as YYYY-MM-DD.", default=None)
    link:Optional[str] = Field(description="Link to the job application or job posting")
    status: Literal["Applied", "Interview", "Offer", "Rejected"] = Field(description="Current status of the job application", default="Applied")
    poc_name: Optional[str] = Field(description="Point of contact name for the job application")
    poc_email: Optional[str] = Field(description="Point of contact email for the job application")
    poc_phone: Optional[str] = Field(description="Point of contact phone number for the job application")
    summary: str = Field(description="Summary of the email content, including any important details or context related to the job application")


@field_validator("applied_date", mode="before")
@classmethod
def normalize_applied_date(cls, value):
    """ Convert common date formats into a Python date. """
    if value is None:
        return None
    if isinstance(value, date): 
        return value
    if not value: 
        return value
    value = str(value).strip() # ISO format: 2026-09-04 
    try:
        return date.fromisoformat(value)
    except ValueError:
        pass # Example: September 4, 2026
    for fmt in ( "%B %d, %Y", "%b %d, %Y", "%m/%d/%Y", "%Y/%m/%d", ):
        try:
            return datetime.strptime( value, fmt ).date()
        except ValueError:
            pass
