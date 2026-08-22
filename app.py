from flask import Flask
from flask_cors import CORS

from attendance import attendance_bp
from leave import leave_bp
from payroll import payroll_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(attendance_bp, url_prefix='/api/attendance')
app.register_blueprint(leave_bp, url_prefix='/api/leave')
app.register_blueprint(payroll_bp, url_prefix='/api/payroll')

if __name__ == '__main__':
    app.run(debug=True, port=5000)