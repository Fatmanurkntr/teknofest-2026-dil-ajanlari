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
`data/config/kurum_profili_kaymakamlik.yaml` dosyasında tanımlanacaktır.
Bu dosya henüz merge edilmemiş paralel bir branch'te geliştirilmektedir.

---

## Pipeline 3/4 Merge Sonrası Yapılacaklar

> **ÖNEMLİ:** Pipeline 3 (Mevzuat Korpusu) ve Pipeline 4 (Kurum Config)
> bu branch'e merge edildiğinde aşağıdaki çapraz kontroller yapılmalıdır:

1. `evrak_turu` alanında kullanılan string değerlerin `kurum_profili.yaml`
   içindeki `evrak_turleri` listesiyle tutarlılığını doğrula.
2. `yazi_turu` alanında kullanılan string değerlerin `kurum_profili.yaml`
   içindeki `sablon_haritasi` anahtarlarıyla eşleştiğini doğrula.
3. `YonlendirmeKarari.onerilen_birim_id` değerlerinin `kurum_profili.yaml`
   içindeki `birimler` listesinde bulunduğunu doğrula.
4. `MevzuatEslesme.kaynak_dokuman` formatının Pipeline 3 çıktısıyla
   uyumlu olduğunu doğrula.

> **NOT:** `data/config/kurum_profili_kaymakamlik.yaml` ve
> `docs/kaynak_referanslari.md` dosyaları bu branch'te mevcut değildir —
> bunlar Pipeline 3/4'ün paralel branch'inde geliştiriliyor. Bu normaldir.
