# -*- coding: utf-8 -*-
import os
import sys
from zk.user import User
from zk.finger import Finger
import binascii

CWD = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.dirname(CWD)
sys.path.append(ROOT_DIR)

from zk import ZK, const
import zk
print("ZK library path: ", zk.__file__)

conn = None
ip = '192.168.1.201'

def sendUserDataToMachine(template , userData , zk):
    zk = ZK(zk['ip'], port=zk['port'], password=zk['password'])

    #zk = ZK(zk.ip, zk.port , zk.password)
    try:
        conn = zk.connect()
        print("Connected to the device")

    # Provided template data
        template_info = template
        # Convert the template from hex string to bytes
        template_bytes = binascii.unhexlify(template_info)
        # Create instances of User and Finger
        user = User(
            uid= userData['uid'] 
            ,name= str(userData['Name'])
            ,privilege= int(userData['Privilege'])
            ,user_id= str(userData['userid']))

        conn.set_user(uid= userData['uid'] ,name= userData['Name'],privilege= userData['Privilege'],user_id= str(userData['userid']))
        print(user)
        finger = Finger(
            uid=int(userData['uid']),
            fid=int(userData['Fid']),
            valid=int(userData['Valid']),
            template=template_bytes
        )
        print("Attempting to save user template")
        conn.save_user_template(user, [finger])
        print("User template saved successfully")

    except Exception as e:
        print("Process terminated: {}".format(e))

    finally:
        if conn:
            conn.disconnect()
            print("Disconnected from the device")
