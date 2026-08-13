# Proje Durum Özeti — TEKNOFEST 2026 Yapay Zeka Dil Ajanları Yarışması, Senaryo 1

Bu belge, projenin şu ana kadarki tüm ilerlemesini özetler. Kaldığınız
yerden devam etmek için buradan başlayın.

---

## 1. Proje Kimliği

- **Yarışma:** TEKNOFEST 2026 Yapay Zeka Dil Ajanları Yarışması — Senaryo 1
- **Tema:** Kamu Evrak ve Yazışma Süreçleri için Çok Ajanlı Akıllı Destek Sistemi
- **Demo kurum profili:** Örenli İlçe Kaymakamlığı (kurgusal)
- **Repo:** teknofest-2026-dil-ajanlari (GitHub, public, Apache-2.0 lisanslı)
- **Mimari yaklaşım:** Kurum-bağımsız çekirdek motor + kurum-özel config
  profili (multi-tenant); dengeli (optimize) ajan akışı — feature-flag
  ile 8-ajanlı orijinal tasarıma da geri dönülebilir.

---

## 2. FAZ 0 — TAMAMLANDI (4/4 Pipeline)

| # | Pipeline | Çıktı | Durum |
|---|---|---|---|
| 1 | Arayüz Şeması | schemas/evrak_state_schema.py — EvrakState Pydantic modeli, 6 düğümün ortak state'i. evrak_turu/yazi_turu/onerilen_birim_id bilinçli olarak str (Enum değil) — kurum-bağımsızlık ilkesi. 10 test. | Tamamlandı |
| 2 | Format Motoru | templates/ (3 Jinja2 şablonu: ust_yazi, cevap_yazisi, tekit_yazisi — bilgilendirme_yazisi ayrı şablon kullanmaz, ust_yazi'yi kullanır), validators/format_validator.py, renderers/template_renderer.py (StrictUndefined singleton, ön-kontroller). 148 test. | Tamamlandı |
| 3 | Mevzuat Korpusu | data/raw/mevzuat/ — 5 kaynak: Resmî Yazışma Yönetmeliği, Kılavuzu, 3071, 4982, 5442 sayılı kanunlar. docs/kaynak_referanslari.md. | Tamamlandı |
| 4 | Kurum Config | data/config/kurum_profili_kaymakamlik.yaml — 9 birim, 6 evrak türü, 4 yazı türü (şablonlarla eşleştirilmiş). | Tamamlandı |

**Kritik tasarım ilkeleri (kodda somutlaşmış):**
- Hardcode etmeme: kurum-özel değerler (evrak türü, yazı türü, birim id) asla Enum/Literal yapılmadı.
- Şablon + kod hibrit: LLM'e resmî yazı biçimi hiç bırakılmadı, format_validator + renderer garanti ediyor.
- Dengeli mimari: 8 mantıksal rol -> 6 düğüm -> tipik vakada 3 LLM çağrısı (Sınıf+Çıkarım, Mevzuat RAG, Taslaklama); Kural Motoru ve Doğrulama önce ücretsiz kod, sadece belirsizlikte LLM'e eskale.

---

## 3. VERİ AŞAMASI — TAMAMLANDI

| # | İş | Durum | Detay |
|---|---|---|---|
| 1 | evraklar.jsonl | Tamamlandı | 161 kayıt, 6 evrak türü. |
| 2a | OCR Görselleri | Tamamlandı | 72 görsel (temiz/orta/zor 24'er adet), evraklar.jsonl'dan üretildi. |
| 2b | Eksik-Alan Varyantları | Kapsandı | evraklar.jsonl içindeki eksik_alan_var_mi kayıtları yeterli görüldü, ayrı dosya açılmadı. |
| 2c | Gold Taslaklar | Tamamlandı | 52 kayıt, format_validator 52/52, 4/4 pytest. |
| 2d | RAG Test Seti | Tamamlandı | 45 soru-madde çifti, 44'ü tam doğrulanmış, 1'i (RAG-035) şeffaf şekilde "insan_dogrulamasi_gerekli" işaretli. |
| 3 | Genel Doğrulama | Kapsandı (dağıtık) | Her veri kategorisi kendi doğrulama script'iyle kontrol edildi (kalite_kontrol.py, gold_taslak_kontrol.py, checklist çapraz doğrulama). |
| 4 | İnsan gözden geçirme | Kapsandı (sürekli) | Her üretim turu, örneklem yerine kapsamlı olarak elle incelendi. |

**VERİ AŞAMASI TAMAMEN KAPANDI.**

---

## 4. Bu Süreçte Öğrenilen Önemli Dersler

1. **Format motorunda "koda sabitleme" gerekçesi:** LLM biçim garantisi veremez; RAG farklı bir problem (içerik doğruluğu) çözer, format motoru başka bir problemi (yapısal tutarlılık) çözer — ikisi rakip değil, tamamlayıcı.
2. **Sentetik veri "kafadan" üretilmez:** Gerçek referans kaynaklardan (kaymakamlık siteleri, resmî formlar) yapısal kalıp çıkarılıp, içerik kurgusal üretildi (docs/sentetik_veri_referans_ornekler.md).
3. **Gold taslaklar LLM'e yazdırılmaz (döngüsellik riski):** Bağımsız sohbette taslak önerisi alınır, insan onaylar — çekirdek Ajan 6 hattından tamamen ayrı.
4. **Hata teşhisinde iki tür ayrımı kritik:** Bazen sorun veridedir (isim sızması, kalıp tekrarı -> veriyi düzelt), bazen koddadır (TARIH_FORMAT, IMZA_BLOKU parser hataları -> kanıtla, sonra kodu düzelt). Her ikisinde de önce teşhis, sonra düzeltme — asla varsayımla hareket etme.
5. **Encoding felaketi:** PowerShell/terminal komutlarına Türkçe metin asla doğrudan parametre verilmemeli; sadece Python içinde encoding='utf-8' ile dosya yazımı yapılmalı.
6. **Kurum-bağımsızlık mimaride süreklilik:** Yeni bir kuruma (örn. Belediye) geçişte kod değişmeyecek, sadece config dosyası değişecek — bu, ticarileşme argümanının somut kanıtı.

---

## 5. Henüz Yazılmayan Kısım — Açık ve Net

**Hiçbir ajanın gerçek LLM/iş mantığı kodu henüz yazılmadı.** Şu ana kadarki her şey "malzeme" (şema, şablon, veri) — sistemin kendisi (OCR okuma, sınıflandırma, RAG sorgusu, taslaklama, yönlendirme, doğrulama ajanlarının çalışan kodu) Faz 1 sonrası, Ajan Geliştirme aşamasında yazılacak.

## 6. Kalan Yol Haritası (Büyük Resim)

```
Veri Aşaması (devam ediyor)
        v
Faz 1 - Altyapı + İskelet Arayüz
  (Orkestrasyon iskeleti/mock ajanlar, Docker+Qdrant+PostgreSQL,
   Streamlit boş demo ekranı, Mevzuat işleme/chunk+embed)
        v
Ajan Geliştirme (Track A/B) - PROJENİN EN BÜYÜK İŞİ
  (Track A: OCR, Sınıf+Çıkarım, Mevzuat RAG gerçek kodu
   Track B: Kural Motoru, Taslaklama, Doğrulama gerçek kodu)
        v
Entegrasyon + Demo Bağlama
  -> BURADA gerçek, test edilebilir uygulama ortaya çıkar
```

---

## 7. Sıradaki Somut Adım (Bir Sonraki Oturumda)

Veri Aşaması tamamen bitti. Sırada **Faz 1 — Altyapı + İskelet Arayüz**
var:
- Orkestrasyon iskeleti (LangGraph, mock ajanlar, koşullu kenarlar)
- Docker Altyapı (Qdrant + PostgreSQL)
- Demo Arayüzü iskeleti (Streamlit, boş şablon)
- Mevzuat İşleme (5 kaynağın chunk + embed edilip Qdrant'a yüklenmesi)

İlk üçü birbirinden bağımsız, paralel yürütülebilir. Mevzuat İşleme,
Docker Altyapı'nın (Qdrant çalışır olması) bitmesini bekler.

---

## 8. Kapanış Notu — Commit c0e2572 (Son Push)

Bu commit ile şunlar GitHub'a (main branch) güvenle işlendi:
- `data/sentetik/evraklar.jsonl` (161 kayıt, tam doğrulanmış)
- `data/sentetik/gold_taslaklar.jsonl` (52 kayıt, format_validator
  52/52 geçti, 4/4 pytest)
- `scripts/gold_taslak_kontrol.py`, `scripts/test_gold_taslak_kontrol.py`
  (daha önce yanlışlıkla hiç commit edilmemişti, bu turda düzeltildi)
- `scripts/kalite_kontrol.py` (data/sentetik/'ten taşındı, yol
  referansı güncellendi)
- Repo temizliği: 9 geçici/tek-kullanımlık script + 2 ara dosya
  silindi

**Toplam test sayısı: 162, hepsi geçiyor.**

Bir sonraki oturuma buradan devam edin — Bölüm 7'deki iki bağımsız
işten (OCR Görselleri / RAG Test Seti) biriyle başlayın.
