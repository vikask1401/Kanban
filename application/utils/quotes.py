import json

f = open('application/data/quotes.json', encoding="utf8")
quotes = json.load(f)
quotelist = []
for i in quotes:
    if i["Category"] == "success" and "Cosmic" not in i["Quote"].split(" "):
        if len(i["Quote"]) <= 60:
            quotelist.append(i["Quote"])
f.close()