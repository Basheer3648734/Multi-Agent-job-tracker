import requests


class Notion_database_service:
    def __init__(self, notion_base_url, datasource_id, notion_version, notion_api_key):
        self.notion_base_url = notion_base_url
        self.datasource_id = datasource_id
        self.notion_version = notion_version
        self.notion_api_key = notion_api_key

    def get_database(self):
        url = f"{self.notion_base_url}/v1/data_sources/{self.datasource_id}/query"
        headers = {
            "Notion-Version": self.notion_version,
            "Authorization": f"Bearer {self.notion_api_key}",
            "Content-Type": "application/json"
        }
        response = requests.post(url, headers=headers)
        return response

        