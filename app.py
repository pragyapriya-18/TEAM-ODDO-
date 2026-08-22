from flask import Flask
from attendance import attendance_bp
from leave import leave_bp

app = Flask(__name__)

app.register_blueprint(attendance_bp, url_prefix='/api/attendance')
app.register_blueprint(leave_bp, url_prefix='/api/leave')

if __name__ == '__main__':
    app.run(debug=True, port=5000)