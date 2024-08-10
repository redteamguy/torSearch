import requests
from bs4 import BeautifulSoup
from scrappers import *
# from scrappers import *
from banner import *
from support_modules import validator
import importlib

def menu():
    print(f"\n{banner}")
    print("\n\n")
    basicChecks()
    print()
    print("[+] Available Options:- \n1. Quick Mode\n2. Deep Search Mode\n3. Custom Queries")

result = []
finalOutput = []

def parse(urlList):
    for listSection in urlList:
        for link in listSection:
            finalOutput.append(link)

search_functions = {
    "ahmia": ahmia,
    # "notevil": notevil,
    "evo": evo,
    "dude": dude,
    "vormweb": vormweb,
    "gdark": gdark,
}

def display(urlList):
    for link in set(urlList):
        print(validator(link))

def searchIt(query, isLimited=True):
    for functionName, func in search_functions.items():
        print(f"[+] Searching {functionName}")
        try:
            search_results = func(query, isLimited)
            result.append(search_results)
        except requests.exceptions.RequestException as e:
            print(f"[!] Error occurred with {functionName}: {e}")
    return result

def customSearch(query, limit=False):
    engine = input("[+] Enter Search Engine to search: ")
    if engine in search_functions:
        try:
            search_results = search_functions[engine](query, limit)
            result.append(search_results)
        except requests.exceptions.RequestException as e:
            print(f"[!] Error occurred with {engine}: {e}")
    else:
        print(f"[!] No such search engine: {engine}")
    parse(result)
    display(finalOutput)

def saveIt(query):
    try:
        with open(f"results/{query}.txt", 'w+') as f:
            for i in set(finalOutput):
                f.write(validator(i) + "\n")
        print(f"[+] {len(set(finalOutput))} Unique URLs saved as results/{query}.txt")
    except IOError as e:
        print(f"[!] Error saving file: {e}")

def deepMode(query):
    print("\n[+] Searching the Depths of the Dark Web. This will take some time!")
    try:
        urlList = searchIt(query, False)
        parse(urlList)
        saveIt(query)
    except Exception as e:
        print(f"[!] Error in deepMode: {e}")

def quickMode(query):
    saveChoice = input("[+] Do you want to save the results[Y/n]: ")
    try:
        urlList = searchIt(query)
        parse(urlList)
        if saveChoice.lower() in ['y', '']:
            saveIt(query)
        else:
            display(urlList)
    except Exception as e:
        print(f"[!] Error in quickMode: {e}")

def entry():
    menu()
    try:
        choice = int(input("[+] Enter Your Choice: "))
        query = input("[+] Enter Your Search Term: ")

        if choice == 1:
            quickMode(query)
        elif choice == 2:
            deepMode(query)
        elif choice == 3:
            customSearch(query, "2")
        else:
            print("[!] Invalid Option Selected!")
    except ValueError as e:
        print(f"[!] Invalid input: {e}")

entry()
