import json
from flask import request, jsonify, Response
from ..services import (
    NaverTabService,
    NaverViewBlogService,
    NaverVisitorService,
    KeywordService,
    KeywordShoppingService,
    KeywordGoogleService,
)


def complex_handler(obj):
    if hasattr(obj, "to_dict"):
        return obj.to_dict()
    raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")


def configure_routes(app):
    def get_strategy(strategy_type):
        strategies = {
            "naver_tab": NaverTabService,
            "naver_view_blog": NaverViewBlogService,
            "naver_visitor": NaverVisitorService,
            "keyword_service": KeywordService,
            "keyword_shopping_service": KeywordShoppingService,
            "keyword_google_service": KeywordGoogleService,
        }
        strategy_cls = strategies.get(strategy_type)
        if not strategy_cls:
            return None
        return strategy_cls()

    @app.route("/api/search", methods=["GET"])
    def search():
        query = request.args.get("query")
        strategy_type = request.args.get("strategy_type")

        strategy = get_strategy(strategy_type)
        if not strategy:
            return jsonify({"error": "Invalid Strategy Type"}), 400

        result = strategy.get_list(query)
        response_data = json.dumps(result, default=complex_handler)
        return Response(response_data, content_type="application/json")
