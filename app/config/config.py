import os

KEYWORD_NAVER_BASE_URL = "https://m.search.naver.com/search.naver?query="
KEYWORD_NAVER_TARGET_CLASS = "a._slog_visible"

KEYWORD_NAVER_SHOPPING_BASE_URL = "https://search.shopping.naver.com/search/all?query="
KEYWORD_NAVER_SHOPPING_TARGET_ATTR = "data-nclick"
KEYWORD_NAVER_SHOPPING_ATTR_STARTSWITH = "N=a:rel.keyword,i:"

KEYWORD_GOOGLE_BASE_URL = "http://suggestqueries.google.com/complete/search?output=toolbar&q="
KEYWORD_GOOGLE_TARGET = "suggestion"
KEYWORD_GOOGLE_TARGET_ATTR = "data"

NAVER_TAB_BASE_URL = "https://m.search.naver.com/search.naver?query="
NAVER_TAB_TARGET_CLASS = "div.bx._rk_hlimit"

NAVER_VISITOR_BASE_URL = "https://blog.naver.com/NVisitorgp4Ajax.nhn?blogId="
NAVER_VISITOR_TARGET = "visitorcnt"
NAVER_VISITOR_TARGET_ATTR = "cnt"

NAVER_VIEW_BLOG_BASE_URL = "https://m.search.naver.com/search.naver?query="
NAVER_VIEW_BLOG_VIEW_CLASS = "div.total_sub"
NAVER_VIEW_BLOG_VIEW_ID_CLASS = "a.sub_thumb"
NAVER_VIEW_BLOG_VIEW_DATE_CLASS = "span.sub_time.sub_txt"
NAVER_VIEW_BLOG_INFLUENCER_CLASS = "div.user_box_2lines"
NAVER_VIEW_BLOG_INFLUENCER_ID_CLASS = "a.thumb_group"
NAVER_VIEW_BLOG_INFLUENCER_DATE_CLASS = "div.group_inner:nth-child(2) div.info:nth-child(2)"
NAVER_VIEW_BLOG_OTHER_CLASS = "div.user_box"
NAVER_VIEW_BLOG_OTHER_ID_CLASS = "a.thumb_group"
NAVER_VIEW_BLOG_OTHER_DATE_CLASS = "div.info"
