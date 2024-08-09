import requests
import json
import os
import time
from bs4 import BeautifulSoup
from requests.exceptions import RequestException

session = requests.session()
proxies = {
    'http': 'socks5h://localhost:9050',
    'https': 'socks5h://localhost:9050'
}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0',
}
session.proxies.update(proxies)
session.headers.update(headers)

def basicChecks():
    try:
        response = requests.get('https://check.torproject.org/api/ip', proxies=proxies).content
        response = json.loads(response)
        print(f"[+] Is Tor Running: {response['IsTor']}")
        print(f"[+] Current IP: {response['IP']}")
    except RequestException as e:
        print(f"[!] Error checking Tor status: {e}")
        response = requests.get('https://check.torproject.org/api/ip').content
        response = json.loads(response)
        print(f"[+] Is Tor Running: {response['IsTor']}")
        print(f"[+] Current IP: {response['IP']}")

        print("[!] Tor is not Running: Starting Tor!\n")
        os.system('systemctl start tor')
        time.sleep(3)
        basicChecks()

SEARCH_ENGINES = {
    "ahmia": "https://ahmia.fi",
    "submarine": "http://no6m4wzdexe3auiupv2zwif7rm6qwxcyhslkcnzisxgeiw6pvjsgafad.onion/",
    "evo": "http://wbr4bzzxbeidc6dwcqgwr3b6jl7ewtykooddsc5ztev3t3otnl45khyd.onion/",
    # "notevil": "http://notevilmtxf25uw7tskqxj6njlpebyrmlrerfv5hc4tuq7c7hilbyiqd.onion/",
    "onionengine": "https://onionengine.com",
    "dude": "http://thedude75pphneo4auknyvspskdmcj4xicbsnkvqgwhb4sfnmubkl5qd.onion",
    "vormweb": "https://vormweb.de/en",
    "gdark": "http://zb2jtkhnbvhkya3d46twv3g7lkobi4s62tjffqmafjibixk6pmq75did.onion"
}

def ahmia(query, isLimited):
    output = []
    try:
        url = f"{SEARCH_ENGINES['ahmia']}/search/?query={query}"
        response = session.get(url).content
        soup = BeautifulSoup(response, 'html.parser')
        urlList = soup.find_all("cite")
        for link in urlList:
            output.append(link.text)
        print(f"\n[+] Ahmia Done!")
    except RequestException as e:
        print(f"[!] Ahmia: Error occurred: {e}")
    return output

def submarine(query, isLimited):
    output = []
    try:
        if not isLimited:
            url = f"{SEARCH_ENGINES['submarine']}search.php?term={query}"
            response = session.get(url).content
            soup = BeautifulSoup(response, 'html.parser')
            soup = soup.find_all('div', {"class": "col-md-8"})
            for i in soup:
                soup = i.find_all('a')
            noOfPages = int(soup[-1].text)
            for i in range(1, noOfPages + 1):
                url = f"{SEARCH_ENGINES['submarine']}search.php?term={query}&page={i}"
                response = session.get(url).content
                soup = BeautifulSoup(response, 'html.parser')
                soup = soup.find_all('a', {"class": "text-custom"})
                for link in soup:
                    output.append(link.text)
            print(f"\n[+] Submarine Done!")
        else:
            url = f"{SEARCH_ENGINES['submarine']}search.php?term={query}"
            response = session.get(url).content
            soup = BeautifulSoup(response, 'html.parser')
            soup = soup.find_all('a', {"class": "text-custom"})
            for link in soup:
                output.append(link.text)
            print(f"\n[+] Submarine Done!")
    except RequestException as e:
        print(f"[!] Submarine: Error occurred: {e}")
    return output

