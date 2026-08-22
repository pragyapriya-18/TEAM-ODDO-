from flask import Blueprint, request, jsonify
from database import get_db_connection

leave_bp = Blueprint('leave', __name__)

@leave_bp.route('/apply', methods=['POST'])
def apply_leave():
    data = request.get_json() or {}
    employee_id = data.get('employee_id')
    reason = data.get('reason')
    date = data.get('date')

    if not employee_id or not date:
        return jsonify({"success": False, "message": "Employee ID and Date required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO leaves (employee_id, reason, date, status) VALUES (?, ?, ?, ?)',
        (employee_id, reason, date, 'Pending')
    )
    conn.commit()
    conn.close()

    return jsonify({"success": True, "message": "Leave applied successfully"}), 200

@leave_bp.route('/action/<int:leave_id>', methods=['PUT'])
def update_leave_status(leave_id):
    data = request.get_json() or {}
    action = data.get('status')

    if action not in ['Approved', 'Rejected']:
        return jsonify({"success": False, "message": "Status must be Approved or Rejected"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE leaves SET status = ? WHERE id = ?', (action, leave_id))
    conn.commit()
    conn.close()

    return jsonify({"success": True, "message": f"Leave {action.lower()} successfully"}), 200

@leave_bp.route('/all', methods=['GET'])
def get_all_leaves():
    conn = get_db_connection()
    records = conn.execute('SELECT * FROM leaves').fetchall()
    conn.close()

    return jsonify({"success": True, "data": [dict(r) for r in records]}), 200