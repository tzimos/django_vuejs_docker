"""
.. module:: backend.wait_db.py
   :synopsis: Script that waits database to start in order to launch
              the django server. It is used in docker-compose.

.. moduleauthor:: Panos Tzimos<tzimoss@gmail.com>
"""
import time

import psycopg2

connected = False
while connected:
    try:
        print('Test if database is conntected.\n')
        conn = psycopg2.connect(
            "db_name=db user=postgres password=random"
        )
        print('Database Connected.')
        connected = True
        conn.close()
    except:
        print('Retrying to connect to Database.')
        time.sleep(1)
