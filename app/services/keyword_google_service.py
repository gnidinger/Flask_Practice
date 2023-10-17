import os
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .keyword_search_service import KeywordSearchService
from ..config.webdriver_config import setup_chrome_driver
from flask import current_app
from typing import List, Optional

load_dotenv()


class KeywordGoogleService:
    def __init__(self):
        self.driver = setup_chrome_driver()

        with current_app.app_context():
            self.base_url = current_app.config["KEYWORD_GOOGLE_BASE_URL"]
            self.target = current_app.config["KEYWORD_GOOGLE_TARGET"]
            self.target_attr = current_app.config["KEYWORD_GOOGLE_TARGET_ATTR"]

    def get_list(self, query: str) -> Optional[List[str]]:
        self.driver.get(self.base_url + query)

        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, self.target))
            )
            elements = self.driver.find_elements(By.CSS_SELECTOR, self.target)
            if elements:
                return [element.get_attribute(self.target_attr) for element in elements]
            else:
                return None
        except Exception as e:
            print(e)

    def __del__(self):
        if self.driver:
            self.driver.quit()


def main(query: str):
    keyword_google_service = KeywordGoogleService()
    try:
        result = keyword_google_service.get_list(query)
        print(result)
        return result
    except Exception as e:
        print(e)


if __name__ == "__main__":
    import sys

    main(sys.argv[1])
