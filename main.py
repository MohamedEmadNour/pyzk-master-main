from flask import Flask, jsonify , request
from zk import ZK
import pyodbc
from example.live_capture import get_attendance
from example.sync_time import synctime
from connectionstring import conn_str,fetch_devices
from control import control_function
import threading
from models import db
from config import Config
from flask_jwt_extended import JWTManager
from authorization import dynamic_function_authorize
from example.setuserfrommachintodb import get_user
import requests
from example.set_user import sendUserDataToMachine

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
jwt = JWTManager(app)
# Global variables
running = False
attendance_thread = None

def attendance_fetching():  
    global running
    while running:
        with pyodbc.connect(conn_str) as db_conn:
            cursor = db_conn.cursor()
            devices = fetch_devices(cursor)
            result = get_attendance(devices)
            if isinstance(result, str):
                print(f'Error: {result}')

@app.route('/start_attendance', methods=['Get'])
# @dynamic_function_authorize('GetAttendanceLogs')
def start_attendance():
    global running, attendance_thread
    if not running:
        running = True
        control_function(True)
        attendance_thread = threading.Thread(target=attendance_fetching)
        attendance_thread.start()
        return jsonify({'status': 'Attendance fetching started'})
    else:
        return jsonify({'status': 'Attendance fetching already running'})

@app.route('/stop_attendance', methods=['GET'])
def stop_attendance():
    global running
    if running:
        running = False
        control_function(False)
        return jsonify({'status': 'Attendance fetching stopped'})
    else:
        return jsonify({'status': 'Attendance fetching is not running'})

@app.route('/synctime', methods=['GET'])
def synctime():
 synctime
@app.route('/user_fetching', methods=['GET'])
def user_fetching():  
        with pyodbc.connect(conn_str) as db_conn:
            cursor = db_conn.cursor()
            devices = fetch_devices(cursor)
            get_user(devices)   
            return jsonify({'status': 'Done fetching users'})
#  @app.errorhandler(422)
#  def handle_unprocessable_entity(err):
#     exc = getattr(err, 'exc')
#     if exc:
#         return jsonify({"msg": "Unprocessable Entity", "errors": exc.messages}), 422
#     return jsonify({"msg": "Unprocessable Entity"}), 422    

# @app.errorhandler(400)
# def handle_bad_request(err):
#     return jsonify({"msg": "Bad Request"}), 400



@app.route('/SendDataToMachine', methods=['POST'])
def SendDataToMachine():
    try:
        data = request.get_json()
        userData = data.get('userData')
        zkMachine = data.get('zkMachine')

        temp = userData.get('Template')
        userDetails = {
            'userid': userData.get('userid'),
            'Privilege': userData.get('Privilege'),
            'Name': userData.get('Name'),
            'uid': userData.get('Uid'),
            'Size': userData.get('Size'),
            'Fid': userData.get('Fid'),
            'Valid': userData.get('Valid')
        }

        # Assuming sendUserDataToMachine is defined elsewhere
        sendUserDataToMachine(template=temp, userData=userDetails, zk=zkMachine)

        return jsonify({"message": "Data sent to machine successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)