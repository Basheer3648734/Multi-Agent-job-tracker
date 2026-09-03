from service import EmailFetcherService

if __name__=="__main__":
    email_fetcher = EmailFetcherService()
    gmail_service = email_fetcher.get_gmail_service()
    email_fetcher.fetch_emails(gmail_service, q='newer_than:1d AND ("application" OR "interview" OR "job status" OR "offer" OR "recruiter")')