# templates/README.md
# Resmî Yazışma Format Motoru — Şablon & Doğrulayıcı

Kaynak yönetmelik: **Resmî Yazışmalarda Uygulanacak Usul ve Esaslar
Hakkında Yönetmelik** (RG 10.06.2020/31151, No. 2646) +
**Cumhurbaşkanlığı Kılavuzu** (2022).

---

## Kurulum

```bash
# Bağımlılıklar
pip install jinja2 pytest

# Proje kökünde çalıştır (doğru import yolları için)
cd <proje_koku>
```

---

## Şablonları Kullanma

```python
# Önerilen kullanım: doğrudan Jinja2 açmak yerine merkezi renderer'u çağır
from renderers.template_renderer import render_ust_yazi

cikti = render_ust_yazi({
    "tc_baslik": {
        "idare_adi": "ÇEVRE VE ŞEHİRCİLİK BAKANLIĞI",
        "birim_adi": "Bilgi İşlem Dairesi Başkanlığı",
    },
    "sayi": "E-67915368-903.07.02-4752",
    "tarih": "07.08.2026",
    "konu": "Personel Hareketleri Hakkında",
    "muhatap": {"tur": "kurum", "isim": "ÇALIŞMA VE SOSYAL GÜVENLİK BAKANLIĞINA"},
    "muhatap_turu": "kurum_ust",
    "metin_paragraflari": ["İlgili yazışmalar hakkında bilgi sunulmaktadır."],
    "kapalis_ifadesi": "arz ederim.",
    "imza": {
        "ad_soyad": "Mehmet YILMAZ",
        "unvan": "Daire Başkanı",
        "yetki_turu": "normal",
    },
    "iletisim": {"adres": "Ankara 06100", "irtibat": "Ayşe KAYA"},
})
print(cikti)
```

> **Dikkat:** `renderers/template_renderer.py` `StrictUndefined` ile merkezi olarak
> yapılandırılmıştır. Doğrudan `jinja2.Environment` açarsanız bu güvenceyi kaybedersiniz.

### Tekit Yazısı — Zorunlu `gun` Parametresi

```python
from renderers.template_renderer import render_tekit_yazisi

cikti = render_tekit_yazisi({
    # ... ortak alanlar ...
    "ilgi": [{
        "tarih": "01.07.2026",
        "sayi": "E-67915368-903.07.02-1000",
        "aciklama": "yazı",
    }],
    "gun": 10,   # ZORUNLU — varsayılan yoktur (aşağıdaki nota bakınız)
})
```

> **Not:** `gun` parametresi varsayılan değer almaz.  
> Kılavuz Örnek 24'teki "5 gün" ifadesi tek bir örnek senaryodur;  
> Madde 34 sayısal bir süre belirtmez.

---

## Format Doğrulama

```python
from validators.format_validator import validate_format

taslak = { ... }  # şablon context ile aynı sözlük
sonuc = validate_format(taslak, "ust_yazi")

if sonuc.gecerli:
    print("✓ Format geçerli")
else:
    for hata in sonuc.hatalar:
        print(f"[{hata.kural_kodu}] {hata.mesaj}  ({hata.madde_ref})")
```

---

## Testleri Çalıştırma

```bash
# Proje kökünden:
pytest tests/ -v
```

---

## Yazı Türleri ve Şablonlar

| Yazı Türü | Şablon | Notlar |
|---|---|---|
| Üst yazı | `ust_yazi.jinja2` | Temel şablon |
| Cevap yazısı | `cevap_yazisi.jinja2` | `ilgi` zorunlu |
| Tekit yazısı | `tekit_yazisi.jinja2` | Konu/metin/kapanış sabitlenmiş |
| Bilgilendirme yazısı | `ust_yazi.jinja2` | Ayrı şablon yoktur — bkz. \[TASARIM KARARI\] #6 |

---

## \[TASARIM KARARI\] Maddeleri — Jüri Referans Tablosu

Bu maddeler **yönetmelik hükmü değildir**; ekip kararıdır.  
Kodda `# [TASARIM KARARI]` yorum etiketiyle işaretlenmiştir.

| # | Konu | Karar | Gerekçe |
|---|---|---|---|
| 1 | Satır aralığı | 1.0 (tek satır) | Yönetmelik/kılavuzda sayısal değer belirtilmemiştir; tutarlılık için seçildi |
| 2 | Ek ve Dağıtım öncesi boşluk | 2 satır | Yönetmelik "uygun satır boşluğu" der, sayı vermez; tekrar eden 2-satır kalıbına tutarlı |
| 3 | Kısaltma kuralı kapsamı | Sadece kurumsal/özel isim kısaltmaları (TBMM, KEP) | Yönetmelik/kılavuzda genel↔kurumsal ayrımı net değil |
| 4 | 9pt'a küçültme | MVP'de uygulanmaz | Somut eşik tanımlı değil, nadir kenar durum |
| 5 | Arz/rica (kurum muhatap, hiyerarşi belirsiz) | Varsayılan "arz ederim." | Hiyerarşi matrisi yönetmelikte tanımlı değil; güvenli taraf seçildi |
| 6 | Bilgilendirme yazısı şablonu | `ust_yazi.jinja2` kullanılır | Kılavuz Bölüm C: ayrı biçimsel şablon yoktur |

> **Cevap yazısında ilgi zorunluluğu** ayrıca `[TASARIM KARARI]` olarak
> işaretlenmiştir: yönetmelikte cevap yazısı için ilgi zorunluluğu
> kaynaklı değildir (tekit yazısı için Madde 34'te kaynaklıdır); ekip
> kararıdır.

> **`renderers/template_renderer.py` — Renderer Güvenceleri:**
> `gun` ve `ilgi` zorunluluğu render öncesi **pre-check** ile garanti edilir;
> `StrictUndefined` singleton olarak merkezi tanımlanmıştır. Ajan 6,
> doğrudan `jinja2.Environment` açmak yerine `render_*` fonksiyonlarını
> kullanmalıdır — aksi takdirde bu güvenceler devre dışı kalır.

---

## Bilgilendirme Yazısı — İmza Yetkisi TODO

```
TODO: Bilgilendirme yazısında Bakan Yardımcısı da imzalayabilir.
      Bu bir YETKİ kuralıdır, FORMAT kuralı değildir.
      validators/format_validator.py'de ele alınmamıştır.
      Ayrı bir yetki kontrol modülünde implemente edilmeli (MVP kapsamı dışı).
```
