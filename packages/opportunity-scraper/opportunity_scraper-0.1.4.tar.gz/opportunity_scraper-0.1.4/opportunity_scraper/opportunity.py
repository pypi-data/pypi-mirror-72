import uuid
from .settings import settings

class Opportunity:
    def __init__(self, uri, title):
        self.type = "Opportunities"
        self.id = uuid.uuid5(uuid.NAMESPACE_URL, uri).urn[9:]
        self.attributes = {
            "assigned_user_name": settings["suitecrm"]["assigned_user_name"],
            "assigned_user_id": settings["suitecrm"]["assigned_user_id"],
            "sales_stage": "Prospecting",
            "opportunity_type": "New Business",
            "lead_source": "Web Site",
            "next_step": uri,
            "name": title,
            "date_closed": None,
        }

    def scrape(self, browser):
        title = self.attributes["name"]
        print(f'Scraping {title}...')
        try:
            browser.get(self.attributes["next_step"])
        except Exception:
            print(f'Failed to fetch details for: {title}')
            return False
        return True
