from multiprocessing import Process
import os
from req_neverLostConn import never_lost_conn
# never_lost_conn(_rtsp_server: str, _source_name: str, _preview=False)
rtsp_server_PRO = 'https://admin:admin@192.168.0.38:4343/video'
rtsp_server_OLD = 'https://admin:admin@192.168.0.120:4343/video'

if __name__ == '__main__':
    print("Start RTSP Stream")
    p1 = Process(target=never_lost_conn, args=(rtsp_server_PRO, "PRO",))
    p2 = Process(target=never_lost_conn, args=(rtsp_server_OLD, "OLD",))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    print("FIN")
