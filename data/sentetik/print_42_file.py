import json
with open('data/sentetik/evraklar.jsonl', 'r', encoding='utf-8') as f:
    records = [json.loads(line) for line in f if line.strip()]

new_records = [r for r in records if r['id'] >= 'SENT-0162']

with open('42_records.txt', 'w', encoding='utf-8') as out:
    for i, r in enumerate(new_records, 1):
        out.write(f"=== KAYIT {i} | ID: {r['id']} | Tür: {r['evrak_turu_dogru']} ===\n")
        out.write(f"Eksik: {r['eksik_alan_var_mi']} | Zorluk: {r['zorluk']}\n")
        out.write(f"Metin:\n{r['metin']}\n")
        out.write('-' * 40 + '\n\n')
