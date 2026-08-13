import json
import random
from pathlib import Path

KAYNAK = Path("data/sentetik/evraklar.jsonl")

# 42 Generic Names
names = [
    "Ahmet Yılmaz", "Ayşe Kaya", "Mehmet Demir", "Fatma Çelik", "Mustafa Şahin",
    "Zeynep Yıldız", "Ali Özdemir", "Hatice Arslan", "Hasan Doğan", "Emine Kılıç",
    "Burak Can", "Seda Çetin", "Zeliha Tunç", "Orhan Efe", "Hüseyin Aksoy",
    "Elif Polat", "Osman Kurt", "Merve Koç", "Halil Gür", "Gül Erdem",
    "İbrahim Şen", "Büşra Çoban", "Serkan Bozkurt", "Derya Taş", "Gökhan Avcı",
    "Cansu Bulut", "Ercan Tekin", "Dilek Kaplan", "Murat Ateş", "Ebru Uysal",
    "Yusuf Güler", "Yasemin Keskin", "Turan Gök", "Pelin Sönmez", "Adem Baş",
    "Sevim Işık", "Kenan Turan", "Gülşen Çam", "Rıza Ak", "Zehra Biçer",
    "Sinan Coşkun", "Tuğçe Dağ"
]

# 42 Distinct Addresses
mahalleler = ["Cumhuriyet", "Yeni", "Merkez", "Fatih", "Yeşil", "Kavaklı", "Güneş", "Yıldız", "Akasya", "Çamlık", "İnönü", "Atatürk", "Barış", "Zafer"]
sokaklar = ["Gül", "Lale", "Menekşe", "Papatya", "Söğüt", "Çınar", "Meşe", "Karanfil", "Sümbül", "Orkide"]
addresses = []
for i in range(42):
    addresses.append(f"{mahalleler[i % len(mahalleler)]} Mah. {sokaklar[i % len(sokaklar)]} Sok. No: {i+1} Örenli")

# 42 Distinct TC Numbers
tcs = [f"{10000000000 + i*1379:011d}" for i in range(42)]

# 16 Distinct Companies
companies = [
    "Yıldız İnşaat Ltd. Şti.", "Kaya Kardeşler A.Ş.", "Demiray Lojistik", "Özdemir Gıda Pazarlama",
    "Şahin Temizlik Hizmetleri", "Akıncı Teknoloji", "Gürbüz Kırtasiye", "Erden Bilişim",
    "Karaca Taşımacılık", "Polat Madencilik", "Tekin Güvenlik A.Ş.", "Koç Yapı",
    "Çetin Catering", "Aslan Turizm", "Güler Otomotiv", "Başaran Medikal"
]

# Closing Sentences
closings = [
    "Gereğini saygılarımla arz ederim.",
    "Gereğinin yapılmasını arz ederim.",
    "Gereğinin yapılmasını talep ederim.",
    "Konunun incelenerek tarafıma bilgi verilmesini talep ediyorum.",
    "Mağduriyetimin giderilmesi hususunda gereğini arz ederim.",
    "Gereken işlemlerin yapılmasını saygıyla arz ederim.",
    "Talebimin değerlendirilmesini arz ederim.",
    "Gereğinin ifasını arz ederim.",
    "Durumu bilgilerinize arz ederim.",
    "İlgili makamca gereğinin yapılmasını rica ederim.",
    "Konunun tetkik edilerek çözüme kavuşturulmasını arz ederim.",
    "Yardımlarınızı bekler, saygılar sunarım.",
    "İşlemlerin hızlandırılmasını talep ediyorum.",
    "Şikayetimin dikkate alınmasını arz ederim.",
    "Tarafıma yazılı olarak bilgi verilmesini arz ederim."
]

ihale_konulari = [
    ("Okul Onarımı İhalesi İtirazı", "İlçemizdeki {okul} onarımı ihalesinde şartnameye uyulmadığı tespit edilmiştir."),
    ("Araç Kiralama İhalesi Sonucuna İtiraz", "Kaymakamlık makam araçları kiralama ihalesinde en düşük teklifimizin teknik bahane ile geçersiz sayılmasına itiraz ediyoruz."),
    ("Kömür Alımı İhalesi Şartnamesine İtiraz", "SYDV kömür alımı ihalesinde şartnamenin 5. maddesinin rekabeti engelleyici olduğu görülmüştür."),
    ("Yemek Hizmeti İhalesi Kararına İtiraz", "Taşımalı eğitim yemek hizmeti ihalesinde komisyon kararının ve teknik puanlamanın yeniden değerlendirilmesi talebi.")
]

