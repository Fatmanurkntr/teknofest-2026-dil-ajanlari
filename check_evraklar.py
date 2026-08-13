import json

ids_to_check = [
    'SENT-0179', 'SENT-0180', 'SENT-0184', 'SENT-0185', 'SENT-0189',
    'SENT-0190', 'SENT-0191', 'SENT-0193', 'SENT-0195', 'SENT-0198', 'SENT-0201'
]

with open('data/sentetik/evraklar.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        if not line.strip(): continue
        data = json.loads(line)
        if data['id'] in ids_to_check:
            print(f"ID: {data['id']}")
            print(f"METİN:\n{data['metin']}\n")
            print(f"BEKLENEN ALANLAR: {data['beklenen_alanlar']}\n")
            print('-'*40)
