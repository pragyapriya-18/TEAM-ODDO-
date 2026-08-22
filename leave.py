from flask import Blueprint, request, jsonify

leave_bp = Blueprint('leave', __name__)

leave_requests = []

@leave_bp.route('/apply', methods=['POST'])
def apply_leave():
    data = request.get_json()
    employee_id = data.get('employee_id')
    reason = data.get('reason')
    date = data.get('date')

    if not employee_id or not date:
        return jsonify({"success": False, "message": "Employee ID and Date required"}), 400

    request_item = {
        "id": len(leave_requests) + 1,
        "employee_id": employee_id,
        "reason": reason,
        "date": date,
        "status": "Pending"
    }
    leave_requests.append(request_item)
    return jsonify({"success": True, "message": "Leave applied successfully", "data": request_item}), 200

@leave_bp.route('/action/<int:leave_id>', methods=['PUT'])
def update_leave_status(leave_id):
    data = request.get_json()
    action = data.get('status')

    if action not in ['Approved', 'Rejected']:
        return jsonify({"success": False, "message": "Status must be Approved or Rejected"}), 400

    for item in leave_requests:
        if item['id'] == leave_id:
            item['status'] = action
            return jsonify({"success": True, "message": f"Leave {action.lower()} successfully", "data": item}), 200

    return jsonify({"success": False, "message": "Leave request not found"}), 404

@leave_bp.route('/all', methods=['GET'])
def get_all_leaves():
    return jsonify({"success": True, "data": leave_requests}), 200