# schemas/ — Alan Sahiplik Matrisi ve Tasarım Kararları

Bu klasör Pipeline 1 (Arayüz Şeması / JSON Sözleşmesi) çıktısını içerir.

## İçerik

| Dosya | Açıklama |
|---|---|
| `evrak_state_schema.py` | LangGraph 6-düğümlü akış için paylaşılan `EvrakState` Pydantic modeli |
| `test_evrak_state_schema.py` | Şema doğrulama testleri |

---

## Alan Sahiplik Matrisi

Her alanı kimin yazdığı (W) ve kimin okuduğu (R) gösterilmiştir.

| Alan | OCR | Sınıf+Çıkarım | Mevzuat RAG | Kural Motoru | Taslaklama | Doğrulama | HITL |
|---|---|---|---|---|---|---|---|
| `evrak_id` | R | R | R | R | R | R | R |
| `kurum_profili_id` | R | R | R | R | R | R | R |
| `pipeline_asamasi` | W | W | W | W | W | W | W |
| `ham_metin` | **W** | R | R | — | — | — | — |
| `ocr_guven_skoru` | **W** | R | — | — | — | — | — |
| `kaynak_format` | **W** | R | — | — | — | — | — |
| `evrak_turu` | — | **W** | R | R | R | R | — |
| `evrak_turu_guven` | — | **W** | — | — | — | — | — |
| `alanlar` | — | **W** | R | R | R | R | — |
| `eksik_alanlar` | — | **W** | — | R | — | — | — |
| `mevzuat_eslesmeleri` | — | — | **W** | R | R | R | — |
| `yazi_turu` | — | — | — | **W** | R | R | — |
| `yazi_turu_kaynagi` | — | — | — | **W** | R | — | — |
| `yonlendirme` | — | — | — | **W** | R | — | — |
| `muhatap` | — | — | — | **W** | R | R | — |
| `muhatap_turu` | — | — | — | **W** | R | R | — |
| `taslak_metin` | — | — | — | — | **W** | R | R |
| `sablon_id` | — | — | — | — | **W** | R | — |
| `dogrulama` | — | — | — | — | — | **W** | R |
| `hitl_karari` | — | — | — | — | — | — | **W** |
| `hitl_kullanici` | — | — | — | — | — | — | **W** |
| `hitl_notu` | — | — | — | — | — | — | **W** |
| `hitl_zamani` | — | — | — | — | — | — | **W** |
| `audit_log` | W | W | W | W | W | W | W |

> **W** = Yazan, **R** = Okuyan, **—** = Kullanmıyor

---

## Hardcode Etmeme İlkesi

**Bu projede benimsenen temel mimari ilke:** çekirdek motor kurum-bağımsız çalışır;
kurum-özel veri ayrı bir config dosyasından (`kurum_profili.yaml`) enjekte edilir.

Bu ilke gereği aşağıdaki üç alan **kasıtlı olarak düz `str` bırakılmıştır**
ve hiçbir zaman `Enum` veya `Literal` yapılmamalıdır:

| Alan | Neden str? |
|---|---|
| `evrak_turu` | Evrak türleri kuruma göre değişir (kaymakamlık ≠ belediye). Sabit Enum farklı kurum profillerine geçişi kırar. |
| `yazi_turu` | Çıktı şablon türleri config'den gelir; şema merge sırasında değişmemeli. |
| `YonlendirmeKarari.onerilen_birim_id` | Birim ID'leri tamamen kurum-özel; Pipeline 4'ün ürettiği config'e aittir. |

Bu üç alanın gerçek değer kümesi **Pipeline 4 (Kurum Config)** tarafından
`data/config/kurum_profili_kaymakamlik.yaml` dosyasında tanımlanmıştır ve
bu dosya artık bu repoda mevcuttur.

---

## Pipeline 3/4 Çapraz Kontrol Sonuçları

