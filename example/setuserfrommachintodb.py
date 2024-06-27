from zk import ZK,const
from connectionstring import connect_to_db, insert_user, insert_template, get_user_machine_id, update_old_data, check_user_exists, check_template_exists
def safe_int(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0
def get_user(devices):
    for device in devices:
        zk = ZK(device.IPAddress, port=device.Port, timeout=5, password=device.CommKey, force_udp=False, ommit_ping=False)
        conn = None  # Initialize conn to None
        try:
            conn = zk.connect()
            print('Disabling device ...')
            conn.disable_device()
            db_conn = connect_to_db()
            cursor = db_conn.cursor()

            print('--- Get User ---')
            users = conn.get_users()

            # Insert users and commit
            for user in users:
                existing_user = check_user_exists(cursor, user, device.Id)
                privilege = 0
                if user.privilege == const.USER_ADMIN:
                    privilege = 1
                
                # Normalize values for comparison
                db_name = existing_user[1] if existing_user else ''
                db_privilege = existing_user[2] if existing_user else ''
                db_password = existing_user[3] if existing_user and existing_user[3] is not None else ''
                db_group_id = safe_int(existing_user[4]) if existing_user else 0
                db_user_id = safe_int(existing_user[5]) if existing_user else 0 

                machine_name = user.name if user.name is not None else ''
                machine_privilege = privilege
                machine_password = user.password if user.password is not None else ''
                machine_group_id = safe_int(user.group_id) if user.group_id is not None else 0
                machine_user_id = safe_int(user.user_id)

                # Debug output
                print("DB Data: ", repr(db_name), repr(db_privilege), repr(db_password), db_group_id, db_user_id)
                print("Machine Data: ", repr(machine_name), repr(machine_privilege), repr(machine_password), machine_group_id, machine_user_id)

                if (db_name, db_privilege, db_password, db_group_id, db_user_id) == (machine_name, machine_privilege, machine_password, machine_group_id, machine_user_id):
                    print(f'User {user.name} already exists and is unchanged.')
                    continue
                else:
                    if existing_user:
                        update_old_data(cursor, 'tbUserMachine', existing_user[0])
                    insert_user(cursor, user, device.Id)

            db_conn.commit()

            for user in users:
                user_machine_id = get_user_machine_id(cursor, user.uid, device.Id)
                print(f'Fetched user_machine_id: {user_machine_id}')

                print('--- Get Templates ---')
                for template in conn.get_templates():
                    existing_template = check_template_exists(cursor, template, user_machine_id)
                    if existing_template:
                        print(f'Template for user_machine_id {user_machine_id} already exists and is unchanged.')
                        continue
                    else:
                        if existing_template:
                            update_old_data(cursor, 'tbUserTemplates', existing_template[0])
                        insert_template(cursor, template, user_machine_id)

            db_conn.commit()
            db_conn.close()

            print("Voice Test ...")
            conn.test_voice()
            print('Enabling device ...')
            conn.enable_device()

        except Exception as e:
            print("Process terminated: {}".format(e))
        finally:
            if conn:
                conn.disconnect()
