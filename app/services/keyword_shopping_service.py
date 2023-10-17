import os
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .keyword_search_service import KeywordSearchService
from ..config.webdriver_config import setup_chrome_driver
from flask import current_app
from typing import List, Optional
import urllib.parse

load_dotenv()


class KeywordShoppingService:
    def __init__(self):
        self.driver = setup_chrome_driver()

        with current_app.app_context():
            self.base_url = current_app.config["KEYWORD_NAVER_SHOPPING_BASE_URL"]
            self.target_attr = current_app.config["KEYWORD_NAVER_SHOPPING_TARGET_ATTR"]
            self.attr_startswith = current_app.config["KEYWORD_NAVER_SHOPPING_ATTR_STARTSWITH"]

    def get_list(self, query: str) -> Optional[List[str]]:
        self.driver.get(self.base_url + query)

        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, f"[{self.target_attr}]"))
            )
            elements = self.driver.find_elements(By.CSS_SELECTOR, f"[{self.target_attr}]")
            if elements:
                responses = [
                    urllib.parse.unquote(
                        element.get_attribute(self.target_attr).split("i:")[1].split(",")[0]
                    )
                    for element in elements
                    if element.get_attribute(self.target_attr).startswith(self.attr_startswith)
                ]
                return responses
            else:
                return []

        except Exception as e:
            print(e)
        finally:
            self.driver.quit()


def main(query: str):
    keyword_shopping_service = KeywordShoppingService()
    try:
        result = keyword_shopping_service.get_list(query)
        print(result)
        return result
    except Exception as e:
        print(e)


if __name__ == "__main__":
    import sys

    main(sys.argv[1])