> **Durum (2026-08-10):** Pipeline 3 ve Pipeline 4 merge edilmiştir.
> Aşağıdaki çapraz kontroller `data/config/kurum_profili_kaymakamlik.yaml`
> ve `docs/kaynak_referanslari.md` dosyaları gerçekten okunarak yapılmıştır.

### a) `evrak_turu` ↔ `kurum_profili.yaml / evrak_turleri[*].id`

✅ **Tutarlı.** YAML'da tanımlı `evrak_turleri` id'leri:

| id | Açıklama |
|---|---|
| `dilekce` | Vatandaş Dilekçesi (3071 sayılı Kanun) |
| `bilgi_edinme` | Bilgi Edinme Başvurusu (4982 sayılı Kanun) |
| `kurumlar_arasi_yazi` | Kurumlar Arası Resmî Yazışma |
| `ihale_itirazi` | İhale İtiraz/Şikayet Dilekçesi |
| `sosyal_yardim_basvuru` | Sosyal Yardım Başvurusu |
| `tapu_kadastro_basvuru` | Tapu/Kadastro İşlem Başvurusu |

`EvrakState.evrak_turu` alanı bu id'leri doğrudan string olarak alabilir.
Sınıflandırma düğümü bu listeyi çalışma zamanında config'den okuyacaktır.

### b) `yazi_turu` ↔ `kurum_profili.yaml / yazi_turleri[*].id`

✅ **Tutarlı.** ~~`sablon_haritasi`~~ — bu anahtar **YAML'da yoktur**; yapı düzeltildi.
Gerçek yapı: `yazi_turleri` listesinin her öğesinde `id` ve `sablon` alanları bulunur.

| `yazi_turu` id | Şablon (`sablon` alanı) |
|---|---|
| `ust_yazi` | `templates/ust_yazi.jinja2` |
| `cevap_yazisi` | `templates/cevap_yazisi.jinja2` |
| `bilgilendirme_yazisi` | `templates/ust_yazi.jinja2` (Tasarım Kararı #6) |
| `tekit_yazisi` | `templates/tekit_yazisi.jinja2` |

`EvrakState.yazi_turu` alanı bu dört id'den birini alır; şablon seçimi
Taslaklama düğümü tarafından `yazi_turleri[*].sablon` alanından yapılır.

### c) `onerilen_birim_id` ↔ `kurum_profili.yaml / birimler[*].id`

✅ **Tutarlı.** YAML'da tanımlı `birimler` id'leri (9 adet):

`yazi_isleri` · `nufus` · `sydv` · `milli_egitim` · `saglik` ·
`mal_mudurlugu` · `tapu` · `tarim` · `emniyet`

`YonlendirmeKarari.onerilen_birim_id` alanı bu id'lerden birini alır.
Kural Motoru düğümü, eşleştirme için `birimler[*].anahtar_kelimeler` listesini kullanır.

### d) `MevzuatEslesme.kaynak_dokuman` ↔ `data/raw/mevzuat/` dosya adları

✅ **Tutarlı.** `docs/kaynak_referanslari.md` incelendi. `data/raw/mevzuat/`
içindeki dosyalar ve önerilen `kaynak_dokuman` değerleri:

| Dosya adı | Önerilen `kaynak_dokuman` değeri |
|---|---|
| `resmi_yazisma_yonetmeligi.pdf` | `"resmi_yazisma_yonetmeligi"` |
| `resmi_yazisma_kilavuzu.pdf` | `"resmi_yazisma_kilavuzu"` |
| `3071_dilekce_hakki_kanunu.pdf` | `"3071_dilekce_hakki_kanunu"` |
| `4982_bilgi_edinme_kanunu.pdf` | `"4982_bilgi_edinme_kanunu"` |
| `5442_il_idaresi_kanunu.pdf` | `"5442_il_idaresi_kanunu"` |

`kaynak_dokuman` alanı serbest `str` olduğundan zorunlu bir format kısıtı
yoktur; ancak dosya adı tabanlı isimlendirme (`.pdf` uzantısı olmadan)
önerilen konvansiyondur — Mevzuat RAG düğümü bu formatı benimsemelidir.
