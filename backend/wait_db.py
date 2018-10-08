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
