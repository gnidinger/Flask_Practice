import os
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from keyword_search_service import KeywordSearchService
from config.webdriver_config import setup_chrome_driver
import app.config as config


driver = setup_chrome_driver()

load_dotenv()

base_url = config.NAVER_VISITOR_BASE_URL
target = config.NAVER_VISITOR_TARGET
attr = config.NAVER_VISITOR_TARGET_ATTR


class NaverVisitorService(KeywordSearchService):
    def __init__(self):
        self.base_url = base_url
        self.target = target
        self.attr = attr

    def get_list(self, query):
        driver.get(self.base_url + query)

        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, self.target))
            )
            target_elements = driver.find_elements(By.CSS_SELECTOR, self.target)
            if target_elements:
                responses = [
                    {"visitorCount": self.blank_empty(element.get_attribute(self.attr))}
                    for element in target_elements
                ]
                WebDriverWait(driver, 10)
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
    finally:
        driver.quit()


if __name__ == "__main__":
    import sys

    main(sys.argv[1])