okullar = ["Atatürk İlkokulu", "Cumhuriyet Ortaokulu", "Fatih Lisesi", "Örenli Mesleki ve Teknik Anadolu Lisesi"]

sosyal_yardim_konulari = [
    ("Gıda Yardımı Talebi", "Aylık gelirimin asgari ücretin altında kalması nedeniyle {ay} ayı için aileme kuru gıda yardımı yapılmasını talep ediyorum."),
    ("Yakacak Yardımı Başvurusu", "Kış aylarında ısınma ihtiyacımızı karşılayamadığımızdan dolayı bu kış için kömür yardımı talep ediyorum."),
    ("Eğitim Bursu ve Materyal Yardımı", "Üniversitede okuyan {sayi} çocuğumun eğitim masrafları ve kırtasiye giderleri için maddi destek talep ediyorum."),
    ("Engelli Yakını Bakım Yardımı", "Yüzde 80 bedensel engelli eşimin günlük bakım masraflarına destek olunması talebidir."),
    ("Barınma Yardımı Talebi", "Geçtiğimiz fırtınada evimizin çatısının hasar görmesi nedeniyle acil barınma/onarım yardımı talep ediyorum.")
]

tapu_konulari = [
    ("Sınır Tecavüzü Şikayeti", "Komşu parsel olan Ada {ada} Parsel {parsel} sahibinin tarlama yaklaşık 5 metre sınır ihlali yapması şikayetidir."),
    ("Tapu Kaydında İsim Düzeltme", "Tapu senedimde adımın hatalı yazılmasından dolayı nüfus kayıtlarına uygun olarak tashihat yapılması talebi."),
    ("Miras İntikal İşlemleri Bilgi Talebi", "Vefat eden annemden kalan tarım arazilerinin miras intikali için yapılması gereken işlemlerin bildirilmesi."),
    ("Kadastro Tespitine İtiraz", "Mahallemizde yapılan son kadastro ölçümlerinde Ada {ada} Parsel {parsel} numaralı arazimin 20 metrekare eksik yazılmasına itiraz ediyorum."),
    ("İzinsiz Yapı ve Müdahalenin Men'i", "Tarlama izinsiz olarak baraka inşa eden ve mahsullerime zarar veren şahsın müdahalesinin men edilmesi talebidir.")
]

