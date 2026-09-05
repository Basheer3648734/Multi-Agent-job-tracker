from multi_agent_job_tracker.email_fetcher_agent.EmailAgent import EmailAgent
from multi_agent_job_tracker.notion_database_agent.Notion_agent import add_email_response_to_notion

email_agent = EmailAgent()

email_output = email_agent.invoke_agent()
print(add_email_response_to_notion(email_output))