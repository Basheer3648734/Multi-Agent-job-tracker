from notion_client import Client

from multi_agent_job_tracker.models.Email_extractor_model import Email_extractor_model


class Notion_database_service:

    def __init__(self, notion_api_key: str):
        self.notion = Client(auth=notion_api_key)

    # =========================================================
    # CONVERSION HELPERS
    # =========================================================

    @staticmethod
    def _rich_text(value):
        """Convert a string to a Notion rich_text property."""

        if value is None:
            return {
                "rich_text": []
            }

        return {
            "rich_text": [
                {
                    "type": "text",
                    "text": {
                        "content": str(value)
                    }
                }
            ]
        }

    @staticmethod
    def _title(value):
        """Convert a string to a Notion title property."""

        if value is None:
            return {
                "title": []
            }

        return {
            "title": [
                {
                    "type": "text",
                    "text": {
                        "content": str(value)
                    }
                }
            ]
        }

    @staticmethod
    def _status(value):
        """Convert a value to a Notion status property."""

        return {
            "status": (
                {"name": value}
                if value
                else None
            )
        }

    @staticmethod
    def _date(value):
        """Convert a value to a Notion date property."""

        return {
            "date": (
                {"start": value}
                if value
                else None
            )
        }

    @staticmethod
    def _email(value):
        """Convert a value to a Notion email property."""

        return {
            "email": value
        }

    @staticmethod
    def _phone(value):
        """Convert a value to a Notion phone property."""

        return {
            "phone_number": value
        }

    @staticmethod
    def _url(value):
        """Convert a value to a Notion URL property."""

        return {
            "url": value
        }

    # =========================================================
    # PYDANTIC -> NOTION
    # =========================================================

    def _build_notion_properties(
        self,
        job: Email_extractor_model
    ):
        """
        Convert Email_extractor_model into Notion properties.

        This is the single source of truth for the Notion schema.
        """

        return {
            "Company Name": self._title(job.Company),

            "Position": self._rich_text(job.position),

            "Pay Rate": self._rich_text(job.pay_rate),

            "Job portal": self._rich_text(job.job_portal),

            "location": self._rich_text(job.location),

            "Applied Date": self._date(job.applied_date),

            "Link": self._url(job.link),

            "Status": self._status(job.status),

            "poc_name": self._rich_text(job.poc_name),

            "poc_email": self._email(job.poc_email),

            "poc_phone": self._phone(job.poc_phone),

            # Remove this if your Notion database doesn't
            # contain a "summary" column.
            "summary": self._rich_text(job.summary),
        }

    # =========================================================
    # GET ROWS
    # =========================================================

    def get_notion_database_rows(
        self,
        data_source_id: str
    ):
        """
        Query all rows from a Notion data source.

        Returns:
            list[dict]
        """

        rows = []

        response = self.notion.data_sources.query(
            data_source_id=data_source_id
        )

        for page in response.get("results", []):

            row = {
                "_page_id": page["id"]
            }

            for column_name, property_data in page["properties"].items():

                row[column_name] = self._extract_property_value(
                    property_data
                )

            rows.append(row)

        return rows

    # =========================================================
    # NOTION PROPERTY -> PYTHON VALUE
    # =========================================================

    @staticmethod
    def _extract_property_value(property_data):
        """
        Convert a Notion property response into a Python value.
        """

        property_type = property_data["type"]

        if property_type == "title":

            values = property_data["title"]

            return (
                values[0]["plain_text"]
                if values
                else None
            )

        if property_type == "rich_text":

            values = property_data["rich_text"]

            return (
                "".join(
                    item["plain_text"]
                    for item in values
                )
                if values
                else None
            )

        if property_type == "number":
            return property_data["number"]

        if property_type == "select":

            select = property_data["select"]

            return (
                select["name"]
                if select
                else None
            )

        if property_type == "status":

            status = property_data["status"]

            return (
                status["name"]
                if status
                else None
            )

        if property_type == "multi_select":

            return [
                item["name"]
                for item in property_data["multi_select"]
            ]

        if property_type == "checkbox":
            return property_data["checkbox"]

        if property_type == "date":

            date = property_data["date"]

            return (
                date["start"]
                if date
                else None
            )

        if property_type == "url":
            return property_data["url"]

        if property_type == "email":
            return property_data["email"]

        if property_type == "phone_number":
            return property_data["phone_number"]

        return None

    # =========================================================
    # CREATE
    # =========================================================

    def add_notion_row(
        self,
        data_source_id: str,
        job: Email_extractor_model
    ):
        """
        Create a new Notion database row.
        """

        properties = self._build_notion_properties(job)

        return self.notion.pages.create(
            parent={
                "type": "data_source_id",
                "data_source_id": data_source_id
            },
            properties=properties
        )

    # =========================================================
    # UPDATE
    # =========================================================

    def update_notion_row(
        self,
        page_id: str,
        job: Email_extractor_model
    ):
        """
        Update an existing Notion database row.
        """

        properties = self._build_notion_properties(job)

        return self.notion.pages.update(
            page_id=page_id,
            properties=properties
        )

    # =========================================================
    # UPSERT
    # =========================================================

    def upsert_notion_row(
        self,
        data_source_id: str,
        job: Email_extractor_model
    ):
        """
        Update an existing row if Company + Position exists.
        Otherwise create a new row.
        """

        company_name = job.Company
        position = job.position

        if not company_name:
            raise ValueError("Company is required")

        if not position:
            raise ValueError("Position is required")

        # -----------------------------------------------------
        # Search for existing row
        # -----------------------------------------------------

        response = self.notion.data_sources.query(
            data_source_id=data_source_id,
            filter={
                "and": [
                    {
                        "property": "Company Name",
                        "title": {
                            "equals": company_name
                        }
                    },
                    {
                        "property": "Position",
                        "rich_text": {
                            "equals": position
                        }
                    }
                ]
            }
        )

        existing_rows = response.get("results", [])

        # -----------------------------------------------------
        # Prevent duplicate records
        # -----------------------------------------------------

        if len(existing_rows) > 1:
            raise ValueError(
                f"Multiple rows found for "
                f"Company='{company_name}', "
                f"Position='{position}'"
            )

        # -----------------------------------------------------
        # UPDATE
        # -----------------------------------------------------

        if existing_rows:

            page_id = existing_rows[0]["id"]

            page = self.update_notion_row(
                page_id=page_id,
                job=job
            )

            return {
                "action": "updated",
                "page": page
            }

        # -----------------------------------------------------
        # CREATE
        # -----------------------------------------------------

        page = self.add_notion_row(
            data_source_id=data_source_id,
            job=job
        )

        return {
            "action": "created",
            "page": page
        }
