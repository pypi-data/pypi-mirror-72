import re
from datetime import datetime
from selenium.common.exceptions import NoSuchElementException
from .opportunity import Opportunity
from .settings import settings

link_id_re = re.compile(r'/competition/(\d+)/overview')
date_re = re.compile(r'^.*: ')

def conform_date(dt):
    # The gov.uk opportunities site uses a variety of datetime formats,
    # some of them not easily manageable by strptime(). Conform them.
    dt = re.sub(r'^[a-zA-Z]+ (\d)', r'\1', dt)
    dt = re.sub(r'20(\d{2})\s*$', r'20\1 09:00am', dt)
    dt = re.sub(r'^(\d) ', r'0\1 ', dt)
    dt = re.sub(r' (\d):(\d{2})', r' 0\1:\2', dt)
    return datetime.strftime(datetime.strptime(dt, "%d %B %Y %I:%M%p"), "%d/%m/%Y")


class Govuk(Opportunity):

    def __init__(self, uri, title):
        super().__init__(uri, title)
        self.attributes["campaign_name"] = 'https://apply-for-innovation-funding.service.gov.uk'
        self.attributes["account_name"] = settings["suitecrm"]["govuk_account_name"]
        self.attributes["account_id"] = settings["suitecrm"]["govuk_account_id"]

    def scrape(self, browser):
        if not super().scrape(browser):
            return
        content = browser.find_element_by_css_selector('#main-content')
        self.attributes["description"] = content.find_element_by_css_selector('p:nth-child(2)').get_attribute('innerText')
        dates = content.find_element_by_css_selector('ul.govuk-list')
        date_closes = date_re.sub('', dates.find_element_by_css_selector('li:nth-child(2)').get_attribute('innerText'))
        self.attributes["date_closed"] = conform_date(date_closes)

        for section in browser.find_elements_by_css_selector('section.govuk-tabs__panel'):
            if section.get_attribute('id') == 'dates':
                self.attributes["description"] += "\n\nDates"
                dts = section.find_elements_by_css_selector('dt')
                dds = section.find_elements_by_css_selector('dd')
                for dt, dd in zip(dts, dds):
                    key = dt.get_attribute('innerText')
                    val = dd.get_attribute('innerText')
                    str_date = conform_date(key)
                    details = val.replace('\n', '')
                    self.attributes["description"] += f"\n> {str_date}: {details}"
            else:
                for row in section.find_elements_by_css_selector('.govuk-grid-row'):
                    heading = row.find_element_by_css_selector('.govuk-grid-column-one-third h2').get_attribute('innerText')
                    body = row.find_element_by_css_selector('.govuk-grid-column-two-thirds .govuk-body').get_attribute('innerText')
                    self.attributes["description"] += f"\n\n{heading}\n\n{body}"

        amount_match = re.findall(r'£[0-9,]+', self.attributes["description"])
        if amount_match:
            filtered = sorted(list(map(lambda x: int(re.sub(r'[^0-9]', '', x)),
                                       amount_match)), reverse=True)
            self.attributes["amount"] = filtered[0]


def search(browser):
    opportunities = []
    browser.get('https://apply-for-innovation-funding.service.gov.uk/competition/search')

    while True:
        search_results = browser.find_elements_by_css_selector('#main-content ul.govuk-list > li')
        for scrape in search_results:
            title_link = scrape.find_element_by_css_selector('h2.govuk-heading-m > a')
            uri = title_link.get_attribute("href")
            id_match = link_id_re.search(uri)
            if id_match:
                title = title_link.text
                opportunities.append(Govuk(uri, title))
        try:
            next_page = browser.find_element_by_css_selector('#main-content ul.pagination > li.next > a')
        except NoSuchElementException:
            break
        next_page.click()

    print(f'==> Found {len(opportunities)} gov.uk competitions')
    for opp in opportunities:
        opp.scrape(browser)

    return opportunities
