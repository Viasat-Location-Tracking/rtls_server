from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
import psycopg2
import json
import time
from datetime import datetime, timezone

db_conn = None
db_curr = None

class ReadUDP(DatagramProtocol):
    def datagramReceived(self, data, addr):
 #       print("received {!r} from {}".format(data, addr))
        insertInTable(data)

def configurePGConn():
    global db_conn, db_curr
    try:
        db_conn = psycopg2.connect(
            dbname = "QPEinfo",
            user = "demouser",
            host = "127.0.0.1",
            password = "PolyGAIT",
            connect_timeout = 3
        )
        db_curr = db_conn.cursor()
    except (Exception, psycopg2.Error) as err:
        print("\ndb connection error:", err)
        quit()

def insertInTable(json_data):
    json_tbl = json.loads(json_data)
    try:
        db_curr.execute("""INSERT INTO webapp_datapoint (tag_id, timestamp, zone, x_pos, y_pos, button_pushed) VALUES (%s, %s, %s, %s, %s, %s);""", 
        (json_tbl["tagId"], datetime.now(timezone.utc), json_tbl["kalmanPositionZoneNames"], json_tbl["kalmanPositionX"], json_tbl["kalmanPositionY"], json_tbl["button1State"] == "pushed"))
        db_conn.commit()
    except (Exception, psycopg2.Error) as err:
        print("\nExecute db error:", err)
        db_conn.rollback()

def main():
    configurePGConn()
    reactor.listenUDP(5000, ReadUDP())
    reactor.run()

if __name__ == '__main__':
    main()