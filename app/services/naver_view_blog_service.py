import os
from dotenv import load_dotenv
from typing import List
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .keyword_search_service import KeywordSearchService
from ..config.webdriver_config import setup_chrome_driver
import app.config as config
from flask import current_app

# driver = setup_chrome_driver()

load_dotenv()


class CommonKeywordResponse:
    def __init__(self, blog_id, publish_date):
        self.blogId = blog_id
        self.publishDate = publish_date

    def to_dict(self):
        return {"blogId": self.blogId, "publishDate": self.publishDate}


class NaverViewBlogService(KeywordSearchService):
    def __init__(self):
        self.driver = setup_chrome_driver()  # 여기에 추가
        self.baseUrl = current_app.config["NAVER_VIEW_BLOG_BASE_URL"]
        self.view_classes = {
            "view": {
                "class": current_app.config["NAVER_VIEW_BLOG_VIEW_CLASS"],
                "idClass": current_app.config["NAVER_VIEW_BLOG_VIEW_ID_CLASS"],
                "dateClass": current_app.config["NAVER_VIEW_BLOG_VIEW_DATE_CLASS"],
            },
            "influencer": {
                "class": current_app.config["NAVER_VIEW_BLOG_INFLUENCER_CLASS"],
                "idClass": current_app.config["NAVER_VIEW_BLOG_INFLUENCER_ID_CLASS"],
                "dateClass": current_app.config["NAVER_VIEW_BLOG_INFLUENCER_DATE_CLASS"],
            },
            "other": {
                "class": current_app.config["NAVER_VIEW_BLOG_OTHER_CLASS"],
                "idClass": current_app.config["NAVER_VIEW_BLOG_OTHER_ID_CLASS"],
                "dateClass": current_app.config["NAVER_VIEW_BLOG_OTHER_DATE_CLASS"],
            },
        }

    def get_list(self, query: str) -> List[CommonKeywordResponse]:
        self.driver.get(self.baseUrl + query)

        # wait = WebDriverWait(self.driver, 5)
        # wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.total_sub")))

        responses = []
        for _, view_class in self.view_classes.items():
            responses.extend(
                self.get_detail(
                    query, view_class["class"], view_class["idClass"], view_class["dateClass"]
                )
            )
        return responses

    def get_detail(
        self, query: str, parent_class: str, id_class: str, date_class: str
    ) -> List[CommonKeywordResponse]:
        parent_elements = self.driver.find_elements(By.CSS_SELECTOR, parent_class)
        responses = []
        for parent_element in parent_elements:
            id_element = parent_element.find_element(By.CSS_SELECTOR, id_class)
            date_element = parent_element.find_element(By.CSS_SELECTOR, date_class)
            if self.check_validity(id_element, date_element):
                id = self.get_id(query, id_element.get_attribute("href"))
                dt = date_element.text
                responses.append(CommonKeywordResponse(id, dt))
        return responses

    @staticmethod
    def check_validity(id_element, date_element) -> bool:
        id_url = id_element.get_attribute("href") if id_element else ""
        return (
            id_element is not None
            and date_element is not None
            and ("m.blog.naver.com" in id_url or "in.naver.com" in id_url)
        )

    @staticmethod
    def get_id(query: str, url: str) -> str:
        second_slash = url.index("/", 2)
        type = url[second_slash : url.index("/", second_slash)]
        return url.replace("https://in.naver.com/", "").replace("https://m.blog.naver.com/", "")


def main(query: str):
    naver_view_blog_service = NaverViewBlogService()
    try:
        responses = naver_view_blog_service.get_list(query)
        for response in responses:
            print(f"Blog ID: {response.blogId}, Publish Date: {response.publishDate}")
        return responses
    finally:
        naver_view_blog_service.driver.quit()


if __name__ == "__main__":
    import sys

    main(sys.argv[1])
