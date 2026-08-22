from flask import Blueprint, request, jsonify
from datetime import datetime

notifications_bp = Blueprint('notifications', __name__)

# Temporary storage
notifications = []
next_id = 1


def _add_notification(employee_id, message, category="General"):
    """Internal helper — call this from attendance.py / leave.py / payroll.py
    to push a notification when something happens (e.g. leave approved)."""
    global next_id
    note = {
        "id": next_id,
        "employee_id": employee_id,   # None/"ALL" for broadcast to everyone
        "category": category,          # e.g. "Leave", "Attendance", "Payroll", "HR Alert"
        "message": message,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "read": False,
    }
    notifications.append(note)
    next_id += 1
    return note


@notifications_bp.route('/send', methods=['POST'])
def send_notification():
    """Admin/HR: manually push a notification (e.g. 'Payroll processing on 28th')."""
    data = request.get_json()
    employee_id = data.get('employee_id', 'ALL')
    message = data.get('message')
    category = data.get('category', 'HR Alert')

    if not message:
        return jsonify({"success": False, "message": "message is required"}), 400

    note = _add_notification(employee_id, message, category)
    return jsonify({"success": True, "message": "Notification sent", "data": note}), 201


@notifications_bp.route('/<employee_id>', methods=['GET'])
def get_notifications(employee_id):
    """Get all notifications for a specific employee, plus any broadcast ones."""
    result = [n for n in notifications if n['employee_id'] in (employee_id, 'ALL')]
    result.sort(key=lambda n: n['id'], reverse=True)
    return jsonify({"success": True, "data": result}), 200


@notifications_bp.route('/read/<int:notification_id>', methods=['POST'])
def mark_read(notification_id):
    note = next((n for n in notifications if n['id'] == notification_id), None)
    if not note:
        return jsonify({"success": False, "message": "Notification not found"}), 404
    note['read'] = True
    return jsonify({"success": True, "message": "Marked as read", "data": note}), 200


@notifications_bp.route('/unread-count/<employee_id>', methods=['GET'])
def unread_count(employee_id):
    count = len([n for n in notifications if n['employee_id'] in (employee_id, 'ALL') and not n['read']])
    return jsonify({"success": True, "data": {"unread": count}}), 200