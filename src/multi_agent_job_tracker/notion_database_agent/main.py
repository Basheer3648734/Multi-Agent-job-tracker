from service import Notion_database_service
from dotenv import load_dotenv
import os

load_dotenv()
notion_base_url = os.getenv("NOTION_BASE_URL")
datasource_id = os.getenv("NOTION_DATASOURCE_ID")
notion_version = os.getenv("NOTION_VERSION")
notion_api_key = os.getenv("NOTION_API_KEY")

if __name__ == "__main__":


    notion_service = Notion_database_service(notion_base_url, datasource_id, notion_version, notion_api_key)
    response = notion_service.get_database()
    print(response)
    print("Response: ", response.text)