def generate_records():
    records = []
    current_id = 162
    
    # Shuffle base data to ensure mix
    random.seed(42)
    indices = list(range(42))
    random.shuffle(indices)
    
    # 16 ihale_itirazi
    for i in range(16):
        idx = indices[current_id - 162]
        name = f"{companies[i]} adına {names[idx]}"
        addr = addresses[idx]
        tc = tcs[idx]
        date = f"0{random.randint(1,9)}.08.2026"
        
        base_konu, base_detay = ihale_konulari[i % len(ihale_konulari)]
        detay = base_detay.replace("{okul}", okullar[i % len(okullar)])
        
        closing = closings[i % len(closings)]
        zorluk = random.choices(["kolay", "orta", "zor"], weights=[0.6, 0.2, 0.2])[0]
        eksik = random.random() < 0.2
        
        if zorluk == "zor":
            metin = f"KAYMAKAMLIĞA\n\nFirmamız {base_konu} sürecinde haksızlığa uğramıştır. {detay} İhalenin iptali gerekmektedir. {closing}\n\nİmza: {name}"
        else:
            metin = f"ÖRENLİ İLÇE KAYMAKAMLIĞINA\n\nBAŞVURAN: {name}\nAdres: {addr}\nVergi No: {tc}\n\nKONU: {base_konu}\n\nAÇIKLAMALAR:\n1. {detay}\n2. 4734 sayılı Kanun uyarınca başvurumuzun değerlendirilmesini istiyoruz.\n3. {closing}\n\nTarih: {date}\nİmza: {name}"
            if eksik:
                metin = metin.replace(f"Tarih: {date}\n", "")
                date = None
                
        records.append({
            "id": f"SENT-{current_id:04d}",
            "evrak_turu_dogru": "ihale_itirazi",
            "hedef_birim_dogru": "yazi_isleri",
            "uretim_yontemi": "serbest_llm",
            "eksik_alan_var_mi": eksik or zorluk == "zor",
            "zorluk": zorluk,
            "metin": metin,
            "beklenen_alanlar": {
                "gonderen_adi": name,
                "tarih": date if zorluk != "zor" else None,
                "konu": base_konu,
                "talep_metni": detay
            }
        })
        current_id += 1

    # 12 sosyal_yardim_basvuru
    for i in range(12):
        idx = indices[current_id - 162]
        name = names[idx]
        addr = addresses[idx]
        tc = tcs[idx]
        date = f"1{random.randint(0,9)}.08.2026"
        
        base_konu, base_detay = sosyal_yardim_konulari[i % len(sosyal_yardim_konulari)]
        detay = base_detay.replace("{ay}", ["Eylül", "Ekim", "Kasım"][i % 3]).replace("{sayi}", str(i%3 + 1))
        closing = closings[(i + 5) % len(closings)]
        
        zorluk = random.choices(["kolay", "orta", "zor"], weights=[0.6, 0.2, 0.2])[0]
        eksik = random.random() < 0.2
        
        if zorluk == "zor":
            metin = f"KAYMAKAMLIĞA\n\n{base_konu} talebim vardır. {detay} {closing}\n\n{name}"
        else:
            metin = f"ÖRENLİ İLÇE KAYMAKAMLIĞINA\n(Sosyal Yardımlaşma ve Dayanışma Vakfı)\n\nBAŞVURAN: {name}\nAdres: {addr}\nT.C. Kimlik No: {tc}\n\nKONU: {base_konu}\n\nAÇIKLAMALAR:\n1. {detay}\n2. {closing}\n\nTarih: {date}\nİmza: {name}"
            if eksik:
                metin = metin.replace(f"Adres: {addr}\n", "")
                
        records.append({
            "id": f"SENT-{current_id:04d}",
            "evrak_turu_dogru": "sosyal_yardim_basvuru",
            "hedef_birim_dogru": "sydv",
            "uretim_yontemi": "serbest_llm",
            "eksik_alan_var_mi": eksik or zorluk == "zor",
            "zorluk": zorluk,
            "metin": metin,
            "beklenen_alanlar": {
                "gonderen_adi": name,
                "tarih": date if zorluk != "zor" else None,
                "konu": base_konu,
                "talep_metni": detay
            }
        })
        current_id += 1

    # 14 tapu_kadastro_basvuru
    for i in range(14):
        idx = indices[current_id - 162]
        name = names[idx]
        addr = addresses[idx]
        tc = tcs[idx]
        date = f"2{random.randint(0,8)}.08.2026"
        
        base_konu, base_detay = tapu_konulari[i % len(tapu_konulari)]
        detay = base_detay.replace("{ada}", str(100 + i*5)).replace("{parsel}", str(1 + i))
        closing = closings[(i + 10) % len(closings)]
        
        zorluk = random.choices(["kolay", "orta", "zor"], weights=[0.6, 0.2, 0.2])[0]
        eksik = random.random() < 0.2
        
        if zorluk == "zor":
            metin = f"KAYMAKAMLIĞA\n\nTapumla ilgili {base_konu} durumum mevcuttur. {detay} {closing}\n\n{name}"
        else:
            metin = f"ÖRENLİ İLÇE KAYMAKAMLIĞINA\n\nBAŞVURAN: {name}\nAdres: {addr}\nT.C. Kimlik No: {tc}\n\nKONU: {base_konu}\n\nAÇIKLAMALAR:\n1. {detay}\n2. {closing}\n\nTarih: {date}\nİmza: {name}"
            if eksik:
                metin = metin.replace(f"T.C. Kimlik No: {tc}\n", "")
                
        records.append({
            "id": f"SENT-{current_id:04d}",
            "evrak_turu_dogru": "tapu_kadastro_basvuru",
            "hedef_birim_dogru": "tapu",
            "uretim_yontemi": "serbest_llm",
            "eksik_alan_var_mi": eksik or zorluk == "zor",
            "zorluk": zorluk,
            "metin": metin,
            "beklenen_alanlar": {
                "gonderen_adi": name,
                "tarih": date if zorluk != "zor" else None,
                "konu": base_konu,
                "talep_metni": detay
            }
        })
        current_id += 1
        
    return records

def main():
    # 1. Read existing
    with open(KAYNAK, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    final_lines = []
    
    # 2. Filter out old 0162-0203
    for line in lines:
        if not line.strip(): continue
        rec = json.loads(line)
        rec_id = rec["id"]
        
        # We only keep IDs < SENT-0162
        if rec_id < "SENT-0162":
            final_lines.append(line)
            
    # 3. Generate 42 unique records
    new_records = generate_records()
    
    # 4. Append and write back
    for rec in new_records:
        final_lines.append(json.dumps(rec, ensure_ascii=False) + "\n")
        
    with open(KAYNAK, 'w', encoding='utf-8') as f:
        f.writelines(final_lines)
        
    print(f"Total lines written: {len(final_lines)}")
    print("Regeneration complete.")

if __name__ == '__main__':
    main()
