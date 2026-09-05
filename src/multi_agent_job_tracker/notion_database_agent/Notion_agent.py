from multi_agent_job_tracker.notion_database_agent.service import Notion_database_service
from dotenv import load_dotenv
import os
from multi_agent_job_tracker.models.Email_response  import Email_response
load_dotenv()

service = Notion_database_service(os.getenv("NOTION_API_KEY"))

def add_email_response_to_notion(email_response: Email_response):
    """
    Adds the extracted email response to the Notion database.
    """
    for email in email_response.emails:
        try:
            row_data = email # Convert Pydantic model to dictionary
            result = service.upsert_notion_row(
                data_source_id=f"{os.getenv('NOTION_DATASOURCE_ID')}",
                job=row_data
            )
            print(f"Added email from {email.Company} to Notion. Result: {result}")
        except Exception as e:
            print(f"Error adding email from {email.Company} to Notion: {e}")