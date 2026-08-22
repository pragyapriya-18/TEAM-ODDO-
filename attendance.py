from flask import Blueprint, request, jsonify
from datetime import datetime
from database import get_db_connection

attendance_bp = Blueprint('attendance', __name__)

@attendance_bp.route('/check-in', methods=['POST'])
def check_in():
    data = request.get_json() or {}
    employee_id = data.get('employee_id')

    if not employee_id:
        return jsonify({"success": False, "message": "Employee ID is required"}), 400

    now = datetime.now()
    today = now.strftime("%Y-%m-%d")

    conn = get_db_connection()
    cursor = conn.cursor()

    existing = cursor.execute(
        'SELECT * FROM attendance WHERE employee_id = ? AND date = ?',
        (employee_id, today)
    ).fetchone()

    if existing:
        conn.close()
        return jsonify({"success": False, "message": "Already checked in today"}), 400

    check_in_time = now.strftime("%H:%M:%S")
    cursor.execute(
        'INSERT INTO attendance (employee_id, date, check_in, status) VALUES (?, ?, ?, ?)',
        (employee_id, today, check_in_time, 'Present')
    )
    conn.commit()
    conn.close()

    return jsonify({"success": True, "message": "Checked in successfully"}), 200

@attendance_bp.route('/check-out', methods=['POST'])
def check_out():
    data = request.get_json() or {}
    employee_id = data.get('employee_id')
    
    if not employee_id:
        return jsonify({"success": False, "message": "Employee ID is required"}), 400

    today = datetime.now().strftime("%Y-%m-%d")
    check_out_time = datetime.now().strftime("%H:%M:%S")

    conn = get_db_connection()
    cursor = conn.cursor()

    existing = cursor.execute(
        'SELECT * FROM attendance WHERE employee_id = ? AND date = ?',
        (employee_id, today)
    ).fetchone()

    if not existing:
        conn.close()
        return jsonify({"success": False, "message": "No check-in record found for today"}), 404

    cursor.execute(
        'UPDATE attendance SET check_out = ? WHERE employee_id = ? AND date = ?',
        (check_out_time, employee_id, today)
    )
    conn.commit()
    conn.close()

    return jsonify({"success": True, "message": "Checked out successfully"}), 200

@attendance_bp.route('/status/<employee_id>', methods=['GET'])
def get_status(employee_id):
    conn = get_db_connection()
    records = conn.execute(
        'SELECT * FROM attendance WHERE employee_id = ?', (employee_id,)
    ).fetchall()
    conn.close()

    return jsonify({"success": True, "data": [dict(r) for r in records]}), 200