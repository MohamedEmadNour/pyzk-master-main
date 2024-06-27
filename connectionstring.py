import pyodbc
from zk import const
import json

# Database connection details
conn_str = (
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=.;'
    'DATABASE=ZKTecoAttendance;'
    'Trusted_Connection=yes;'
    'TrustServerCertificate=yes;'
)
def connect_to_db():
    try:
        connection = pyodbc.connect(conn_str)
        return connection
    except pyodbc.Error as e:
        print(f"Error connecting to database: {e}")
        return None
def insert_attendance(cursor, log, DeviceId):
    query = """
    IF NOT EXISTS (SELECT 1 FROM tbAttendanceLogs WHERE user_id = ? AND Timestamp = ?)
    BEGIN 
        INSERT INTO tbAttendanceLogs (user_id, Timestamp, Status, Punch, tbDeviceId,uid )
        VALUES (?, ?, ?, ?, ?,?)
    END
    """
    cursor.execute(query, log.user_id, log.timestamp, log.user_id, log.timestamp, log.status, log.punch, DeviceId,log.uid)
def insert_device_log(cursor , DeviceId,StatusForConnect):
    query = """
    BEGIN 
        INSERT INTO tbDeviceLogs (tbDeviceId, StatusForConnect)
        VALUES (?, ?)
    END
    """
    cursor.execute(query, DeviceId, StatusForConnect)
def fetch_devices(cursor):
    query = "SELECT Id, IPAddress, Port, CommKey FROM tbDevice where IsDeleted =0"
    cursor.execute(query)
    return cursor.fetchall()

def insert_user(cursor, user, device_id):
    privilege = 0
    if user.privilege == const.USER_ADMIN:
        privilege = 1
    cursor.execute('''INSERT INTO tbUserMachine (uid, tbDeviceId, name, privilege, password, group_id, user_id, CreationDate, IsDeleted)
                      VALUES (?, ?, ?, ?, ?, ?, ?, GETDATE(), 0)''',
                   (user.uid, device_id, user.name, privilege, user.password, user.group_id, user.user_id))
def get_user_machine_id(cursor, uid, device_id):
    cursor.execute('''SELECT Id FROM tbUserMachine WHERE uid = ? AND tbDeviceId = ? AND IsDeleted = 0''', (uid, device_id))
    result = cursor.fetchone()
    return result[0] if result else None
def insert_template(cursor, template, user_machine_id):
    template_data = template.json_pack()["template"]  # Extract the raw template string
    print(user_machine_id, template.size, template.fid, template.valid, template_data, template.mark)
    cursor.execute('''INSERT INTO tbUserTemplates (tbUserMachineId, size, fid, valid, template, mark, CreationDate, IsDeleted)
                      VALUES (?, ?, ?, ?, ?, ?, GETDATE(), 0)''',
                   (user_machine_id, template.size, template.fid, template.valid, template_data, template.mark))
def update_old_data(cursor, table, id):
    cursor.execute(f'''UPDATE {table} SET IsDeleted = 1, LastEditDate = GETDATE() WHERE Id = ?''', (id,))

def check_user_exists(cursor, user, device_id):
    cursor.execute('''SELECT Id, name, privilege, password, group_id, user_id FROM tbUserMachine WHERE uid = ? AND tbDeviceId = ? AND IsDeleted = 0''', (user.uid, device_id))
    return cursor.fetchone()

def check_template_exists(cursor, template, user_machine_id):
    template_data = template.json_pack()["template"]  # Extract the raw template string
    query = '''
        SELECT Id 
        FROM tbUserTemplates 
        WHERE tbUserMachineId = ? 
          AND size = ? 
          AND fid = ? 
          AND valid = ? 
          AND CAST(template AS nvarchar(max)) = ? 
          AND IsDeleted = 0
    '''
   
    # Print the full query for debugging
    formatted_query = query.replace('?', '{}').format(user_machine_id, template.size, template.fid, template.valid, repr(template_data))
    print("Executing query: ", formatted_query)
    
    cursor.execute(formatted_query)
    return cursor.fetchone()