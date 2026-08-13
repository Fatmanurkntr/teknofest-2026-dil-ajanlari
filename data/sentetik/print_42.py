import json
with open('data/sentetik/evraklar.jsonl', 'r', encoding='utf-8') as f:
    records = [json.loads(line) for line in f if line.strip()]

new_records = [r for r in records if r['id'] >= 'SENT-0162']

for i, r in enumerate(new_records, 1):
    print(f"=== KAYIT {i} | ID: {r['id']} | Tür: {r['evrak_turu_dogru']} ===")
    print(f"Eksik: {r['eksik_alan_var_mi']} | Zorluk: {r['zorluk']}")
    print(f"Metin:\n{r['metin']}")
    print('-' * 40 + '\n')
