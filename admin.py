from flask import Blueprint, render_template

from auth.decorators import admin_required
from models import User


admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/admin")
@admin_required
def admin():
    users = User.query.order_by(User.id.asc()).all()
    return render_template("admin.html", users=users)
