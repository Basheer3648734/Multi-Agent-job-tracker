import requests
import os
from dotenv import load_dotenv

load_dotenv()

notion_base_url = os.getenv("NOTION_BASE_URL")
datasource_id = os.getenv("NOTION_DATASOURCE_ID")
url = f"{notion_base_url}v1/databases/{datasource_id}"

headers = {
    "Notion-Version": os.getenv("NOTION_VERSION"),
    "Authorization": f"Bearer {os.getenv('NOTION_API_KEY')}",
    "Content-Type": "application/json"
}

response = requests.get(url, headers=headers)

print(response)
print("Response: ", response.text)