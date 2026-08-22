from flask import Blueprint, request, jsonify
from datetime import datetime

attendance_bp = Blueprint('attendance', __name__)

# Temporary storage for attendance
attendance_records = []

@attendance_bp.route('/check-in', methods=['POST'])
def check_in():
    data = request.get_json()
    employee_id = data.get('employee_id')

    if not employee_id:
        return jsonify({"success": False, "message": "Employee ID is required"}), 400

    now = datetime.now()
    today = now.strftime("%Y-%m-%d")

    # Check if already checked in today
    for record in attendance_records:
        if record['employee_id'] == employee_id and record['date'] == today:
            return jsonify({"success": False, "message": "Already checked in today"}), 400

    record = {
        "id": len(attendance_records) + 1,
        "employee_id": employee_id,
        "date": today,
        "check_in": now.strftime("%H:%M:%S"),
        "check_out": None,
        "status": "Present"
    }
    attendance_records.append(record)
    return jsonify({"success": True, "message": "Checked in successfully", "data": record}), 200

@attendance_bp.route('/check-out', methods=['POST'])
def check_out():
    data = request.get_json()
    employee_id = data.get('employee_id')
    today = datetime.now().strftime("%Y-%m-%d")

    for record in attendance_records:
        if record['employee_id'] == employee_id and record['date'] == today:
            record['check_out'] = datetime.now().strftime("%H:%M:%S")
            return jsonify({"success": True, "message": "Checked out successfully", "data": record}), 200

    return jsonify({"success": False, "message": "No check-in record found for today"}), 404

@attendance_bp.route('/status/<employee_id>', methods=['GET'])
def get_status(employee_id):
    records = [r for r in attendance_records if r['employee_id'] == employee_id]
    return jsonify({"success": True, "data": records}), 200