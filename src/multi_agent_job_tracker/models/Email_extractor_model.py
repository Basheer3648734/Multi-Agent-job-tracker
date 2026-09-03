from pydantic import BaseModel, Field
from typing import Optional, Literal

class Email_extractor_model(BaseModel):
    Company:str = Field(description="Company name where the job application is sent")
    position:str = Field(description="Job Position applied for")
    pay_rate: Optional[str] = Field(description="Pay rate offered for the job")
    job_portal: Optional[str] = Field(description="Job portal where the application is sent")
    location: Optional[str] = Field(description="Location of the job")
    applied_date: str = Field(description="Date when the application was sent")
    link:Optional[str] = Field(description="Link to the job application or job posting")
    status: Literal["Applied", "Interview", "Offer", "Rejected"] = Field(description="Current status of the job application")
    poc_name: Optional[str] = Field(description="Point of contact name for the job application")
    poc_email: Optional[str] = Field(description="Point of contact email for the job application")
    poc_phone: Optional[str] = Field(description="Point of contact phone number for the job application")
    summary: str = Field(description="Summary of the email content, including any important details or context related to the job application")
