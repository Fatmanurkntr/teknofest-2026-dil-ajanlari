import json
import random
with open('data/sentetik/evraklar.jsonl', 'r', encoding='utf-8') as f:
    records = [json.loads(line) for line in f if line.strip()]

new_records = [r for r in records if r['id'] >= 'SENT-0162']
random.seed(123)
sample = random.sample(new_records, 5)

for i, r in enumerate(sample, 1):
    print(f"=== ÖRNEK {i} ===")
    print(f"ID: {r['id']}")
    print(f"Tür: {r['evrak_turu_dogru']}")
    print(f"Birim: {r['hedef_birim_dogru']}")
    print(f"Zorluk: {r['zorluk']}")
    print(f"Eksik Alan Var Mı: {r['eksik_alan_var_mi']}")
    print(f"Metin:\n{r['metin']}")
    print("----------------------\n")
