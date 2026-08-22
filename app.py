from flask import Flask
from database import init_db
from auth import auth_bp
from flask_cors import CORS

from attendance import attendance_bp
from leave import leave_bp
from payroll import payroll_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(attendance_bp, url_prefix='/api/attendance')
app.register_blueprint(leave_bp, url_prefix='/api/leave')
app.register_blueprint(payroll_bp, url_prefix='/api/payroll')
app.register_blueprint(auth_bp, url_prefix="/api/auth")

init_db()

if __name__ == '__main__':
    app.run(debug=True, port=5000)