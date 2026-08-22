from flask import Blueprint, request, jsonify
from database import get_db_connection

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/signup", methods=["POST"])
def signup():

    data = request.get_json()

    employee_id = data.get("employee_id")
    email = data.get("email")
    password = data.get("password")
    role = data.get("role")

    if not employee_id or not email or not password or not role:
        return jsonify({
            "success": False,
            "message": "All fields are required"
        }), 400

    if role not in ["Employee", "HR"]:
        return jsonify({
            "success": False,
            "message": "Invalid role"
        }), 400

    conn = get_db_connection()

    try:
        conn.execute("""
            INSERT INTO users
            (employee_id, email, password, role)
            VALUES (?, ?, ?, ?)
        """, (
            employee_id,
            email,
            password,
            role
        ))

        conn.execute("""
            INSERT INTO employees
            (employee_id)
            VALUES (?)
        """, (employee_id,))

        conn.commit()

        return jsonify({
            "success": True,
            "message": "Account created successfully"
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "message": str(e)
        }), 400

    finally:
        conn.close()


@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    conn = get_db_connection()

    user = conn.execute("""
        SELECT *
        FROM users
        WHERE email = ?
        AND password = ?
    """, (email, password)).fetchone()

    conn.close()

    if not user:
        return jsonify({
            "success": False,
            "message": "Invalid email or password"
        }), 401

    return jsonify({
        "success": True,
        "message": "Login successful",
        "user": {
            "employee_id": user["employee_id"],
            "email": user["email"],
            "role": user["role"]
        }
    })