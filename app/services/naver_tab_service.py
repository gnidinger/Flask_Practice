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

base_url = config.NAVER_TAB_BASE_URL
target = config.NAVER_TAB_TARGET_CLASS


class NaverTabService(KeywordSearchService):
    def __init__(self):
        self.base_url = base_url
        self.target = target

    def get_list(self, query):
        driver.get(self.base_url + query)

        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, self.target))
            )
            tabs_elements = driver.find_elements(By.CSS_SELECTOR, self.target)
            if tabs_elements:
                tabs = [self.reason_empty(tab.text) for tab in tabs_elements]
                return {"tabs": ", ".join(tabs)}
            else:
                return None

        except Exception as e:
            print(e)

    @staticmethod
    def reason_empty(text):
        return text.replace("이 정보가 표시된 이유", "")


def main(query: str):
    naver_tab_service = NaverTabService()
    try:
        result = naver_tab_service.get_list(query)
        print(result)
    finally:
        driver.quit()


if __name__ == "__main__":
    import sys

    main(sys.argv[1])
