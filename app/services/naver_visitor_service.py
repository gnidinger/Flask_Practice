import os
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .keyword_search_service import KeywordSearchService
from ..config.webdriver_config import setup_chrome_driver
import app.config as config
from flask import current_app


# driver = setup_chrome_driver()

load_dotenv()


class NaverVisitorService(KeywordSearchService):
    def __init__(self):
        self.driver = setup_chrome_driver()

        with current_app.app_context():
            self.base_url = current_app.config["NAVER_VISITOR_BASE_URL"]
            self.target = current_app.config["NAVER_VISITOR_TARGET"]
            self.attr = current_app.config["NAVER_VISITOR_TARGET_ATTR"]

    def get_list(self, query):
        self.driver.get(self.base_url + query)

        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, self.target))
            )
            target_elements = self.driver.find_elements(By.CSS_SELECTOR, self.target)
            if target_elements:
                responses = [
                    {"visitorCount": self.blank_empty(element.get_attribute(self.attr))}
                    for element in target_elements
                ]
                WebDriverWait(self.driver, 5)
                return responses
            else:
                return []

        except Exception as e:
            print(e)
            return []

    @staticmethod
    def blank_empty(text):
        return text if text else ""


def main(query: str):
    naver_visitor_service = NaverVisitorService()
    try:
        result = naver_visitor_service.get_list(query)
        print(result)
        return result
    finally:
        naver_visitor_service.driver.quit()


if __name__ == "__main__":
    import sys

    main(sys.argv[1])