def evo(query, isLimited):
    output = []
    try:
        if not isLimited:
            url = f"{SEARCH_ENGINES['evo']}/evo/?q={query}"
            response = session.get(url).content
            soup = BeautifulSoup(response, 'html.parser')
            soup = soup.find('div', {"class": "pagination"})
            soup = soup.find_all('button', {"class": "navbutton submit"})
            noOfPages = int(soup[-1].text)
            for i in range(1, noOfPages + 1):
                url = f"{SEARCH_ENGINES['evo']}/evo/?q={query}&thumbs=&page={i}"
                response = session.get(url).content
                soup = BeautifulSoup(response, 'html.parser')
                soup = soup.findAll("div", {"class": "webUrl"})
                for i in soup:
                    output.append(i.text)
            print(f"\n[+] Evo Done!")
        else:
            url = f"{SEARCH_ENGINES['evo']}/evo/?q={query}&thumbs="
            response = session.get(url).content
            soup = BeautifulSoup(response, 'html.parser')
            soup = soup.findAll("div", {"class": "webUrl"})
            for i in soup:
                output.append(i.text)
            print(f"\n[+] Evo Done!")
    except RequestException as e:
        print(f"[!] Evo: Error occurred: {e}")
    return output

def onionengine(query, isLimited):
    output = []
    try:
        url = f"{SEARCH_ENGINES['onionengine']}/search.php?search={query}&submit=Search&rt="
        response = session.get(url).content
        soup = BeautifulSoup(response, 'html.parser')
        soup = soup.find("div", {"style": "text-align:center;"})
        soup = soup.findAll('a')
        noOfPages = int(soup[-2].text)
        for i in range(2, noOfPages):
            url = f"{SEARCH_ENGINES['onionengine']}/search.php?search={query}&submit=Search&page={i}"
            response = session.get(url).content
            soup = BeautifulSoup(response, 'html.parser')
            soup = soup.findAll('table')[1]
            soup = soup.findAll("a")
            for i in range(1, len(soup) + 1, 4):
                output.append(soup[i].text)
        print(f"[+] OnionEngine Done!")
    except RequestException as e:
        print(f"[!] OnionEngine: Error occurred: {e}")
    return output

def dude(query, isLimited):
    output = []
    try:
        url = f"{SEARCH_ENGINES['dude']}/?query={query}"
        response = session.get(url).content
        soup = BeautifulSoup(response, 'html.parser')
        soup = soup.find_all('div', {"class": "result"})
        for link in soup:
            result = link.find('a')['href']
            output.append(result)
        print("[+] Dude Done!")
    except RequestException as e:
        print(f"[!] Dude: Error occurred: {e}")
    return output

def vormweb(query, isLimited):
    output = []
    try:
        url = f"{SEARCH_ENGINES['vormweb']}/search?q={query}"
        response = session.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        result = soup.find_all("div", class_="query-box")
        for results in result:
            link = results.find("a").get("href")
            output.append(link)
        print(f"[+] Vormweb Done!")
    except RequestException as e:
        print(f"[!] Vormweb: Error occurred: {e}")
    return output

def gdark(query, isLimited):
    output = []
    try:
        if not isLimited:
            initial_url = f"{SEARCH_ENGINES['gdark']}/gdark/search.php?query={query}&search=1"
            response = session.get(initial_url).content
            soup = BeautifulSoup(response, 'html.parser')
            noOfResults = soup.find("div", id="result_report").text.split(" ")[1]
            url = f"{SEARCH_ENGINES['gdark']}/gdark/search.php?query={query}&start=0&search=1&results={noOfResults}"
            response = session.get(url).content
            soup = BeautifulSoup(response, 'html.parser')
            results = soup.find_all("div", {"class": "url"})
            for link in results:
                url = link.text.split(" ")[0]
                if len(url) > 50:
                    output.append(url)
            print('[+] GDark Done!')
        else:
            url = f"{SEARCH_ENGINES['gdark']}/gdark/search.php?query={query}&start=0&search=1"
            response = session.get(url).content
            soup = BeautifulSoup(response, 'html.parser')
            results = soup.find_all("div", {"class": "url"})
            for link in results:
                url = link.text.split(" ")[0]
                if len(url) > 50:
                    output.append(url)
            print('[+] GDark Done!')
    except RequestException as e:
        print(f"[!] GDark: Error occurred: {e}")
    return output
