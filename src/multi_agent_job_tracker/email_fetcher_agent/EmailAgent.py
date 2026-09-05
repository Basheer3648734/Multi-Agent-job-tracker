import os

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool

from multi_agent_job_tracker.models.Email_response import Email_response
from multi_agent_job_tracker.email_fetcher_agent.service import (
    EmailFetcherService,
)


load_dotenv()


class EmailAgent:

    def __init__(self):
        self.model_name = os.getenv(
            "EMAIL_AGENT_MODEL",
            "gpt-5.5"
        )

        self.email_query = (
            'newer_than:1d AND '
            '("application" OR "interview" OR '
            '"job status" OR "offer" OR "recruiter")'
        )

        self.prompt = """
        You are an email extractor agent.

        Get the emails and for each email extract the information.

        Make sure to extract the information as well as
        summarize the email content.

        If any field is not present in the email, return it
        as null or empty string rather than hallucinating
        the information.

        Make sure to extract information only from the
        provided email.

        Status (context of email):
        - Applied: The email indicates that a job application
          has been submitted.
        - Interview: The email indicates that an interview
          has been scheduled or requested.
        - Offer: The email indicates that a job offer has
          been made.
        - Rejected: The email indicates that the job
          application has been rejected.
        """

    def fetch_emails(self) -> list[str]:
        """
        Fetch emails from Gmail.
        """

        service = EmailFetcherService().get_gmail_service()

        emails = EmailFetcherService().fetch_emails(
            service,
            q=self.email_query,
        )

        return emails

    def invoke_agent(self) -> Email_response:
        """
        Invokes the email agent to fetch emails and
        extract relevant information.
        """

        @tool(
            "Email_Agent",
            description=(
                "Fetches emails from Gmail and returns "
                "the relevant email contents."
            ),
        )
        def get_email_agent() -> list[str]:
            return self.fetch_emails()

        agent = create_agent(
            model=self.model_name,
            tools=[get_email_agent],
            response_format=Email_response,
        )

        response = agent.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": self.prompt,
                    }
                ]
            }
        )

        return response["structured_response"]
