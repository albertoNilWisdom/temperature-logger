import sys
import datetime
import psutil
import mysql.connector
import os

db = mysql.connector.connect(host='192.168.0.23',user='ted',passwd='<PW>',db='homelab_system_logging')
cursor = db.cursor(buffered=True)

def main():
    if not hasattr(psutil, "sensors_temperatures"):
        sys.exit("platform not supported")
    temps = psutil.sensors_temperatures()
    if not temps:
        sys.exit("can't read any temperature")
    for name, entries in temps.items():
        for entry in entries:
            values = "'"+os.uname()[1]+"','"+str(datetime.datetime.now())+"','"+"%-s', %s"%(entry.label or name, entry.current)
            sql = "INSERT INTO temperatures(computer_name,datetime_varchar,device_ID,temperature_C)VALUES("+str(values)+")"
           # print(values)
            cursor.execute(sql)
            db.commit()


if __name__ == '__main__':
    main()