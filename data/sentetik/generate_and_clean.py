import json
import random
from pathlib import Path

KAYNAK = Path("data/sentetik/evraklar.jsonl")

IDS_TO_DELETE = {f"SENT-{i:04d}" for i in range(118, 158)}
IDS_TO_DELETE.add("SENT-0159")
IDS_TO_DELETE.add("SENT-0160")

REPLACEMENTS = {
    "ORENLI ILCE KAYMAKAMLIĞI": "ÖRENLİ İLÇE KAYMAKAMLIĞI",
    "ILCE SAGLIK MÜDÜRLÜĞÜNE": "İLÇE SAĞLIK MÜDÜRLÜĞÜNE",
    "ILCE MILLI EGITIM MÜDÜRLÜĞÜNE": "İLÇE MİLLÎ EĞİTİM MÜDÜRLÜĞÜNE",
    "ILCE EMNİYET MÜDÜRLÜĞÜNE": "İLÇE EMNİYET MÜDÜRLÜĞÜNE",
    "ORENLI TAPU MÜDÜRLÜĞÜNE": "ÖRENLİ TAPU MÜDÜRLÜĞÜNE",
    "ORENLI MAL MÜDÜRLÜĞÜNE": "ÖRENLİ MAL MÜDÜRLÜĞÜNE",
    "ORENLI TARIM VE ORMAN MÜDÜRLÜĞÜNE": "ÖRENLİ TARIM VE ORMAN MÜDÜRLÜĞÜNE",
    "ORENLI SYDV BAŞKANLIĞINA": "ÖRENLİ SYDV BAŞKANLIĞINA"
}

def clean_record(record):
    if record["id"] in {f"SENT-{i:04d}" for i in range(111, 118)}:
        metin = record.get("metin", "")
        for old, new in REPLACEMENTS.items():
            metin = metin.replace(old, new)
        record["metin"] = metin
    return record

random.seed(101)
names = ["Ahmet Yılmaz", "Ayşe Kaya", "Mehmet Demir", "Fatma Çelik", "Mustafa Şahin", "Zeynep Yıldız", "Ali Özdemir", "Hatice Arslan", "Hasan Doğan", "Emine Kılıç", "Burak Can", "Seda Nur", "Kemal Sunal", "Cem Karaca", "Zeliha Tunç", "Orhan Veli"]
addresses = ["Cumhuriyet Mah. Atatürk Cad. No: 12 Örenli", "Yeni Mah. İnönü Cad. No: 34 Örenli", "Merkez Mah. Lise Cad. No: 56 Örenli", "Fatih Mah. İstiklal Cad. No: 78 Örenli", "Yeşil Mah. Park Cad. No: 90 Örenli", "Kavaklı Mah. Söğüt Sok. No: 11 Örenli"]
tcs = ["12345678901", "23456789012", "34567890123", "45678901234", "56789012345", "67890123456", "78901234567"]
dates = ["01.08.2026", "05.08.2026", "10.08.2026", "15.08.2026", "20.08.2026", "25.08.2026"]
companies = ["Yıldız İnşaat Ltd. Şti.", "Kaya Kardeşler A.Ş.", "Demiray Lojistik", "Özdemir Gıda Pazarlama", "Şahin Temizlik Hizmetleri", "Akıncı Teknoloji"]

ihale_konulari = [
    ("Okul Onarımı İhalesi İtirazı", "İlçemizdeki 3 okulun çatı onarımı ihalesinde usulsüzlük yapıldığı iddiası."),
    ("Araç Kiralama İhalesi Sonucuna İtiraz", "Kaymakamlık makam araçları kiralama ihalesinde en düşük teklifimizin haksız yere geçersiz sayılmasına itiraz."),
    ("Kömür Alımı İhalesi Şartnamesine İtiraz", "SYDV kömür alımı ihalesinde şartnamenin rekabeti engelleyici maddeler içerdiği iddiası."),
    ("Yemek Hizmeti İhalesi Kararına İtiraz", "Taşımalı eğitim yemek hizmeti ihalesinde komisyon kararına ve teknik puanlamaya itiraz edilmesi.")
]
sosyal_yardim_konulari = [
    ("Gıda Yardımı Talebi", "Aylık gelirimin yetersizliği nedeniyle aileme kuru gıda yardımı yapılmasını talep ediyorum."),
    ("Yakacak Yardımı Başvurusu", "Kış aylarında ısınma ihtiyacımızı karşılayamadığımız için kömür yardımı talep ediyorum."),
    ("Eğitim Bursu ve Materyal Yardımı", "Üniversitede okuyan 2 çocuğumun eğitim masrafları için maddi destek talep ediyorum."),
    ("Engelli Yakını Bakım Yardımı", "Yüzde 80 engelli babamın bakım masraflarına destek olunması talebi."),
    ("Barınma Yardımı Talebi", "Evimizin çatısının çökmesi nedeniyle acil onarım yardımı talep ediyorum.")
]
tapu_konulari = [
    ("Sınır Tecavüzü Şikayeti", "Komşu parsel (Ada 120 Parsel 5) sahibinin tarlama sınır ihlali yapması şikayeti."),
    ("Tapu Kaydında İsim Düzeltme", "Tapu senedimde adımın yanlış yazılmasından dolayı tashihat yapılması talebi."),
    ("Miras İntikal İşlemleri Bilgi Talebi", "Vefat eden babamdan kalan arazilerin miras intikali için yapılması gerekenler."),
    ("Kadastro Tespitine İtiraz", "Mahallemizde yapılan yeni kadastro ölçümlerinde arazimin 20 metrekare eksik yazılmasına itiraz."),
    ("İzinsiz Yapı ve Müdahalenin Men'i", "Tarlama izinsiz olarak baraka inşa eden şahsın müdahalesinin men edilmesi talebi.")
]

