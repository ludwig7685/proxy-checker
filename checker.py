import requests
from termcolor import colored
import threading

proxies_file = "proxies.txt"
checked_proxies = set()

def check_proxy(proxy):
    try:
        response = requests.get("https://www.google.com", proxies={"http": proxy, "https": proxy}, timeout=5)
        if response.status_code == 200:
            print(colored(f"{proxy} works", "green"))
            with open("yes.txt", "a") as f:
                if proxy not in checked_proxies:
                    f.write(proxy + "\n")
                    checked_proxies.add(proxy)
        else:
            print(colored(f"{proxy} doesn't work", "red"))
    except:
        print(colored(f"{proxy} doesn't work", "red"))

def main():
    with open(proxies_file, "r") as f:
        proxies = f.read().splitlines()

    threads = []
    num_threads = 20  # Number of threads to run simultaneously (adjust as needed)

    for proxy in proxies:
        t = threading.Thread(target=check_proxy, args=(proxy,))
        threads.append(t)
        t.start()

        if len(threads) >= num_threads:
            for thread in threads:
                thread.join()
            threads = []

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
