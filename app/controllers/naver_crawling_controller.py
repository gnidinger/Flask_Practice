from flask import Flask, request, jsonify
from services import NaverTabService, NaverViewBlogService, NaverVisitorService

app = Flask(__name__)

strategies = {
    "naver_tab": NaverTabService(),
    "naver_view_blog": NaverViewBlogService(),
    "naver_visitor": NaverVisitorService(),
}


@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("query")
    strategy_type = request.args.get("strategy_type")

    strategy = strategies.get(strategy_type)
    if not strategy:
        return jsonify({"error": "Invalid Strategy Type"}), 400

    result = strategy.get_list(query)
    return jsonify(result)


if __name__ == __main__:
    app.run()
