import threading
import queue
import requests

lester  = queue.Queue()

valid_proxies = []

with open("proxy_server.txt") as f:
    proxies = f.read().split("\n")
    for prox in proxies:
        lester.put(prox)
def check_proxies():
    global lester
    while not lester.empty():
        proxy = lester.get()
        try:
            res = requests.get("http://ipinfo.io/json",
                               proxies = {"http": proxy,
                                        "https": proxy
                                        }
                              )
        except:
            continue
        if res.status_code == 200:
            print(proxy)
            


            with open("valid_proxies_server.txt", "a") as file:
                file.write(proxy)
                file.write("\n")

for _ in range(10):
    threading.Thread(target=check_proxies).start()