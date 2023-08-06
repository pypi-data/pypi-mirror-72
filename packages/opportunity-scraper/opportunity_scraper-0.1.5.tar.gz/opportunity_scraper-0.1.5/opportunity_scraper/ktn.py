import re
from datetime import datetime
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from .opportunity import Opportunity
from .settings import settings

link_id_re = re.compile(r'/challenges/single/(\d+)')
open_re = re.compile(r'Launch of the Competition: (\d{1,2})([a-z]{2})? (of )?([a-zA-Z]{3,}) (20\d{2})')
close_re = re.compile(r'Deadline for applications: (\d{1,2})([a-z]{2})? (of )?([a-zA-Z]{3,}) (20\d{2})')

opp_headings = [
    'Background',
    'challenges',
    'Rewards and benefits',
    'Functional requirements',
    'Technical characteristics',
    'Operating conditions',
    'Deployment timescale',
    'Cost requirement and market opportunity',
    'Eligibility and assessment criteria',
    'IP and potential commercial route',

]

class KTN(Opportunity):

    def __init__(self, uri, title):
        super().__init__(uri, title)
        self.attributes["campaign_name"] = 'https://www.ktninnovationexchange.co.uk'
        self.attributes["account_name"] = settings["suitecrm"]["ktn_account_name"]
        self.attributes["account_id"] = settings["suitecrm"]["ktn_account_id"]

    def scrape(self, browser):
        if not super().scrape(browser):
            return
        content = browser.find_element_by_css_selector('.main-content .content .text')
        self.attributes["description"] = content.find_element_by_xpath('//h3[contains(text(), "Summary")]/following-sibling::p').text
        current_heading = 'background'
        current_text = None
        children = content.find_elements_by_xpath('//*[contains(@class, "description")]/*')
        for child in children:
            this_text = child.text.strip()
            if this_text in opp_headings:
                if current_heading:
                    self.attributes["description"] += f"\n\n{current_heading}\n\n{current_text}"
                    current_text = None
                current_heading = this_text
            else:
                if current_heading == 'Deployment timescale':
                    close_match = close_re.search(this_text)
                    if close_match:
                        self.attributes["date_closed"] = datetime.strftime(datetime.strptime(
                            f'{close_match.group(1)} {close_match.group(4)} {close_match.group(5)}', "%d %B %Y"), "%d/%m/%Y")
                    current_heading = None

                else:
                    if not current_text:
                        current_text = this_text
                    else:
                        current_text += this_text

        amount_match = re.findall(r'£[0-9,]+', self.attributes["description"])
        if amount_match:
            filtered = sorted(list(map(lambda x: int(re.sub(r'[^0-9]', '', x)), amount_match)), reverse=True)
            self.attributes["amount"] = filtered[0]

def login(browser):
    browser.get('https://www.ktninnovationexchange.co.uk/auth')
    form = browser.find_element_by_xpath('//*[@id="main-content"]/div/form')
    username = form.find_element_by_xpath('//*[@id="Email"]')
    password = form.find_element_by_xpath('//*[@id="Password"]')
    username.send_keys(settings["browser"]["ktn_username"])
    password.send_keys(settings["browser"]["ktn_password"])
    form.submit()

def search(browser, tried_auth=False):
    opportunities = []
    browser.get('https://www.ktninnovationexchange.co.uk/challenges')

    try:
        browser.find_element_by_xpath('/html/body[contains(@class, "logged-in")]')
    except NoSuchElementException:
        if tried_auth:
            raise
        login(browser)
        return search(browser, True)

    pages = browser.find_elements_by_xpath('//*[@id="js-challenge-pagination"]/li')
    current_page = 1

    while current_page <= len(pages) - 2:
        search_results = browser.find_elements_by_xpath('//*[@id="challenge-list-placeholder"]/div/div[contains(@class, "content")]')
        if not search_results:
            break
        for scrape in search_results:
            title = scrape.find_element_by_css_selector('.heading')
            link_id = scrape.find_element_by_css_selector('.btn')
            uri = link_id.get_attribute("href")
            id_match = link_id_re.search(uri)
            if id_match:
                opportunities.append(KTN(uri, title.text))
        current_page += 1
        try:
            next_page = browser.find_element_by_xpath(f'//*[@id="js-challenge-pagination"]/li/a[contains(text(), "{current_page}")]/..')
        except NoSuchElementException:
            break
        try:
            next_page.click()
            WebDriverWait(browser, 2).until(
                EC.staleness_of(link_id)
            )
        except TimeoutException:
            break

    print(f'==> Found {len(opportunities)} KTN competitions')
    for opp in opportunities:
        opp.scrape(browser)

    return opportunities
