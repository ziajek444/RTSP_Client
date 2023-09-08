from multiprocessing import Process
from main import main_loop


def get_https_rstp_server_addr(_login, _passwd, _ip, _port):
    addr = f"https://{_login}:{_passwd}@{_ip}:{_port}/video"
    return addr


def run(_addr_list: list):
    processes = list()
    cam_idx = 1
    for addr in _addr_list:
        processes.append(Process(target=main_loop, args=(addr, f"CAM_{cam_idx}",)))
        cam_idx += 1
    for proc in processes:
        proc.start()
    for proc in processes:
        proc.join()


if __name__ == '__main__':
    print("Start RTSP Stream")

    rtsp_server_CAM_1 = get_https_rstp_server_addr("admin", "admin", "192.168.0.38", "4343")
    rtsp_server_CAM_2 = get_https_rstp_server_addr("admin", "admin", "192.168.0.120", "4343")
    rtsp_server_CAM_3 = get_https_rstp_server_addr("admin", "admin", "192.168.0.22", "4343")

    addr_list = [rtsp_server_CAM_1, rtsp_server_CAM_2, rtsp_server_CAM_3]
    run(addr_list)

    print("FIN")
