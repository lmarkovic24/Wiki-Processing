import json

def load_from_file():
    r1 = {}
    r2 = {}
    try:
        f = open("./backups/countSmall.json","r",encoding="utf-8")
        conts = f.read()
        r1 = json.loads(conts)
        f.close()
    except Exception as e:
        r1 = {}
    try:
        f = open("./backups/uniqueSmall.json","r",encoding="utf-8")
        conts = f.read()
        r2 = json.loads(conts)
        f.close()

        for key in r2.keys():
            r2[key] = set(r2[key])

    except Exception as e:
        r2 = {}
    
    return r1,r2

counts, unique = load_from_file()

f = open("output.txt","w",encoding="utf-8")

for key in counts.keys():
    f.write(f"{key}|{len(unique[key])}|{counts[key]}\n")
