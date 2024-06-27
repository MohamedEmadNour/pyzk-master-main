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

ip = '192.168.1.201'
conn = None
zk = ZK(ip, port=4370, password=1)
try:
    conn = zk.connect()
    print("Connected to the device")
    conn.delete_user(uid=8,user_id='18822')
except Exception as e:
    print("Process terminated: {}".format(e))

finally:
    if conn:
        conn.disconnect()
        print("Disconnected from the device")       