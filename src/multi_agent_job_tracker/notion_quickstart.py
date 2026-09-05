
import os
from dotenv import load_dotenv
from notion_database_agent.service import Notion_database_service
from multi_agent_job_tracker.models.Email_extractor_model import Email_extractor_model
load_dotenv()


notion_service:Notion_database_service = Notion_database_service(os.getenv("NOTION_API_KEY"))
row = Email_extractor_model( Company="Meta", position="AI Enginee", pay_rate="72", job_portal="linkedin", location="us", applied_date="2026-09-03", link="https://developers.notion.com/reference/query-a-data-source?playground=open", status="Applied", poc_name="adf", poc_email="afdfd@fddd.com", poc_phone="8555", summary="" )

result = notion_service.upsert_notion_row(
    data_source_id=f"{os.getenv('NOTION_DATASOURCE_ID')}",
    job=row)

print(result)