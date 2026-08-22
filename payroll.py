from flask import Blueprint, request, jsonify

payroll_bp = Blueprint('payroll', __name__)

# Temporary storage — same pattern as attendance_records
payroll_records = [
    {"employee_id": "DF-101", "name": "Ananya Rao", "salary": 85000, "last_updated": None},
    {"employee_id": "DF-102", "name": "Rahul Mehta", "salary": 95000, "last_updated": None},
    {"employee_id": "DF-103", "name": "Priya Nair", "salary": 70000, "last_updated": None},
]

from datetime import datetime


@payroll_bp.route('/all', methods=['GET'])
def get_all_payroll():
    """Admin: view payroll for every employee."""
    return jsonify({"success": True, "data": payroll_records}), 200


@payroll_bp.route('/<employee_id>', methods=['GET'])
def get_payroll(employee_id):
    """Employee: read-only view of own salary."""
    record = next((r for r in payroll_records if r['employee_id'] == employee_id), None)
    if not record:
        return jsonify({"success": False, "message": "Employee not found"}), 404
    return jsonify({"success": True, "data": record}), 200


@payroll_bp.route('/<employee_id>', methods=['PUT'])
def update_payroll(employee_id):
    """Admin: update an employee's salary structure."""
    data = request.get_json()
    new_salary = data.get('salary')

    if new_salary is None:
        return jsonify({"success": False, "message": "salary is required"}), 400
    if not isinstance(new_salary, (int, float)) or new_salary < 0:
        return jsonify({"success": False, "message": "salary must be a positive number"}), 400

    record = next((r for r in payroll_records if r['employee_id'] == employee_id), None)
    if not record:
        return jsonify({"success": False, "message": "Employee not found"}), 404

    record['salary'] = new_salary
    record['last_updated'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return jsonify({"success": True, "message": "Salary updated", "data": record}), 200


@payroll_bp.route('/slip/<employee_id>', methods=['GET'])
def salary_slip(employee_id):
    """Simple generated salary slip — enough for a demo report."""
    record = next((r for r in payroll_records if r['employee_id'] == employee_id), None)
    if not record:
        return jsonify({"success": False, "message": "Employee not found"}), 404

    basic = record['salary'] * 0.5
    hra = record['salary'] * 0.2
    allowances = record['salary'] - basic - hra

    slip = {
        "employee_id": record['employee_id'],
        "name": record['name'],
        "month": datetime.now().strftime("%B %Y"),
        "basic": round(basic, 2),
        "hra": round(hra, 2),
        "allowances": round(allowances, 2),
        "gross_salary": record['salary'],
    }
    return jsonify({"success": True, "data": slip}), 200