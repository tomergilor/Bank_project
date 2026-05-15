from flask import Flask, jsonify, redirect, render_template, request, session, url_for

from app.database import get_accounts_for_user, get_user_by_username


app = Flask(__name__)
app.secret_key = "bank-project-secret-key"


def build_user_payload(user_row) -> dict:
    return {
        "id": user_row["id"],
        "username": user_row["username"],
        "first_name": user_row["first_name"],
        "last_name": user_row["last_name"],
        "role": user_row["role"],
        "is_active": bool(user_row["is_active"]),
    }


@app.route("/", methods=["GET"])
def home():
    return render_template("login.html", error_message="")


@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "").strip()

    user = get_user_by_username(username)
    if not user or user["password"] != password:
        return render_template("login.html", error_message="Invalid username or password."), 401

    if not user["is_active"]:
        return render_template("login.html", error_message="User is inactive."), 403

    session["user_id"] = user["id"]
    session["username"] = user["username"]
    return redirect(url_for("dashboard"))


@app.route("/dashboard", methods=["GET"])
def dashboard():
    username = session.get("username")
    if not username:
        return redirect(url_for("home"))

    user = get_user_by_username(username)
    if not user:
        session.clear()
        return redirect(url_for("home"))

    accounts = get_accounts_for_user(user["id"])
    return render_template(
        "dashboard.html",
        user=build_user_payload(user),
        accounts=accounts,
    )


@app.route("/logout", methods=["GET"])
def logout():
    session.clear()
    return redirect(url_for("home"))


@app.route("/api/health", methods=["GET"])
def api_health():
    return jsonify({"status": "ok"})


@app.route("/api/login", methods=["POST"])
def api_login():
    data = request.get_json(silent=True) or {}
    username = str(data.get("username", "")).strip()
    password = str(data.get("password", "")).strip()

    user = get_user_by_username(username)
    if not user or user["password"] != password:
        return jsonify({"success": False, "message": "Invalid credentials"}), 401

    if not user["is_active"]:
        return jsonify({"success": False, "message": "User is inactive"}), 403

    return jsonify({"success": True, "user": build_user_payload(user)})


@app.route("/api/users/<username>", methods=["GET"])
def api_get_user(username: str):
    user = get_user_by_username(username)
    if not user:
        return jsonify({"success": False, "message": "User not found"}), 404

    return jsonify(
        {
            "success": True,
            "user": build_user_payload(user),
            "accounts": [
                {
                    "account_number": account["account_number"],
                    "account_type": account["account_type"],
                    "balance": account["balance"],
                    "currency": account["currency"],
                }
                for account in get_accounts_for_user(user["id"])
            ],
        }
    )


if __name__ == "__main__":
    app.run(debug=True, port=5000)
