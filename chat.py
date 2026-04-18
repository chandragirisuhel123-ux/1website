from flask import (
    Blueprint,
    current_app,
    jsonify,
    render_template,
    request,
    send_from_directory,
    url_for,
)
from flask_login import current_user, login_required

from ..services.chatbot_loader import get_chatbot_answer, get_response_images


chat_bp = Blueprint("chat", __name__)


@chat_bp.route("/chat")
@login_required
def chat():
    return render_template("chat.html", user=current_user)


@chat_bp.route("/chat/message", methods=["POST"])
@login_required
def chat_message():
    payload = request.get_json(silent=True) or {}
    message = (payload.get("message") or "").strip()

    if not message:
        return jsonify({"error": "Message is required."}), 400

    answer = get_chatbot_answer(message)
    image_urls = [
        url_for("chat.legacy_asset", filename=filename)
        for filename in get_response_images(message)
    ]

    return jsonify(
        {
            "user": message,
            "answer": answer,
            "images": image_urls,
        }
    )


@chat_bp.route("/assets/<path:filename>")
@login_required
def legacy_asset(filename):
    return send_from_directory(current_app.config["LEGACY_ASSET_DIR"], filename)