new_records = []
current_id = 162

def generate_records(count, type_name, target_unit, konulari_list, is_company=False):
    global current_id
    for _ in range(count):
        if is_company:
            name = random.choice(companies) + " adına " + random.choice(names)
        else:
            name = random.choice(names)
            
        tc = random.choice(tcs)
        addr = random.choice(addresses)
        date = random.choice(dates)
        konu, detay = random.choice(konulari_list)
        
        zorluk = random.choices(["kolay", "orta", "zor"], weights=[0.6, 0.2, 0.2])[0]
        eksik = random.random() < 0.2
        
        if zorluk == "zor":
            if type_name == "ihale_itirazi":
                metin = f"KAYMAKAMLIĞA\n\nFirmamız {konu} ile ilgili mağdur edilmiştir. {detay} İhalenin iptalini istiyoruz.\n\nİmza: {name}"
            else:
                metin = f"KAYMAKAMLIĞA\n\n{konu} hakkında sorunum var. {detay} Gereğinin yapılmasını istiyorum.\n\n{name}"
        else:
            if type_name == "sosyal_yardim_basvuru":
                metin = f"ÖRENLİ İLÇE KAYMAKAMLIĞINA\n(Sosyal Yardımlaşma ve Dayanışma Vakfı Başkanlığı)\n\nBAŞVURAN: {name}\nAdres: {addr}\nT.C. Kimlik No: {tc}\n\nKONU: {konu}\n\nAÇIKLAMALAR:\n1. {detay}\n2. Gerekli incelemelerin yapılarak tarafıma yardım bağlanmasını arz ederim.\n\nTarih: {date}\nİmza: {name}"
            else:
                metin = f"ÖRENLİ İLÇE KAYMAKAMLIĞINA\n\nBAŞVURAN: {name}\nAdres: {addr}\nKimlik/Vergi No: {tc}\n\nKONU: {konu}\n\nAÇIKLAMALAR:\n1. {detay}\n2. Konunun incelenerek tarafıma bilgi verilmesini ve mağduriyetimin giderilmesini talep ediyorum.\n3. Gereğini saygılarımla arz ederim.\n\nTarih: {date}\nİmza: {name}"
            
            if eksik:
                metin = metin.replace(f"Tarih: {date}\n", "")
                date = None
                
        rek = {
            "id": f"SENT-{current_id:04d}",
            "evrak_turu_dogru": type_name,
            "hedef_birim_dogru": target_unit,
            "uretim_yontemi": "serbest_llm",
            "eksik_alan_var_mi": eksik or zorluk == "zor",
            "zorluk": zorluk,
            "metin": metin,
            "beklenen_alanlar": {
                "gonderen_adi": name,
                "tarih": date if zorluk != "zor" else None,
                "konu": konu,
                "talep_metni": detay
            }
        }
        new_records.append(rek)
        current_id += 1

generate_records(16, "ihale_itirazi", "yazi_isleri", ihale_konulari, is_company=True)
generate_records(12, "sosyal_yardim_basvuru", "sydv", sosyal_yardim_konulari, is_company=False)
generate_records(14, "tapu_kadastro_basvuru", "tapu", tapu_konulari, is_company=False)

def main():
    with open(KAYNAK, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    final_lines = []
    deleted_count = 0
    fixed_count = 0
    
    for line in lines:
        if not line.strip():
            continue
        record = json.loads(line)
        record_id = record.get("id")
        
        if record_id in IDS_TO_DELETE:
            deleted_count += 1
            continue
            
        record = clean_record(record)
        if record_id in {f"SENT-{i:04d}" for i in range(111, 118)}:
            fixed_count += 1
            
        # Clean up any leftover keys from previous steps (like _encoding_notu)
        if "_encoding_notu" in record:
            del record["_encoding_notu"]
            
        final_lines.append(json.dumps(record, ensure_ascii=False) + "\n")
        
    # Append new records
    for rek in new_records:
        final_lines.append(json.dumps(rek, ensure_ascii=False) + "\n")
        
    # Write everything back securely
    with open(KAYNAK, 'w', encoding='utf-8') as f:
        f.writelines(final_lines)
        
    print(f"Fixed ASCII records: {fixed_count} (should be 7)")
    print(f"Deleted records: {deleted_count} (should be 42)")
    print(f"Appended records: {len(new_records)} (should be 42)")

if __name__ == '__main__':
    main()
