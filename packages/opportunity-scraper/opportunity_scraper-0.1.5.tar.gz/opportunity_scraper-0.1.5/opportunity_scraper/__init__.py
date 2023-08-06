import json
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient
from selenium import webdriver
from .settings import settings
from . import govuk, ktn

__all__ = ['govuk', 'ktn']

def run():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--window-size=1920x1080")
    browser = webdriver.Chrome(settings["browser"]["chromedriver"], options=chrome_options)
    govuk_opps = govuk.search(browser)
    ktn_opps = ktn.search(browser)
    browser.quit()

    client = BackendApplicationClient(client_id=settings["oauth"]["client_id"])
    session = OAuth2Session(client=client)
    session.fetch_token(token_url=settings["oauth"]["token_url"],
                        client_id=settings["oauth"]["client_id"],
                        client_secret=settings["oauth"]["client_secret"])

    for opp in govuk_opps + ktn_opps:
        req = session.post(f'{settings["suitecrm"]["api_url"]}/V8/module',
                           json={"data": opp.__dict__})
        title = opp.attributes["name"]
        if req.status_code == 201:
            print(f'Created opportunity: "{title}"')
        else:
            error = json.loads(req.text)["errors"]["detail"]
            print(f'Error creating opportunity: "{title}"')
            print(f'  "{error}"')
            