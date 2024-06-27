# -*- coding: utf-8 -*-
import os
import sys
from datetime import datetime

CWD = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.dirname(CWD)
sys.path.append(ROOT_DIR)

from zk import ZK

def synctime() :
    conn = None
    zk = ZK('10.200.24.1', port=4370 , password=1)
    try:
        conn = zk.connect()
        print ("Syncing time...")
        isconnect =  conn.checkMachineConnection()
        print(isconnect)
    except Exception as e:
        print ("Process terminate : {}".format(e))
    finally:
        if conn:
            conn.disconnect()
