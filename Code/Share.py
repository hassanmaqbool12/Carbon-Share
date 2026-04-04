import time
import threading
import server
import data
import directShare


class App:
    def __init__(self):
        self.direct = directShare.App()

    def start(self):
        threading.Thread(target=self.monitor_ip, daemon=True).start()
        threading.Thread(target=server.init_server, daemon=True).start()
        data.show_success_log(f"Running on: {data.url}")
        self.direct.run()

    def monitor_ip(self):
        while True:
            try:
                new_url = data.check()
                if data.previousIP != new_url:
                    data.previousIP = new_url
                    data.url = new_url
                    data.url = new_url
                    self.direct.updateIP(new_url)
            except Exception as e:
                data.show_error_log(f"IP Monitor Error {e}")
            time.sleep(2)


if __name__ == "__main__":
    
    app = App()
    app.start()
