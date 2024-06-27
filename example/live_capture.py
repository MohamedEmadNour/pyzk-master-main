from zk import ZK
from connectionstring import connect_to_db,insert_device_log,insert_attendance
from threading import Thread
import time







def process_device(device):
    zk = ZK(device.IPAddress, port=device.Port, timeout=5, password=device.CommKey, force_udp=False, ommit_ping=False)
    attendance_list = []
    is_connected = None  # Track the initial connection status

    while True:
        try:
            # Connect to the machine
            conn = zk.connect()
            if is_connected is None or not is_connected:
                # Log the initial connection status or status change
                db_conn = connect_to_db()
                cursor = db_conn.cursor()
                insert_device_log(cursor, device.Id, True)
                db_conn.commit()
                db_conn.close()
                is_connected = True
            print(f"Successfully connected to device {device.IPAddress}")
        except Exception as e:
            if is_connected is None:
                # Log the initial disconnection status
                db_conn = connect_to_db()
                cursor = db_conn.cursor()
                insert_device_log(cursor, device.Id, False)
                db_conn.commit()
                db_conn.close()
                is_connected = False
            elif is_connected:
                # Log the disconnection status change
                db_conn = connect_to_db()
                cursor = db_conn.cursor()
                insert_device_log(cursor, device.Id, False)
                db_conn.commit()
                db_conn.close()
                is_connected = False
            print(f"Error connecting to device {device.IPAddress}: {e}")
            time.sleep(10)  # Retry the same device after 10 seconds
            continue

        try:
            # Connect to the database
            db_conn = connect_to_db()
            if db_conn:
                cursor = db_conn.cursor()
            else:
                print("Failed to connect to the database")
                time.sleep(10)  # Retry database connection after 10 seconds
                continue

            for attendance in conn.live_capture():
                if attendance is not None :
                    attendance_list.append(attendance)
                    insert_attendance(cursor, attendance, device.Id)
                    db_conn.commit()
        except Exception as e:
            print(f"Error processing device {device.IPAddress}: {e}")
            time.sleep(10)  # Wait for 10 seconds before retrying
        finally:
            if db_conn:
                db_conn.close()

        time.sleep(10)  # Check for new attendance data every 10 seconds

def get_attendance(devices):
    threads = []
    for device in devices:
        thread = Thread(target=process_device, args=(device,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()
