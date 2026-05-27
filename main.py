import requests
import re
import json
import time
import random

API_URL = "https://sr.wikipedia.org/w/api.php"

CYRILLIC_RE = re.compile(r'[\u0400-\u04FF]')

headers = {
    "User-Agent": "SerbianCyrillicWordCollector/1.0",
    "Api-User-Agent" : "lmarkovic24@rg.edu.rs"
}

params = {
    "action": "query",
    "format": "json",
    "generator": "random",
    "grnnamespace": 0,     # normal articles only
    "prop": "extracts",
    "explaintext": 1,
    "grnlimit": 1 # page count
}

counts = {}
unique_occurrences = {}
def save_to_file():
    with open("count.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(counts,indent=4, ensure_ascii=False))
    with open("unique.json", "w", encoding="utf-8") as f:
        for key in unique_occurrences.keys():
            unique_occurrences[key] = list(unique_occurrences[key])
        f.write(json.dumps(unique_occurrences,indent=4, ensure_ascii=False))
        for key in unique_occurrences.keys():
            unique_occurrences[key] = set(unique_occurrences[key])

def load_from_file():
    r1 = {}
    r2 = {}
    try:
        f = open("count.json","r",encoding="utf-8")
        conts = f.read()
        r1 = json.loads(conts)
        f.close()
    except Exception as e:
        r1 = {}
    try:
        f = open("unique.json","r",encoding="utf-8")
        conts = f.read()
        r2 = json.loads(conts)
        f.close()

        for key in r2.keys():
            r2[key] = set(r2[key])

    except Exception as e:
        r2 = {}
    
    return r1,r2

def process_page():
    response = requests.get(API_URL, params=params, headers=headers)
    data = response.json()

    pages = data["query"]["pages"]
    pid = 0
    for page_id, page in pages.items():
        title = page["title"]
        text = page.get("extract", "")
        pid = page_id

        print("TITLE:", title)
        print()
    
    for word in text.split(" "):

        
        chars = "\n\r ,.;=+?!()"
        
        for c in chars:
            word = word.replace(c,"")
        
        if CYRILLIC_RE.match(word):
            if word in counts.keys():
                counts[word]+=1
            else:
                counts[word] = 1

            if word in unique_occurrences.keys():
                unique_occurrences[word].add(pid)
            else:
                unique_occurrences[word] = set()
                unique_occurrences[word].add(pid)
    

    


counts,unique_occurrences = load_from_file()

num_its = 5
its_done = 30
while True:
    for _ in range(num_its):
        for i in range(5):
            process_page()
            time.sleep(0.5)
            its_done+=1
        save_to_file()

        time.sleep(2)
    val = random.randint(5,15)
    for i in range(val,0):
        print(f"Time left: {i} | completed {num_its}")
        time.sleep(i)
    