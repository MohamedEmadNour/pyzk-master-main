# -*- coding: utf-8 -*-
import os
import sys

CWD = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.dirname(CWD)
sys.path.append(ROOT_DIR)

from zk import ZK


conn = None
zk = ZK('192.168.1.201', port=4370 , password=1)
try:
    conn = zk.connect()
    choices = input('Are you sure want to delete all data? [Y/N]: ')
    if choices == 'Y' or choices == 'y':
        conn.clear_data()
        print ("Clear all data...")
    else:
        print ("Clear all data canceled !")
except Exception as e:
    print ("Process terminate : {}".format(e))
finally:
    if conn:
        conn.disconnect()
